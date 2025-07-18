'''
Azure 기반 Allgero NX Manual Auto Chunker

< 개정 이력 >
...
# 25.06.25 파트별 기능 통
# 25.06.27 로직 추가 (주석으로 체크)
# 25.07.16 일부 기능 개선, 결과 디렉토리 재구성, os 일반화 등

< 향후 논의해야 할 agenda >
# Table Chunking Range
    ㄴ 최소 Chunk 보다 작은 경우, 최소 Chunk 유지
    ㄴ 김태균 과장 : 만약 최소 Chunk 보다 큰 경우, Table에서 병합된 부분까지 의미 단위로 쪼개는 방식 
    ㄴ 박세영 대리 : 몇 Depth 까지 고려할 것인가? 1 Depth에서 엄청 길게 나오면?
    ㄴ 김태균 과장 : 1 Depth 까지만 고려하는 것으로 우선 픽스
# Table Chunking 이후 passage page update

# DI 추출
    ㄴ DI 로 잘못 추출된 경우, 내용의 변형이 일어날 수 있음
    ㄴ 정확한 결과를 얻기 위해서 눈으로 검토하는 것은 불가피함.
    ㄴ 1개년 사업 범위 내에선 DI 추출 결과를 믿고 사용해도 무방할 것으로 판단(openparser 테이블 추출 결과 DI보다 퀄리티가 낮은 것으로 판단 또한, GPU 내부 MPS 사용 불가한지 체크 필요)
'''

from datetime import datetime
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentContentFormat, AnalyzeResult
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict
from pathlib import Path
import logging
import os
import re
import pandas as pd

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # backend root 디렉토리
DATA_DIR = os.path.join(BASE_DIR, "data")

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

 ########################## Part 1 ###########################
# Step 1-1
def process_files_in_directory(directory_path):
    '''디렉터리 순회하며 PDF 파일 처리 후 .md 파일 목록 반환'''
    results = []
    md_files = []  # 생성된 .md 파일 경로를 저장
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[-1].lower()
            if file_ext == '.pdf':
                logging.info(f"allegronx_chunker: PDF 파일 처리 중: {file_path}")
                try:
                    content, tables_data = analyze_documents_combined(file_path)
                    results.append({
                        'file_path': file_path,
                        'content': content,
                        'tables_data': tables_data
                    })
                    # 생성된 .md 파일 경로 추가
                    # 버그 수정 (Windows 호환되도록 수정함)
                    filename_wo_ext = os.path.splitext(os.path.basename(file_path))[0]
                    # 25.07.17 timestamp 제거 
                    output_file = os.path.join(BASE_DIR, "result", "md", f"{filename_wo_ext}.md")
                    md_files.append(output_file)
                except Exception as e:
                    logging.error(f"allegronx_chunker: 파일 처리 중 에러 발생: {file_path}, 에러: {str(e)}")
                    continue
            else:
                logging.warning(f"allegronx_chunker: 처리할 수 없는 파일 형식: {file_path}")
    return results, md_files  # 결과와 .md 파일 목록 반환


# Step 1-2.
def analyze_documents_combined(file_path):
    '''
    Azure DI를 사용하여 PDF를 추출하는 함수
    표 데이터 작업을 위해 같은 PDF 문서를 두 번 API 호출합니다.
    이후, 마크다운 타입으로 정제한 표를 원본 데이터에 치환
    '''
    load_dotenv()

    endpoint = os.getenv("AZURE_DI_ENDPOINT")
    key = os.getenv("AZURE_DI_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_DI_ENDPOINT or AZURE_DI_KEY is not set in the environment variables.")

    # Windows 호환 가능하도록 수정
    filename_wo_ext = os.path.splitext(os.path.basename(file_path))[0]
    # 25.07.17 timestamp 제거
    
    # 디렉토리 생성
    result_md_dir = os.path.join(BASE_DIR, "result", "md")
    result_tables_dir = os.path.join(BASE_DIR, "result", "tables")
    os.makedirs(result_md_dir, exist_ok=True)
    os.makedirs(result_tables_dir, exist_ok=True)
    
    output_file = os.path.join(result_md_dir, f"{filename_wo_ext}.md")
    table_output_file = os.path.join(result_tables_dir, f"tables_{filename_wo_ext}.txt")

    try:
        with open(file_path, "rb") as f:
            pdf_data = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # DI 두 번 호출 버전 코드 ---> 백업용, 지금은 비용 문제 때문에 쓰지 않음.
    # try:
    #     poller = client.begin_analyze_document(
    #         "prebuilt-layout",
    #         AnalyzeDocumentRequest(bytes_source=pdf_data),
    #         output_content_format=DocumentContentFormat.MARKDOWN
    #     )
    #     result_markdown: AnalyzeResult = poller.result()
    #     markdown_content = result_markdown.content
    # except Exception as e:
    #     raise Exception(f"Failed to extract Markdown content: {str(e)}")

    # try:
    #     poller = client.begin_analyze_document(
    #         "prebuilt-layout",
    #         AnalyzeDocumentRequest(bytes_source=pdf_data)
    #     )
    #     result_tables: AnalyzeResult = poller.result()
    # except Exception as e:
    #     raise Exception(f"Failed to extract table data: {str(e)}")
    
    ## 06.27 DI 한 번만 부르는 것으로 수정
    try:
        # 단일 API 호출로 마크다운과 표 데이터 추출
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            AnalyzeDocumentRequest(bytes_source=pdf_data),
            output_content_format=DocumentContentFormat.MARKDOWN
        )
        result: AnalyzeResult = poller.result()
        markdown_content = result.content  # 마크다운 콘텐츠
        tables = result.tables  # 표 데이터
    except Exception as e:
        raise Exception(f"Failed to extract document data: {str(e)}")


    table_replacements = []
    # 테이블 정보를 관리할 리스트 (tables가 없어도 빈 리스트로 초기화)
    tables_data = []
    
    # 결과 안에 tables 속성 체크
    if tables:
        with open(table_output_file, "w", encoding="utf-8") as f:
            f.write(f"Total Tables Detected: {tables}\n\n")
            logging.info(f"allegronx_chunker: Total Tables Detected: {len(tables)}")

            # 테이블 번호를 1번 부터 시작해서 반복
            for table_idx, table in enumerate(tables, 1):
                # 첫번째 셀을 가져와서 -> 위치 정보를 가져와서 -> 그 중, page 정보를 가져옴.
                page_num = table.cells[0].bounding_regions[0].page_number if table.cells else "Unknown"
                # 각 정보를 조합해서 table key 필드를 만들 것임.
                table_key = f"Table {table_idx} (Page {page_num}, Rows: {table.row_count}, Columns: {table.column_count})"
                logging.info(f"allegronx_chunker: {table_key}")

                # row, column 길이에 맞게 테이블 모양을 만드는 작업
                # 그리고 거기에 content를 하나씩 집어넣는다.
                # 셀마다 순회함. 
                table_data = [["" for _ in range(table.column_count)] for _ in range(table.row_count)]
                for cell in table.cells:
                    row_idx = cell.row_index
                    col_idx = cell.column_index
                    content = re.sub(r'[\n\r\t]+', ' ', cell.content or "").strip()
                    table_data[row_idx][col_idx] = content

                # beta (25.07.08) => column count 측정 :: DI 가 row_count를 잘못 감지하는 케이스 발견하여, 생성된 마크다운 기준으로 개수 파악
                # => 확인 결과 :: 기존 코드 써도 문제 없음. 결과는 동일함.
                markdown_data = format_table_to_markdown(table_data, table.column_count)
                col_cnt  = markdown_data.split('\n')[0].count('|') - 1

                # 테이블 정보 정의
                tables_data.append({
                    "key": table_key,
                    "page": page_num,
                    "page_range": [page_num],  # 페이지 범위 초기화
                    "rows": table.row_count,
                    # 25.07.08 backup // 문제 생기면 다시 돌려놓기.
                    # "columns": table.column_count,
                    "columns": col_cnt,
                    "data": table_data,
                    # 앞에서 생성한 데이터를 마크다운 형식으로 변환
                    # "markdown": format_table_to_markdown(table_data, table.column_count),
                    "markdown": markdown_data,
                    # 인덱스는 enumerate의 index를 따름.
                    "original_index": table_idx,
                    # 250620 필드 추가 (마크다운을 보고 생성형이 변환한 텍스트)
                    "llm_generate_data": ''
                })

            # (로그 확인) 테이블 총 개수, 테이블 내부 구조 확인
            logging.info(f"allegronx_chunker: 테이블 데이터 개수: {len(tables_data)}")
            logging.debug(f"allegronx_chunker: 테이블 데이터 샘플: {tables_data[:2]}")

            # 초기 <table> 섹션 교체 함수
            def replace_table(match, merged_indices=None):
                # 각 테이블에 대해 진행할 것인데, 예를 들어 첫번째 테이블이라면, 
                # match.start() 즉, 시작되는 첫번째 인덱스 번호이며,
                # markdown_content[:] 를 통해 슬라이싱 되어, 테이블 앞쪽 부분이 스캔되고
                # 거기서 <table> 이라는 태그가 몇 번 나오는 지 센다.
                # finditer는 match된 객체를 반환하기에 for로 요소를 받아 리스트로 만든 후, len으로 길이를 세었음.
                table_idx = len([m for m in re.finditer(r'<table>', markdown_content[:match.start()])]) + 1

                # 일단 보류.. 이 부분 동작 안 할듯..
                if merged_indices and table_idx in merged_indices and table_idx not in [t["original_index"] for t in table_replacements]:
                    logging.debug(f"allegronx_chunker: Removing <table> {table_idx} (merged into another table)")
                    return ""
                
                for table_info in table_replacements:
                    # 인덱스가 일치하는 것만 교체할 것임.
                    if table_info["original_index"] == table_idx:
                        logging.debug(f"allegronx_chunker: Replacing <table> {table_idx} with {table_info['key']}")
                        # table 태그를 마크다운으로 바꾼다.
                        return table_info["markdown"]
                logging.debug(f"allegronx_chunker: No replacement found for <table> {table_idx}, using original")
                
                return match.group(0)

            # 초기 교체
            table_replacements = tables_data.copy()
            # m 에 들어가는 것은 re.sub에서 찾은 table 임. 
            # lambda이기 떄문에 뽑힌 각 테이블에 대해 replace_table 함수를 적용함.
            # 정규표현식에서 .*? 만으로는 줄바꿈을 잡아낼 수 없기 떄문에 DOTALL을 사용함.
            # markdown_content는 마크다운으로 뽑은 텍스트 전체
            # --> 최종적으로 <table>로 감지된 부분이 replace_table 함수가 적용되면서 마크다운으로 교체됨.            
            content = re.sub(r'<table>.*?</table>', lambda m: replace_table(m, merged_indices=set()), markdown_content, flags=re.DOTALL)
    else:
        logging.info(f"allegronx_chunker: 테이블이 감지되지 않았습니다.")
        content = markdown_content

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"allegronx_chunker: Combined output saved to {output_file}")
        logging.info(f"allegronx_chunker: Table data saved to {table_output_file}")

        return content, tables_data
    except Exception as e:
        raise Exception(f"Failed to save output: {str(e)}")
    

 # Step 1-3.
def format_table_to_markdown(table_data, column_count):
    """테이블 데이터를 Markdown 형식으로 변환, 페이지 범위 추가"""
    formatted_table = []
    if table_data:
        header_row = table_data[0]
        formatted_table.append("| " + " | ".join(header_row) + " |")
        formatted_table.append("| " + " | ".join(["---"] * column_count) + " |")
        for row in table_data[1:]:
            formatted_row = "| " + " | ".join(cell for cell in row) + " |"
            formatted_table.append(formatted_row)

    return "\n".join(formatted_table)
    

 ########################## Part 2 ###########################
 # Step 2-1. 
 # 25.07.17 파일 이름 파라미터 추가
def batch_process_directory(md_files, md_file_name):
    '''
    md 디렉토리 밑의 모든 마크다운 문서에 대한 패시지 작업,
    빈 페이지 번호 추가 추출,
    엑셀 변환 작업을 진행하는 함수'''
    data = []
    # for filepath in md_files:
    #     if not os.path.exists(filepath):
    #         print(f"파일이 존재하지 않습니다: {filepath}")
    #         continue
    if md_files.endswith('.md'):
        data.extend(process_markdown_file(md_files))

    if not data:   
        logging.warning("allegronx_chunker: 처리할 .md 파일이 없습니다.")
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=["file_name", "1 depth", "2 depth", "3 depth", "4 depth", "content"])
    
    # apply로 페이지 번호와 마커 끝 여부 추출
    df[['pages', 'is_ended_with_marker', 'length']] = df['content'].apply(
        lambda x: pd.Series(extract_page_numbers(x))
    )

    # 페이지 번호 채우기
    last_valid_page = 0  # 직전 유효 페이지 번호 초기화
    current_file = None  # 현재 파일 추적
    for idx in range(len(df)):
        current_pages = df.at[idx, 'pages']
        is_ended_with_marker = df.at[idx, 'is_ended_with_marker']
        file_name = df.at[idx, 'file_name']

        # 파일이 바뀌었는지 확인
        if file_name != current_file:
            last_valid_page = 0  # 새 파일 시작 시 페이지 번호 초기화
            current_file = file_name

        if len(current_pages) == 0:  # 현재 패시지의 페이지 번호가 비어 있는 경우
            if idx == 0 or file_name != df.at[idx - 1, 'file_name']:  # 첫 번째 행 또는 새 파일의 첫 번째 패시지
                df.at[idx, 'pages'] = [1]  # 첫 패시지는 무조건 [1]
                last_valid_page = 1
            else:
                # 이전 패시지의 정보 확인
                prev_is_ended_with_marker = df.at[idx - 1, 'is_ended_with_marker']
                prev_pages = df.at[idx - 1, 'pages']
                prev_last_page = prev_pages[-1] if prev_pages else last_valid_page
                
                if prev_is_ended_with_marker:
                    # 경우 1: 이전 패시지가 마커로 끝났다면, 마지막 페이지 + 1
                    df.at[idx, 'pages'] = [prev_last_page + 1]
                else:
                    # 경우 2: 이전 패시지가 마커로 끝나지 않았다면, 마지막 페이지 유지
                    df.at[idx, 'pages'] = [prev_last_page]
                last_valid_page = df.at[idx, 'pages'][-1]
        else:
            # 페이지가 있는 경우
            if (idx == 0 or file_name != df.at[idx - 1, 'file_name']) and 1 not in current_pages:
                df.at[idx, 'pages'].insert(0, 1)  # 새 파일의 첫 행에 1 추가
            last_valid_page = current_pages[-1]  # 마지막 페이지 번호 업데이트

    df['content'] = df['content'].apply(lambda x: remove_page_markers(x))

 # 25.07.17 파일 이름 적용 수정
    # 중간 결과 저장 제거 (최종 결과만 저장)
    # df.to_excel(f"{BASE_DIR}/result/excel/{md_file_name}_Part2_Output_{timestamp}.xlsx", index=False, engine='openpyxl')
    return df


# Step 2-2.
def process_markdown_file(file_path):
    '''Dataframe 만들기 좋은 형태로 변환하는 함수'''
    with open(file_path, encoding='utf-8') as f:
        text = f.read()
    file_title = os.path.splitext(os.path.basename(file_path))[0]
    chunks = extract_chunks_from_text(text)
    return [(file_title, *chunk) for chunk in chunks]


# Step 2-3.
def extract_chunks_from_text(text):
    '''
    title 패턴 별로 나누는 함수 (4 Depth)
    패턴은 1. -> 1.1. -> 1.1.1. -> 1) 단계로 구성되어 있음
    '''
    chunks = []
    current_chunk = []
    current_pages = set([1])  # First page starts at 1
    parent_titles = {}  # Dictionary to store titles by depth: {1: 대제목, 2: 중제목, 3: 소제목, 4: 세제목}
    current_page = 1  # Track page number (default 1)

    # 넘버링 중, 불필요한 기호가 첨가된 넘버링을 변환 :: ex) 3\) -> # 3 으로 정제
    text = re.sub(r'(?m)^(\s*)(\d+)\\\)\s+(.*)', r'\1# \2) \3', text)
    lines = text.splitlines()
    cleaned_lines = []
    i = 0
    
    # 내용을 전체적으로 다시 클렌징 할 것임. (필요한 줄만 리스트에 담을 것.)
    while i < len(lines):
        line = lines[i].strip()
        # PageFooter, PageBreak, PageHeader는 버림 (아무 행동도 안함.)
        if line.startswith('<!-- PageFooter') or line.startswith('<!-- PageBreak') or line.startswith('<!-- PageHeader'):
            i += 1
            # 내가 탐색하는 줄이 빈 값이면, 그것도 pass
            while i < len(lines) and not lines[i].strip():
                i += 1
            continue
        # PageNumeber는 담아야 됨.
        if line.startswith('<!-- PageNumber'):
            cleaned_lines.append(lines[i])
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
        else:
            # 빈 줄이 아닌 줄은 추가. 기존에 축적된 cleaned_lines 도 참고.
            if line or not cleaned_lines or cleaned_lines[-1]:
                cleaned_lines.append(lines[i])
            i += 1

    lines = cleaned_lines

    for line in lines:
        # Find markdown titles with numbering (# 1., # 1.1., # 1.1.1., # 3))
        # 날짜/시간 형태는 제목으로 인식하지 않도록 개선된 정규식
        # 뒤에 사용하는 group()은 정규식에서 괄호로 묶인 부분을 추출한다.
        
        # 먼저 날짜/시간 패턴인지 확인
        date_time_pattern = re.match(r'^\s*#+\s+\d+\.\s*\d+\.\s*\d+\.\s*(오전|오후)\s*\d+:\d+', line)
        if date_time_pattern:
            # 날짜/시간 패턴이면 제목으로 인식하지 않고 일반 텍스트로 처리
            title_match = None
        else:
            # 일반적인 문서 번호 체계만 인식
            title_match = re.match(r'^\s*#+\s+(\d+(\.\d+)*\.?|\d+\s*\\?\))\s+(.*)', line)

        if title_match:
            # title_match가 되었다는 건 이전까지의 내용을 정리해서 올리고 새로운 청크를 준비해야 한다는 의미.
            logging.debug('allegronx_chunker: =====current chunk exists=====')
            # 이전에 쌓여있던 걸 하나로 뭉친다.
            content_text = '\n'.join(current_chunk).strip()
            logging.debug(f'allegronx_chunker: content_text: {content_text[:100]}...')
            logging.debug('allegronx_chunker: ============')
            # 위에서 뭉친 내용에 달라줄 라벨링 만드는 작업
            full_title = '\n'.join([parent_titles.get(i, '') for i in range(1, 5) if parent_titles.get(i)]).strip()
            logging.debug(f'allegronx_chunker: full_title: {full_title}')

            # if full_title:
            #     # 라벨링 있으면 뭉친 내용이랑 결합
            #     content_text = f"{full_title}\n{content_text}"

            # 그냥 공백만 있는 경우는 따로 추가 안할 것임.
            if re.sub(r'\s+', '', content_text) != '':
                content_text = f"{full_title}\n{content_text}"
            
                # 엑셀에 띄워줄 것이므로 순서에 맞게 넣어줌.
                chunks.append((
                    parent_titles.get(1, ''),  # 대제목
                    parent_titles.get(2, ''),  # 중제목
                    parent_titles.get(3, ''),  # 소제목
                    parent_titles.get(4, ''),  # 세제목
                    content_text,
                ))

            # 이제 내용 처리 다 했으니, 
            current_chunk = []

            # 넘버링과 그 제목 분리
            numbering = title_match.group(1).strip()
            title_text = title_match.group(3).strip()
            # 세분류 4) 같은 경우는 4 ) , 4\) 로도 나올 수 있어 4)로 일관성 있게 변환
            normalized_numbering = re.sub(r'\s*\\?\)', ')', numbering)

            # 추가하고자 하는 넘버링의 Depth를 정함.
            if normalized_numbering.endswith(')'):
                depth = 4  # 세제목 (e.g., 3))
                # 제목에 : 한 다음 주저리 내용이 붙어있는 경우, 분리시킴.
                if ':' in title_text:
                    content_text = title_text.split(':')[-1]
                    title_text = title_text.split(':')[0]
                    # 미리 내용의 첫 번째 부분에 넣어줌.
                    current_chunk.append(content_text)
            else:
                # 양끝에 혹시 모를 . 제거 후 1을 더한 값을 depth로 정의함.
                # 대제목 (1.), 중제목 (1.1.), 소제목 (1.1.1.)
                depth = normalized_numbering.strip('.').count('.') + 1  

            # 계층 딕셔너리에 갱신할 때 값에 해당하는 부분.
            single_title = f"{normalized_numbering} {title_text}".strip()
            logging.debug(f'allegronx_chunker: ===single title=== {single_title}')

            # 내가 추가하고자 하는 넘버링(depth)보다 작은 것만 남긴다.
            parent_titles = {k: v for k, v in parent_titles.items() if k < depth}
            # 갱신
            parent_titles[depth] = single_title

        else:
            # Add content
            if line.strip():
                current_chunk.append(line.strip())

    # Save last chunk
    if current_chunk:
        content_text = '\n'.join(current_chunk).strip()
        full_title = '\n'.join([parent_titles.get(i, '') for i in range(1, 5) if parent_titles.get(i)]).strip()
        if content_text and content_text != full_title:
            if full_title:
                content_text = f"{full_title}\n{content_text}"
            # page_str = ', '.join(str(p) for p in sorted(current_pages)) if current_pages else str(current_page)
            chunks.append((
                parent_titles.get(1, ''),
                parent_titles.get(2, ''),
                parent_titles.get(3, ''),
                parent_titles.get(4, ''),
                content_text,
                # page_str
            ))

    return chunks


# Step 2-4.
def extract_page_numbers(content):
    '''패시지의 페이지 추출 함수'''
    page_markers = re.findall(r'<!--\s*PageNumber="(\d+)\s*/\s*\d+"\s*-->', content)  # 모든 페이지 식별자 추출
    is_ended_with_marker = content.strip().endswith('" -->')  # 텍스트가 페이지 마커로 끝나는지 확인
    
    page_numbers = sorted(set(map(int, page_markers)))  # 중복 제거 후 정렬

    # 페이지 넘버링이 있는 경우
    if page_numbers:
        # Case A: 텍스트 시작이 페이지 마커로 시작하는 경우
        if content.strip().startswith('<!-- PageNumber='):
            # Case A-1: 마커가 여러 개 찍혀있는 경우
            if len(page_numbers) > 1:
                # Case A-1-1: 끝 쪽에 마커가 찍혀 있는 경우
                if is_ended_with_marker:
                    page_numbers.remove(page_numbers[0])
                # Case A-1-2: 끝 쪽에 마커가 없는 경우
                else:
                    page_numbers.append(page_numbers[-1] + 1)
                    page_numbers.remove(page_numbers[0])
            # Case A-2: 마커가 한 개 찍혀있는 경우
            else:
                page_numbers.append(page_numbers[-1] + 1)
                page_numbers.remove(page_numbers[0])
        # Case B: 텍스트 끝이 페이지 마커로 끝나는 경우
        elif is_ended_with_marker:
            pass
        # Case C: 텍스트 중간에 페이지 마커가 있는 경우
        else:
            page_numbers.append(page_numbers[-1] + 1)

    return page_numbers, is_ended_with_marker, len(content)  # 페이지 번호 리스트와 마커 끝 여부 반환


# Step 2-5.
def remove_page_markers(content):
    """콘텐츠에서 페이지 식별자를 제거하는 함수."""
    return re.sub(r'<!--\s*PageNumber="(\d+)\s*/\s*\d+"\s*-->', "", content).strip()


 ########################## Part 3 ###########################
 # Step 3-1.
  # 25.07.17 파일 이름 파라미터 추가
def merge_adjacent_table(df, tables_data, md_file_name):
    '''
    인접한 두 테이블을 병합하는 작업을 수행한다. 이 때 전제되는 필수조건인 '인접'의 개념은 다음과 같다.
    # '인접한다' : "Next Table"의 시작점에서 "Current Table"의 끝점의 차이가 0

    [수행조건]
    # 엑셀의 각 패시지마다 반영을 할 것임 (맨 바깥쪽 for문)
    # 하나의 패시지에서 Part 1에서 저장해놓은 테이블 딕셔너리에서 두 개를 잡아서 본다. (current, next table.)
    # 병합을 하려면 연속된 두 테이블이 모두 패시지에 위치해야 한다. 이 때 확인할 부분은 current의 끝부분과 next의 시작 부분이다.
    # find를 했을 때, 두 군데 모두 발견되어야 진행을 할 수 있다.
    # 페이지 간 인접성 체크를 진행할 것이며, 사이에 있는 마커와 모든 공백, 줄바꿈을 제거한 뒤 확인해야 한다.

    인접성이 확인되면 두 테이블을 병합하기 위한 조건을 살핀다. 
    # 붙이기 위한 조건
     a. Current Table의 Column 수 > Next Table의 Column 수
      -> PASS
     b. Current Table의 Column 수 == Next Table의 Column 수
      이 경우, 다음의 추가 조건 중 최소 1건을 만족해야 진행이 가능하다.
      b-1. Next Table의 첫 행의 셀들 중 하나라도 비어있을 때로 수정
      b-2. [Current Table의 Column 값] == [Next Table의 Column 값]
       -> 병합 진행
     c. Current Table의 Column 수 - Next Table의 Column 수 == 1:
      이 경우, Next Table에 padding을 준다.
     d. 나머지 조건은 일단 pass 하며, Current Table의 Column 수 - Next Table의 Column 수 > 1 인 경우, 차이만큼 Padding을 고려중이다.
       -> 아직 미반영.

    만약 병합 후, 병합된 테이블과 다음 테이블이 또 병합조건을 만족하는 경우, 연쇄 병합이 일어난다.
    '''
    # 연속 인접 테이블 병합
    merged_tables = tables_data.copy()  # 원본 데이터를 유지하기 위해 복사
    merged_indices = set()  # 병합으로 삭제된 테이블의 original_index 추적
    
    for idx, content in enumerate(df['content']):
        i = 0
        # 시작 인덱스 고정을 위한 플래그
        update_flag = False
        
        while i < len(tables_data): # merged_tables로 변경하여 동적 갱신 반영
            update_flag = False
            current_table = tables_data[i]
            while i + 1 < len(tables_data):
                next_table = tables_data[i + 1]
                
                # (로그) 
                if idx == 5 or idx == 10 or idx == 11 or idx == 16:
                    if i < 7:
                        logging.debug(f'allegronx_chunker: ===cur_nxt_tb={idx}행의-{i}번째 테이블==')
                        logging.debug(f'allegronx_chunker: ===현재 테이블===\n{current_table}')
                        logging.debug('allegronx_chunker: =======')
                        logging.debug(f'allegronx_chunker: ===다음 테이블===\n{next_table}')
                        logging.debug('allegronx_chunker: =======')

                        logging.debug(f'allegronx_chunker: content: {content[:200]}...')
                        logging.debug(f'allegronx_chunker: current_table markdown 찾기: {content.find(current_table["markdown"])}')
                        logging.debug(f'allegronx_chunker: next_table markdown 찾기: {content.find(next_table["markdown"])}')
                        logging.debug('allegronx_chunker: ========')

                # 내용에 테이블 인덱스 위치를 찾는다. 
                current_table_end = content.find(current_table["markdown"])
                
                # 설계 방향이 변경됨으로 내부 로직은 실제로 적용 안 될 것임.
                if current_table_end == -1:
                    table_tag_pattern = r'<table>.*?</table>'
                    table_tags = [m.start() for m in re.finditer(table_tag_pattern, content, re.DOTALL)]
                    if len(table_tags) >= current_table["original_index"]:
                        current_table_end = table_tags[current_table["original_index"]-1] + len(re.search(table_tag_pattern, content[table_tags[current_table["original_index"]-1]:]).group(0))
                else:
                    logging.debug(f'allegronx_chunker: ==마크다운 엑셀 데이터 {idx} 행의 테이블 번호 {i} 번째 찾았습니다.')
                    # 현재 마크다운 테이블의 마지막 인덱스를 알 수 있음.
                    current_table_end += len(current_table["markdown"])
                
                # 다음 테이블의 첫번째 인덱스를 찾는다.
                next_table_start = content.find(next_table["markdown"])

                # 설계 방향이 변경됨으로 내부 로직은 실제로 적용 안 될 것임.
                if next_table_start == -1:
                    table_tag_pattern = r'<table>.*?</table>'
                    table_tags = [m.start() for m in re.finditer(table_tag_pattern, content, re.DOTALL)]
                    if len(table_tags) >= next_table["original_index"]:
                        next_table_start = table_tags[next_table["original_index"]-1]
                
                # 로그 너무 많이 찍혀서 일단 주석처리함.
                if next_table_start == -1 or current_table_end == -1:
                    # print(f"Could not find table positions: current={current_table['key']} (end={current_table_end}), next={next_table['key']} (start={next_table_start})")
                    break
                
                # (로그)
                if idx == 5 or idx == 10 or idx == 11 or idx == 16:
                    if i < 7:
                        print('===직전 값 로그====')
                        print(current_table_end)
                        print('====')
                        print(next_table_start)
                        print('=====')
                        print(content)
                        print('======')
                        print(content[current_table_end:next_table_start])
                        print('====ddddd====')

                # 인접여부 확인
                if not is_adjacent_table(content, current_table_end, next_table_start):
                    break

                logging.info(f'allegronx_chunker: ===인접했습니다!!=== Between {current_table["key"]} and {next_table["key"]}')

                # 여기서 나오는 반환값은 관리하는 테이블 딕셔너리 (갱신된 상태) 또는 None
                merged_result = merge_tables(current_table, next_table)
                if merged_result:
                    logging.info(f'allegronx_chunker: =====if merged_result >> {idx}행의-{i}번째 테이블=======')
                    # 병합된 딕셔너리 테이블을 통으로 merged_tables에 갱신
                    merged_tables[i] = merged_result
                    current_table = merged_result

                    # log
                    if next_table["original_index"] == 5 or next_table["original_index"] == 6 or next_table["original_index"] == 7:
                        print('===merged_indics 조건 로그====')
                        print(next_table["original_index"], "\n", merged_result, idx, i )

                    # 다음 테이블은 삭제된 것으로 간주 (나중에 필터링 할 대상임.)
                    merged_indices.add(next_table["original_index"])

                    # 연속된 병합 처리 시, 최초 한 번만 수행하고 그 이후는 위치 정보를 fix해야 한다.
                    if update_flag == False:
                        current_table_start = content.find(tables_data[i]["markdown"])
                        update_flag = True

                    # 다음 테이블의 마지막 부분을 잡는다.
                    next_table_end = next_table_start + len(next_table["markdown"])
                    print('==병합 전 체크합니다!!=(현재, 다음)=', current_table_start, next_table_end)
                    if current_table_start != -1 and next_table_end != -1:
                        # 최종 결과 = 현재 테이블 직전 content + merged markdown + 다음 테이블 이후의 content
                        content = (
                            content[:current_table_start] +
                            merged_result["markdown"] +  # 병합된 markdown으로 갱신
                            content[next_table_end:]
                        )
                        
                        print('===병합 된 content===\n', content)
                        # 데이터프레임에 병합 내용 반영
                        df.at[idx, 'content'] = content
                        
                        print(f"Updated content with merged table: {merged_result['key']}")

                    else:
                        print(f"Warning: ≈t for merged table {merged_result['key']}")
                    # 다음 테이블 대상을 연속해서 탐지해야 함.
                    i += 1
                else:
                    break
            # 현재 테이블 대상을 연속해서 탐지해야 함.
            i += 1

    print("merged_indices:", merged_indices)
    # 병합으로 삭제된 테이블 제외하고 최종 merged_tables 생성
    filtered_tables = [table for table in merged_tables if table.get("original_index") not in merged_indices]
    
    # final_tables = filtered_tables
    print(f'====filtered_tables 수====={len(filtered_tables)}')
    print(filtered_tables)
  
    final_tables = []
    idx = 0

    while idx < len(filtered_tables):
        current = filtered_tables[idx]
        # 마지막 테이블이면 그냥 추가하고 종료
        if idx == len(filtered_tables) - 1:
            final_tables.append(current)
            break

        next_table = filtered_tables[idx + 1]

        # current의 page_range가 next_table의 page_range에 포함되면 current 제거
        # 그리고 이것은 병합된 테이블에 한해 적용.
        # 현재 페이지에 표가 있고 그 다음 표가 현재 페이지와 다음 페이지에 걸쳐서 나오는 경우 문제가 되기 때문에 체크한다.
        if set(current["page_range"]).issubset(set(next_table["page_range"])) and current.get("merged_indices") is not None:
        # if set(current["page_range"]).issubset(set(next_table["page_range"])):
            # current 생략, 다음 테이블로 넘어감 (i += 1만)
            idx += 1
        else:
            # 포함되지 않으면 current 유지
            final_tables.append(current)
            idx += 1


    print(f'====final_tables 수====={len(final_tables)}')
# 25.07.17 파일 이름 적용 수정
    # 중간 결과 저장 제거 (최종 결과만 저장)
    # df.to_excel(f'{BASE_DIR}/result/excel/{md_file_name}_Part3_Output_{timestamp}.xlsx')
    return df, final_tables


 # Step 3-2.
def is_adjacent_table(content, current_table_end_idx, next_table_start_idx) -> bool:
    """두 테이블이 인접한지 확인 (페이지 경계 마크다운 제거 및 공백/줄바꿈 무시)하는 함수"""
    page_boundary_pattern = r'<!-- PageNumber="[^"]*" -->'
    between_content = content[current_table_end_idx:next_table_start_idx]
    cleaned_content = re.sub(page_boundary_pattern, '', between_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'\s+', '', cleaned_content)
    # 앞의 전처리 이후 테이블 사이에 아무 것도 없다면(between_content의 length가 0) 표가 붙어있는 것임.
    print(f"Checking adjacency: Cleaned content length between tables: {len(cleaned_content)}")
    if len(cleaned_content) > 0:
        print(f"Non-empty content between tables: {between_content[:200]}...")
    
    return not cleaned_content


# Step 3-3.
def merge_tables(current_table, next_table):
    """두 테이블을 병합하는 함수"""
    current_cols = current_table['columns']
    next_cols = next_table['columns']
    current_data = current_table['data']
    next_data = next_table['data']

    # 다음 테이블의 컬럼 수가 1 적은 경우
    if next_cols == current_cols - 1:
        print(f"Merging tables: Padding 1 column for {next_table['key']} (Columns: {next_cols} -> {current_cols})")

        # 각 행마다 순회하며, 앞쪽에 패딩을 추가한다.
        padded_next_data = [[""] + row for row in next_data]
        merged_data = current_data + padded_next_data
        return {
            "key": f"{current_table['key']} + {next_table['key']}",  # 병합된 테이블의 키 갱신
            "page": current_table["page"], # page는 갱신 따로 안함.
            "page_range": list(set(current_table["page_range"] + next_table["page_range"])),  # 페이지 범위 통합
            "rows": len(merged_data), # 합쳐진 테이블의 행 길이
            "columns": current_cols, 
            "data": merged_data,
            "markdown": format_table_to_markdown(merged_data, current_cols),
            "original_index": current_table["original_index"],
            "merged_indices": current_table.get("merged_indices", {current_table["original_index"]}) | {next_table["original_index"]},
            "llm_generate_data": current_table.get("llm_generate_data", "")  # 기존 필드 유지
        }

    # 기존 조건
    if next_cols > current_cols:
        print(f"Skipping merge: Next table has more columns ({next_cols} > {current_cols})")
        return None

    elif next_cols == current_cols:
        # 내부 조건을 체크. title의 일치여부 / 첫번째 행 중 하나의 셀이라도 비어있을 경우
        current_title = current_data[0] if current_data else []
        next_title = next_data[0] if next_data else []
        titles_match = current_title == next_title
        next_first_row_has_empty_cell = any(not cell.strip() for cell in next_data[0]) if next_data and next_data[0] else True

        if titles_match or next_first_row_has_empty_cell:
            print(f"Merging tables: Titles match={titles_match}, First cell empty={next_first_row_has_empty_cell}")
            # title이 일치하면 다음 테이블의 두번째 행부터 합치고, 아니면 첫번째 행부터 합친다. 
            merged_data = current_data + (next_data[1:] if titles_match else next_data)

            return {
                "key": f"{current_table['key']} + {next_table['key']}",  # 병합된 테이블의 키 갱신
                "page": current_table["page"],
                "page_range": list(set(current_table["page_range"] + next_table["page_range"])),  # 페이지 범위 통합
                "rows": len(merged_data),
                "columns": current_cols,
                "data": merged_data,
                "markdown": format_table_to_markdown(merged_data, current_cols),
                "original_index": current_table["original_index"],
                "merged_indices": current_table.get("merged_indices", {current_table["original_index"]}) | {next_table["original_index"]},
                "llm_generate_data": current_table.get("llm_generate_data", "")  # 기존 필드 유지
            }
        else:
            print(f"Skipping merge: Titles match={titles_match}, First cell empty={next_first_row_has_empty_cell}")
            return None
    else:
        print(f"Skipping merge: Incompatible column counts ({next_cols} vs {current_cols})")
        return None


 ########################## Part 4 ###########################
 # Step 4.1
def parse_table_for_embedding(tables_data: List[Dict]) -> List[Dict]:
    '''
    임베딩 전용 포맷으로 변환하는 함수
    형태는 (Column 1) : (Value 1), (Column 2) : (Value 2)
    '''
    # 25.07.17 빈 칸 채우기를 예외 처리할 컬럼명 리스트 (공백 제거 후 비교)
    # Mandatory는 빈 공란에 selected 체크가 연속으로 찍히면 안됨.
    # Explanation은 하위 병합 셀이 있을 경우 해당 부분에 내용이 들어가면 안됨.
    fill_exclude_columns = {"Mandatory", "Explanation"}

    # 25.07.17 로직 변경 (for 영역)
    for element in tables_data:
        headers_raw = element["data"][0]
        headers = [data.replace(' ', '').strip() for data in headers_raw]
        rows = element["data"][1:]

        parsed_data = []
        prev_values = [""] * len(headers)

        for row in rows:
            row_filled = []
            for i, cell in enumerate(row):
                column_name = headers[i]
                cell_stripped = cell.strip()
                
                if cell_stripped == "":
                    if column_name in fill_exclude_columns:
                        row_filled.append("")  # 빈 칸 유지
                    else:
                        row_filled.append(prev_values[i])  # 이전 값으로 채우기
                else:
                    row_filled.append(cell_stripped)
                    prev_values[i] = cell_stripped  # 이전 값 갱신

            current_entry = {headers[i]: row_filled[i] for i in range(len(headers))}
            parsed_data.append(current_entry)

        def dict_to_sentence(data_dict: Dict[str, str]) -> str:
            return ", ".join(f"{k.strip()}: {v.strip()}" for k, v in data_dict.items())

        element['llm_generate_data'] = [dict_to_sentence(item) for item in parsed_data]

    return tables_data


 # Step 4.2
  # 25.07.17 파일 이름 파라미터 추가
def replace_markdown_with_llm_data(df, tables_data, md_file_name):
    """
    패시지의 마크다운 테이블을 llm_generate_data로 치환하는 함수.
    
    Parameters:
    - df: 패시지 데이터가 포함된 데이터프레임 (content 열 포함)
    - tables_data: 테이블 정보 딕셔너리 리스트
    
    Returns:
    - df: 갱신된 데이터프레임
    - updated_tables: 갱신된 테이블 데이터
    """
    updated_tables = tables_data.copy()  # 원본 데이터 복사

    for idx, original_content in enumerate(df['content']):
        content = original_content  # 처음은 원본에서 시작
        
        for i, table in enumerate(tables_data):
            # 마크다운 위치 탐색
            markdown_start = content.find(table["markdown"])
            
            if markdown_start == -1:
                print(f"Warning: Markdown for table {table['key']} not found in content at row {idx}")
                continue
            
            markdown_end = markdown_start + len(table["markdown"])
            
            # llm_generate_data를 문자열로 변환 (리스트를 줄바꿈으로 연결)
            llm_data_str = "\n".join(table["llm_generate_data"])
            
            # content에서 마크다운을 llm_generate_data로 치환
            content = (
                content[:markdown_start] +
                llm_data_str +
                content[markdown_end:]
            )

            if idx == 77 and i < 10:
                print(f'{idx}-{i} :: start index >> {markdown_start}')
                print(f'{idx}-{i} :: end index >> {markdown_end}')

                print('======')
                print(content)
                print('=====')
                print(llm_data_str)

        print(f"Replaced markdown with llm_generate_data for table {table['key']} at row {idx}")
        
            # 루프 종료 후, 최종 content를 df에 반영
        df.at[idx, 'content'] = content            
            # 테이블 데이터의 markdown도 llm_generate_data로 갱신 (필요 시)
            # updated_tables[i]["markdown"] = llm_data_str

    # 최종 치환된 content 길이 정보를 갱신함.
    df['length'] = df['content'].apply(len)
    # 중간 결과 저장 제거 (최종 결과만 저장)
    # df.to_excel(f'{BASE_DIR}/result/excel/{md_file_name}_Part4_Output_{timestamp}.xlsx')
    return df, updated_tables


 ########################## Part 5 ###########################
 # Step 5.1
 # 06.27 chunk_size를 받도록 수정
  # 25.07.17 파일 이름 파라미터 추가
def divide_large_passage(df, md_file_name, chunk_size=2000):
    '''추가 chunking 진행 함수'''
    # 데이터프레임에 함수 적용
    new_rows = []
    for i, row in df.iterrows():
        # 06.27 chunk_size를 받도록 수정
        split_rows = split_content(row, chunk_size)
        new_rows.extend(split_rows)

    # 결과 데이터프레임 생성
    result_df = pd.DataFrame(new_rows, columns=df.columns)
     # 25.07.17 파일 이름 적용 수정
    result_df.to_excel(f"{BASE_DIR}/docs/save_result/pdf_result/{md_file_name}_Part5_Output_{timestamp}.xlsx")

    return result_df


 # Step 5.2
 # 06.27 하드코딩 -> 변수인 chunk_size로 변경
def split_content(row, chunk_size):
    '''content를 줄 단위로 분할하는 함수'''
    if row['length'] <= chunk_size:
        # 06.27 추가 : 페이지 정보를 나중에 갱신할 것이므로 갱신 대상이 아님을 default로 설정
        row['is_split'] = False 
        return [row]
    else:
        # 여기 왔다는 건 쪼개야 할 패시지가 있다는 것. 일단 줄 단위로 쪼개봄
        lines = row['content'].split('\n')
        new_rows = []
        current_content = ""
        current_length = 0
        # 매뉴얼 특징 상 공통적으로 첫 페이지에 title을 제공하고 있지 않아 라벨링을 할 필요가 없음.
        # 첫 스텝을 거치고 나면 
        is_first_split = True
        
        for line in lines:
            line_length = len(line)
            # 각 라인별로 내가 정한 임계치에 다다를 때까지 합친다. 
            # !!!split 조건 수정 필요해보임!!!!
            if current_length + line_length > chunk_size:
                new_row = row.copy()
                new_row['content'] = add_depth_label({'1 depth': row['1 depth'], '2 depth': row['2 depth'], '3 depth': row['3 depth'], '4 depth': row['4 depth'], 'content': current_content.strip()}, is_split=True, is_second_split=not is_first_split)
                # 길이 갱신
                new_row['length'] = current_length
                # 06.27 추가 : 여기에 들어왔다는 건 행을 추가할 것이라는 의미로 True
                new_row['is_split'] = True

                new_rows.append(new_row)
                current_content = line + '\n'
                # 줄바꿈 추가했으니 길이를 1 추가한 건데 안해도 됨.
                current_length = line_length + 1
                is_first_split = False
            else:
                current_content += line + '\n'
                current_length += line_length + 1
        
        if current_content:
            new_row = row.copy()
            new_row['content'] = add_depth_label({'1 depth': row['1 depth'], '2 depth': row['2 depth'], '3 depth': row['3 depth'], '4 depth': row['4 depth'], 'content': current_content.strip()}, is_split=True, is_second_split=not is_first_split)
            new_row['length'] = current_length
            # 06.27 추가 : 여기에 들어왔다는 건 행을 추가할 것이라는 의미로 True
            new_row['is_split'] = True
            new_rows.append(new_row)
        
        return new_rows
    

 # Step 5.3
def add_depth_label(row, is_split=False, is_second_split=False):
    '''content에 depth 라벨링을 추가하는 함수'''
    if not is_split or not is_second_split:
        return row['content']
    depth_labels = []
    depth_cols = ['1 depth', '2 depth', '3 depth', '4 depth']
    # 빈 값이 없는 것들만 depth_labels에 새로 추가해서 나중에 join 시킨 결과가 라벨링 값임
    for col in depth_cols:
        if pd.notna(row[col]) and row[col] != "":
            depth_labels.append(f"{row[col]}")
    
    # 라벨링 값 join + 잘려진 내용
    return "\n".join(depth_labels) + "\n" + row['content'] if depth_labels else row['content']
