import os
import openai
import requests
import pandas as pd
import json
import random
from ast import literal_eval




# 환경 변수 설정
def get_azure_config(project_id):
    print(f"Getting Azure config for project_id: {project_id}")
    if project_id == "Public":
        config = {
            "key": os.getenv("Public_AZURE_OPENAI_KEY"),
            "endpoint": os.getenv("Public_AZURE_OPENAI_ENDPOINT"),
            "deployment": os.getenv("Public_DEPLOYMENT_CHAT"),
            "api_version": os.getenv("Public_AZURE_OPENAI_API_VERSION")
        }
    elif project_id == "Corporate":
        config = {
            "key": os.getenv("Corporate_AZURE_OPENAI_KEY"),
            "endpoint": os.getenv("Corporate_AZURE_OPENAI_ENDPOINT"),
            "deployment": os.getenv("Corporate_DEPLOYMENT_CHAT"),
            "api_version": os.getenv("Corporate_AZURE_OPENAI_API_VERSION")
        }
    elif project_id == "CLT":
        config = {
            "key": os.getenv("AZURE_OPENAI_API_KEY"),
            "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "deployment": os.getenv("DEPLOYMENT_CHAT"),
            "api_version": os.getenv("AZURE_OPENAI_API_VERSION")
        }
    else:
        raise ValueError("Invalid project_id. Use 'Public' or 'Corporate'")
    
    print(f"Retrieved config: {config}")
    return config


def initialize_azure_config(project_id):
    print(f"Initializing Azure config for project_id: {project_id}")
    global azure_config, AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT_CHAT, OPENAI_HEADERS, OPENAI_PARAMS
    
    azure_config = get_azure_config(project_id)
    print(f"Azure config set to: {azure_config}")
    
    AZURE_OPENAI_KEY = azure_config["key"]
    AZURE_OPENAI_ENDPOINT = azure_config["endpoint"]
    AZURE_OPENAI_API_VERSION = azure_config["api_version"]
    AZURE_OPENAI_DEPLOYMENT_CHAT = azure_config["deployment"]
    OPENAI_HEADERS = {'Content-Type': 'application/json','api-key': AZURE_OPENAI_KEY}
    OPENAI_PARAMS = {'api-version': AZURE_OPENAI_API_VERSION}
    
    print(f"Global variables set:")
    print(f"AZURE_OPENAI_KEY: {AZURE_OPENAI_KEY[:5]}...")
    print(f"AZURE_OPENAI_ENDPOINT: {AZURE_OPENAI_ENDPOINT}")
    print(f"AZURE_OPENAI_API_VERSION: {AZURE_OPENAI_API_VERSION}")
    print(f"AZURE_OPENAI_DEPLOYMENT_CHAT: {AZURE_OPENAI_DEPLOYMENT_CHAT}")
    
    openai.api_type = "azure"
    openai.api_base = AZURE_OPENAI_ENDPOINT
    openai.api_version = AZURE_OPENAI_API_VERSION
    openai.api_key = AZURE_OPENAI_KEY

# 토큰 계산
import tiktoken

def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("gpt-4")
    num_tokens = len(encoding.encode(string))
    return num_tokens

def num_tokens_from_messages(messages):
    """Returns the number of tokens used by a list of messages."""
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += num_tokens_from_string(value)
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens


# Input data Json 형식 변환 쿼리
def Save_data(field_business, user_type, df, edf, Constraints):
    try:
        print("=== Save_data 함수 시작 ===")
        # QA 엑셀 파일 JSON 형식 변환 시작
        data_payloads = {
            'value' : []
        }

        for i in range(len(df)) :
            data = {
                'Num' : i,
                'Answer' : df.loc[i]['Answer'],
                'Question' : df.loc[i]['Question']
            }
            data_payloads['value'].append(data)

        Jdata = json.dumps(data_payloads, indent=4, ensure_ascii=False)
        print("QA data converted to JSON")

        # Entity 사전 데이터 형식 변환 시작
        edata_payloads = {
            'value' : []
        }
        index = []
        entry = []
        synonym = []
        for x in range(len(edf)) :
            index.append(x)
            entry.append(edf.loc[x]['Entry'])
            synonym.append(edf.loc[x]['Synonym'])
        
        edata = {
                'index' : index,
                'Entry' : entry,
                'Synonym' : synonym
            }
        
        idf = pd.DataFrame(edata)
        mdata = {}

        for Entry, group in idf.groupby('Entry') :
            mdata[Entry] = group['Synonym'].unique().tolist()

        edata_payloads['value'].append(mdata)

        EJdata = json.dumps(edata_payloads, indent=4, ensure_ascii=False)
        print("Entity data converted to JSON")

        print("Calling Read_json...")
        result = Read_json(field_business, user_type, Jdata, EJdata, Constraints)
        print(f"Read_json returned: {result}")
        
        if result is None:
            print("Error: Read_json returned None")
            return None
            
        print(f"Save_data returning: {result}")
        print("=== Save_data 함수 종료 ===")
        return result
    except Exception as e:
        print(f"Error in Save_data: {e}")
        logging.error(f"sentence_generator.py: Error in Save_data: {e}")
        return None




# 파일 데이터 읽기 및 유형별 프롬프트 호출
def Read_json(field_business, user_type, Jdata, EJdata, Constraints):
    try:
        print("=== Read_json 함수 시작 ===")
        field_business = field_business
        user_type = user_type
        d_data = json.loads(Jdata)
        Ed_data = json.loads(EJdata)

        main_sent = conversational_retrieval(field_business, user_type, d_data, Constraints)
        contraction_sent = conversational_summary(main_sent)
        nounform_sent = conversational_exchange(d_data)
        synonym_sent = conversational_synonym(main_sent, Ed_data)
        print("Starting storage...")
        storage_center = storage(d_data, main_sent, contraction_sent, nounform_sent, synonym_sent)
        
        print(f"Read_json returning: {storage_center}")
        print("=== Read_json 함수 종료 ===")
        return storage_center
    except Exception as e:
        print(f"Error in Read_json: {e}")
        logging.error(f"sentence_generator.py: Error in Read_json: {e}")
        return None



# 동의어 확장 prompt
def conversational_synonym(main_sent,Ed_data):

    conv_result_list = []

    for i in range(len(main_sent)) :
        result = literal_eval(main_sent[i])

        prompt_template = f''' {result} 질문들을 구성하고 있는 단어들 중 {Ed_data}에 포함되어 있는 단어를 분석한 뒤, 해당 단어를 같은 레벨에 존재하는 다른 단어로 치환하여 문장을 구성하세요.

        ## 힌트 ##
        문장에 구성되어 있는 단어 1: '자가용', '드라이브', '빙판길' ...
        문장에 구성되어 있는 단어와 같은 레벨의 단어 1: '자가용' = '자동차', '드라이브' = '운전', '빙판길' = '얼음길' ...

        문장에 구성되어 있는 단어 2: '자이로드롭', '놀이기구', '티켓', '비용'
        문장에 구성되어 있는 단어와 같은 레벨의 단어 2: '자이로드롭' = '자이로 드롭', '놀이기구' = '어트렉션'|'어트랙션', '티켓' = '티캣'|'표', '비용' = '요금' ...

        ## 예시 ##
        basic question 1: 친구 자가용으로 드라이브 중인데, 빙판길 때문에 너무 위험할 때는 어떻게 하나요?
        question 1: 친구 자동차로 운전 중인데, 얼음길 때문에 너무 위험할 때는 어떻게 하나요?
        
        basic question 2: 자이로드롭 놀이기구 티켓 비용이 어떻게 되나요?
        question 2: 자이로 드롭 어트렉션 표 요금이 어떻게 되나요?
        ...
        ## /예시 ##

        
        새로운 단어로 치환하여 구성한 문장들은 원래 문장과 형태는 똑같고, 단어만 치환되어야 합니다. 만약, 동의어로 치환할 단어가 없다고 판단될 경우, 당신은 자유롭게 뜻이 일치하는 다른 단어로 치환하여도 무관합니다.

        답변 형식은 리스트([])로 출력해주세요.
        답변 형식 :
        ["Question 1","Question 2","Question 3",..,"Question 10"]

        답변 :

        '''
    
        prompt = [{'role':'user', 'content':prompt_template}]
    
        tokens = num_tokens_from_messages(prompt)

        if tokens > 16000:
            return f"답변 가능한 최대 메시지 길이는 16000토큰 입니다. 메시지에 {tokens}개의 토큰이 사용되었습니다. 메시지 길이를 줄여주세요."
        else :
            conv_result_list.append(get_completion_from_messages(prompt))
    return conv_result_list



# 문장 간결화 prompt
def conversational_summary(main_sent):
    
    conv_result_list = []
    logging.info(f'sentence_generator.py: main_sent: {main_sent}')
    for i in range(len(main_sent)):
        result = literal_eval(main_sent[i])

        prompt_template = f''' {result} 각 질문의 핵심을 간결하게 요약하되, 다채롭고 다양한 표현을 사용하여 문장 끝이 반복되지 않도록 해주세요. 예를 들면, 어말어미를 다양하게 활용하는 것을 말합니다. 어말어미는 문장의 맥락과 문체, 화자의 태도 등을 반영하는 것을 말합니다.

            ## 예시 ##
            before 1: 2시간 뒤에 강남에서 친구 만나기로 했는데, 맛있는 한정식집 추천해줄 수 있나요?
            after 1: 맛있는 강남 한정식집 추천해줄 수 있나요?
            before 2: 2시간 뒤에 강남에서 친구 만나기로 했는데, 맛있는 한정식집 추천해줄 수 있나요?
            after 2: 강남 맛있는 한정식집 알고싶어
            before 3: 2시간 뒤에 강남에서 친구 만나기로 했는데, 맛있는 한정식집 추천해줄 수 있나요?
            after 3: 한정식 맛집 강남 위치로 추천 부탁드려요
            before 4: 2시간 뒤에 강남에서 친구 만나기로 했는데, 맛있는 한정식집 추천해줄 수 있나요?
            after 4: 친구와 강남에 갈만한 한정식집 알려줘
            before 5: 2시간 뒤에 강남에서 친구 만나기로 했는데, 맛있는 한정식집 추천해줄 수 있나요?
            after 5: 강남역 주변 유명한 한식가게 있을까요? 
            ...
            ## /예시 ##

            각 질문의 요약에는 다른 동사, 어미, 또는 문장 구조를 사용하여 문장의 다양성을 높여주세요. 단, 핵심 단어는 반드시 포함하되 문장 앞, 중간 또는 뒤에 문맥에 맞게 배치하여 구성합니다.

            답변 형식은 리스트([])로 출력해주세요.
            답변 형식 :
            ["Question1","Question2","Question3",..,"Question 10"]

            답변: 
            '''
    
        prompt = [{'role':'user', 'content':prompt_template}]
    
        tokens = num_tokens_from_messages(prompt)

        if tokens > 16000:
            return f"답변 가능한 최대 메시지 길이는 16000토큰 입니다. 메시지에 {tokens}개의 토큰이 사용되었습니다. 메시지 길이를 줄여주세요."
        else :
            conv_result_list.append(get_completion_from_messages(prompt))

    return conv_result_list



# 복합문장10, 단일문장10, 명사형10, 동의어파생10
# QA 적용 prompt(Main Sentence)
def conversational_retrieval(field_business, user_type, d_data, Constraints):
    
    prom = []
    for val in d_data['value'] :
        work = val['Question']
        definition = val['Answer']
        print(work)
        print(definition)
        
        prompt_template = f'''
            purpose="{field_business}"
            user="{user_type}"
            work="{work}"
            definition="{definition}"

            # Task:
            - work에 대한 definition을 바탕으로 업무 관련 문장 10개를 생성해야 합니다.
            - 이 중, 5개는 간결하게, 5개는 구체적인 상황을 포함하여 작성해야 합니다.
            ※ 복합적인 의도가 담긴 문장 생성 X
            - 아래 예시들을 참고하여 작성해 주세요.

            # Output:
            - 무조건 해당 리스트 형식으로 출력하세요. ["문장1","문장2",..,"문장10"]

            # 예시1
            work: "노루컴퓨터 문의"
            user: "컴퓨터 사용자"
            question: "컴퓨터 수리 신청 방법"
            definition: "컴퓨터 A/S 신청은 제조사 고객센터나 공식 홈페이지를 통해 가능합니다. 증상을 간단히 정리해두시면 접수에 도움이 됩니다."
            output: ["컴퓨터 수리 맡기려고요","컴퓨터 A/S 신청 안내","노트북 A/S 신청 방법 알려줘","PC 수리 신청할래","컴퓨터 수리 접수 문의","컴퓨터 수리 어디서 신청해","컴퓨터 고장나서 A/S 신청하려는데 어떻게 하나요","노트북이 안 켜지는데 어디 가서 수리해야 돼","인터넷으로 컴퓨터 A/S 접수 되나요","PC 고장 수리 접수 지금 바로 가능한가요"]

            # 예시2
            work: "건강검진 관련 안내"
            user: "건강검진을 받으려는 국민"
            question: "건강검진 예약 문의"
            definition: "건강검진 예약은 병원 홈페이지나 전화로 가능합니다. 원하시는 날짜를 선택한 뒤, 기본 정보를 입력하면 완료됩니다. 종합검진은 사전 상담이 필요할 수 있습니다."
            output: ["건강검진 예약 방법 알려줘","건강검진 예약 관련 안내","병원 검진 예약 되나요","검진 예약 가능한가요","건강검진 병원 예약 문의","건강검진 예약 어디서 하나요","검진 어떻게 예약하는 건가요","종합검진 전화로 바로 예약할 수 있나요","건강검진 예약할 때 필요한 정보가 뭔가요","병원 홈페이지에서 온라인으로 건강검진 예약 가능해"]

            # 예시3
            work: "메디택배 관련 문의"
            user: "메디택배를 이용하는 대한민국 국민"
            question: "택배 배송 조회 문의"
            definition: "택배 배송 조회는 메디택배 어플에서 운송장 번호 입력 후 조회 버튼을 누르면 현재 위치와 도착 예정일을 확인할 수 있습니다. 일부 배송은 지연될 수 있으니 참고 바랍니다."
            output: ["택배 배송 조회하려고요","택배 위치 확인 가능해","택배 배송 중 확인 방법","택배 물건 배송 중인가요","택배 배송 상태 알려주세요","운송장 없이 택배 배송 조회 되나요","택배 배송 조회 어떻게 하나요","현재 택배 배송 상태를 조회하려는데 어디서 하는 건가요","택배 잘 배송되고 있는건지 확인 부탁드려요","택배 배송 지연되는 것도 조회 가능한가요"]

            # 제약조건(절대로 이런 케이스로는 질문을 만들지 마세요)
            {Constraints}

        '''

        prompt = [{'role':'user', 'content':prompt_template}]
    
        tokens = num_tokens_from_messages(prompt)

        if tokens > 16000:
            return f"답변 가능한 최대 메시지 길이는 16000토큰 입니다. 메시지에 {tokens}개의 토큰이 사용되었습니다. 메시지 길이를 줄여주세요."
        else :
            print(tokens)
            prom.append(get_completion_from_messages(prompt))
    return prom


# 문장 명사화 prompt
def conversational_exchange(d_data):
    
    conv_result_list = []
 
    for i in range(len(d_data['value'])) :
        result = d_data['value'][i]

        prompt_template = f''' {result} 답변의 깊은 이해를 바탕으로, 핵심 단어를 찾은 뒤 명사(noun)로 끝나는 문장을 만들어주세요. 이 때, 핵심 단어는 반드시 포함하되 문장 앞, 중간 또는 뒤에 자유롭게 배치하여 만든 문장들의 패턴이 다양해지도록 구성하세요.

        ## 예시 ##
        * 핵심 단어 : '강남', '한정식집'
        Answer: 서울 강남에 존재하는 맛있는 한정식집에 대해서 안내해 드릴게요. 1. 다같이 사랑방 / 위치 : 서울 강남구 ... \n2. 강남면옥 / 위치 : 서울 강남구 ...
        question 1: 맛있는 강남 한정식집 추천
        question 2: 강남 맛있는 한정식집 추천
        question 3: 강남 한정식 맛집 위치 
        question 4: 한정식 추천 맛집 장소
        question 5: 강남역 주변 맛있는 한정식집
        ...
        question 10 : 추천할만한 강남역 근처 한식 맛집
        ## /예시 ##

        각 질문은 문장 구조를 다르게하여 위 예시처럼 문장의 다양성을 높여주세요. 다시 한번 더 말하지만, 핵심 단어는 반드시 포함하되 문장 앞, 중간 또는 뒤에 자유롭게 배치하여 만든 문장들의 패턴이 다양해지도록 구성하고, 반드시 문장의 끝은 어말어미를 붙여서 끝나는 것이 아닌, 예시 'question'처럼 명사(noun)로만 끝나야 합니다 명심하세요.

        답변 형식은 리스트([])로 출력해주세요.
        답변 형식 :
        ["Question1","Question2","Question3",..,"Question10"]

        답변 :

        '''
    
        prompt = [{'role':'user', 'content':prompt_template}]
    
        tokens = num_tokens_from_messages(prompt)
        print(tokens)
        if tokens > 16000:
            return f"답변 가능한 최대 메시지 길이는 16000토큰 입니다. 메시지에 {tokens}개의 토큰이 사용되었습니다. 메시지 길이를 줄여주세요."
        else :
            conv_result_list.append(get_completion_from_messages(prompt))
    return conv_result_list



# GPT 결과 출력
def get_completion_from_messages(messages, deployment=None, temperature=0):
    if deployment is None:
        if 'azure_config' not in globals():
            raise ValueError("Azure configuration not initialized. Call initialize_azure_config first.")
        deployment = azure_config["deployment"]
    
    payloads = {
        "temperature" : temperature,
        "messages" : messages
    }
    r = requests.post(azure_config["endpoint"] + "/openai/deployments/" + deployment + "/chat/completions",
                    json=payloads, 
                    headers={'Content-Type': 'application/json', 'api-key': azure_config["key"]}, 
                    params={'api-version': azure_config["api_version"]})
    
    Result = r.json()['choices'][0]['message']['content']

    return Result



# data storage
def storage(d_data, main_sent, contraction_sent, nounform_sent, synonym_sent):
    try:
        print("=== storage 함수 시작 ===")
        final_result = []
        for i in range(len(d_data['value'])):
            question = d_data['value'][i]
            parser_main_sent = main_sent[i]
            parser_contraction_sent = contraction_sent[i]
            parser_nounform_sent = nounform_sent[i]
            parser_synonym_sent = synonym_sent[i]
            auto_sentence = {
                'index' : i,
                'question' : str(question),
                'main_sent' : str(parser_main_sent),
                'contraction_sent' : str(parser_contraction_sent),
                'nounform_sent' : str(parser_nounform_sent),
                'synonym_sent' : str(parser_synonym_sent)
            }
            final_result.append(auto_sentence)

        df = pd.DataFrame(final_result)

        directory_path = os.path.join(os.getcwd(), 'docs', 'save_result', 'sentence')
        print(f"현재 작업 디렉토리: {os.getcwd()}")
        print(f"파일 저장 디렉토리: {directory_path}")

        if not os.path.exists(directory_path):
            print(f"디렉토리 생성 시도: {directory_path}")
            os.makedirs(directory_path)
            print(f"디렉토리 생성 완료: {directory_path}")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f'Result_Sentence_{timestamp}.xlsx'
        full_path = os.path.join(directory_path, file_name)
        print(f"파일 저장 경로: {full_path}")

        df.to_excel(full_path)
        print(f"파일 저장 완료: {file_name}")

        result = {
            'file_name': file_name
        }
        print(f"storage 함수 반환값: {result}")
        print("=== storage 함수 종료 ===")
        return result
    except Exception as e:
        print(f"Error in storage function: {e}")
        logging.error(f"sentence_generator.py: Error in storage function: {e}")
        return None
