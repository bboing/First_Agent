from collections import defaultdict
from datetime import datetime

import xml.etree.ElementTree as ET
import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

def validate_xml(xml_string):
    try:
        root = ET.fromstring(xml_string)
        if root.tag != '{http://www.omg.org/spec/BPMN/20100524/MODEL}definitions':
            print("Error: Root element is not <bpmn:definitions>")
            return False
        return True
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
        return False

def escape_xml(text):
    # XML 특수 문자 이스케이프
    return (text.replace('&', '&')
                .replace('<', '<')
                .replace('>', '>')
                .replace('"', '"')
                .replace("'", "'"))
                         

def parse_bpmn_to_dataframe(xml_file_path):
    try:
        with open(xml_file_path, 'r', encoding='utf-8') as f:
            xml_string = f.read().strip()
    except FileNotFoundError:
        print(f"Error: File {xml_file_path} not found.")
        return None, None
    except UnicodeDecodeError:
        print("UTF-8 decoding failed, trying latin-1...")
        try:
            with open(xml_file_path, 'r', encoding='latin-1') as f:
                xml_string = f.read().strip()
        except Exception as e:
            print(f"Error reading file: {e}")
            return None, None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None

    xml_string = escape_xml(xml_string)
    
    if not validate_xml(xml_string):
        print("Invalid XML format")
        return None, None

    namespaces = {
        'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
        'custom': 'http://custom'
    }

    root = ET.fromstring(xml_string)
    elements = []
    flows = []
    missing_ids = []

    def get_element_info(element, element_type, lane=None):
        elem_id = element.get('id', '')
        name = element.get('name', '')
        # Custom 속성 추출
        custom_attrs = {k: v for k, v in element.attrib.items() if k.startswith('{http://custom}')}
        custom_attrs_str = '; '.join([f"{k.split('}')[1]}={v}" for k, v in custom_attrs.items()])
        
        doc = element.find('bpmn:documentation', namespaces)
        documentation = doc.text.strip() if doc is not None and doc.text else ''
        
        # Incoming/Outgoing flows: 텍스트로 처리
        incoming = [f.text for f in element.findall('bpmn:incoming', namespaces) if f.text is not None]
        outgoing = [f.text for f in element.findall('bpmn:outgoing', namespaces) if f.text is not None]
        
        # 텍스트 누락 확인
        for f in element.findall('bpmn:incoming', namespaces):
            if f.text is None:
                missing_ids.append(f"Missing text in <bpmn:incoming> for {element_type} {elem_id} ({name})")
        for f in element.findall('bpmn:outgoing', namespaces):
            if f.text is None:
                missing_ids.append(f"Missing text in <bpmn:outgoing> for {element_type} {elem_id} ({name})")
        
        data_objects = []
        for data_obj in element.findall('.//bpmn:dataObjectReference', namespaces):
            data_objects.append(data_obj.get('name', ''))
        for data_store in element.findall('.//bpmn:dataStoreReference', namespaces):
            data_objects.append(data_store.get('name', ''))
        data_objects_str = '; '.join(data_objects)
        
        relationships = element.find('.//custom:relationships/custom:relation', namespaces)
        rel_str = relationships.get('next', '') if relationships is not None else ''
        
        return {
            'Element Type': element_type,
            'Element ID': elem_id,
            'Element Name': name,
            'Lane': lane,
            'Documentation': documentation,
            'Custom Attributes': custom_attrs_str,
            'Data Objects': data_objects_str,
            'Incoming Flow ID': '; '.join(incoming),
            'Outgoing Flow ID': '; '.join(outgoing),
            'Custom Relationships': rel_str
        }

    lane_map = {}
    for lane in root.findall('.//bpmn:lane', namespaces):
        lane_id = lane.get('id')
        lane_name = lane.get('name', '')
        for node_ref in lane.findall('bpmn:flowNodeRef', namespaces):
            lane_map[node_ref.text] = lane_name

    process = root.find('bpmn:process', namespaces)
    process_id = process.get('id', '') if process is not None else ''
    process_name = process.get('name', '') if process is not None else ''
    custom_attrs = {k: v for k, v in process.attrib.items() if k.startswith('{http://custom}')}
    process_custom_attrs = '; '.join([f"{k.split('}')[1]}={v}" for k, v in custom_attrs.items()])

    collaboration = root.find('bpmn:collaboration', namespaces)
    participant_id = ''
    participant_name = ''
    if collaboration is not None:
        participant = collaboration.find('bpmn:participant', namespaces)
        participant_id = participant.get('id', '') if participant is not None else ''
        participant_name = participant.get('name', '') if participant is not None else ''

    for task in root.findall('.//bpmn:task', namespaces):
        elements.append(get_element_info(task, 'Task', lane_map.get(task.get('id'), '')))
    
    for sub_process in root.findall('.//bpmn:subProcess', namespaces):
        elements.append(get_element_info(sub_process, 'Sub-Process', lane_map.get(sub_process.get('id'), '')))
    
    for call_activity in root.findall('.//bpmn:callActivity', namespaces):
        elements.append(get_element_info(call_activity, 'Call Activity', lane_map.get(call_activity.get('id'), '')))
    
    for start_event in root.findall('.//bpmn:startEvent', namespaces):
        elements.append(get_element_info(start_event, 'Start Event', lane_map.get(start_event.get('id'), '')))
    
    for end_event in root.findall('.//bpmn:endEvent', namespaces):
        elements.append(get_element_info(end_event, 'End Event', lane_map.get(end_event.get('id'), '')))
    
    for gateway in root.findall('.//bpmn:exclusiveGateway', namespaces):
        elements.append(get_element_info(gateway, 'Exclusive Gateway', lane_map.get(gateway.get('id'), '')))
    
    for gateway in root.findall('.//bpmn:inclusiveGateway', namespaces):
        elements.append(get_element_info(gateway, 'Inclusive Gateway', lane_map.get(gateway.get('id'), '')))
    
    for gateway in root.findall('.//bpmn:parallelGateway', namespaces):
        elements.append(get_element_info(gateway, 'Parallel Gateway', lane_map.get(gateway.get('id'), '')))

    for flow in root.findall('.//bpmn:sequenceFlow', namespaces):
        flow_id = flow.get('id', '')
        source_ref = flow.get('sourceRef', '')
        target_ref = flow.get('targetRef', '')
        flow_name = flow.get('name', '')
        is_message = flow.get('{http://custom}IsMessage', 'false') == 'true'
        flow_type = 'Message Flow' if is_message else 'Sequence Flow'
        
        flows.append({
            'Flow ID': flow_id,
            'Flow Type': flow_type,
            'Flow Source': source_ref,
            'Flow Target': target_ref,
            'Flow Name': flow_name
        })

    graph = defaultdict(list)
    reverse_graph = defaultdict(list)
    for flow in flows:
        graph[flow['Flow Source']].append(flow['Flow Target'])
        reverse_graph[flow['Flow Target']].append(flow['Flow Source'])

    def dfs(node, visited, order, current_order):
        visited.add(node)
        neighbors = graph[node]
        sorted_neighbors = sorted(neighbors, key=lambda x: any(flow['Flow Name'].lower() == 'yes' for flow in flows if flow['Flow Target'] == x), reverse=True)
        for neighbor in sorted_neighbors:
            if neighbor not in visited:
                order[neighbor] = current_order[0] + 1
                current_order[0] += 1
                dfs(neighbor, visited, order, current_order)

    order = {}
    visited = set()
    current_order = [0]
    
    start_events = [e['Element ID'] for e in elements if e['Element Type'] == 'Start Event']
    for start in start_events:
        if start not in visited:
            order[start] = current_order[0] + 1
            current_order[0] += 1
            dfs(start, visited, order, current_order)

    elements_df = pd.DataFrame(elements)
    flows_df = pd.DataFrame(flows)
    
    elements_df['Sequence Order'] = elements_df['Element ID'].map(order).fillna(0).astype(int)
    
    elements_df['Process ID'] = process_id
    elements_df['Process Name'] = process_name
    elements_df['Process Custom Attributes'] = process_custom_attrs
    elements_df['Participant ID'] = participant_id
    elements_df['Participant Name'] = participant_name
    elements_df['Notes'] = ''
    
    if missing_ids:
        print("\nMissing ID warnings:")
        for msg in missing_ids:
            print(msg)
        elements_df['Notes'] = elements_df.apply(
            lambda row: '; '.join([msg for msg in missing_ids if row['Element ID'] in msg]), axis=1
        )
    
    elements_df.to_excel(f'{BASE_DIR}/result/bpmn_result/bpmn_elements_{timestamp}.xlsx', index=False)
    flows_df.to_excel(f'{BASE_DIR}/result/bpmn_result/bpmn_flows_{timestamp}.xlsx', index=False)
    
    return elements_df, flows_df