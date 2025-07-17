# 여기서 작업 진행함!! 07.08.
from datetime import datetime
from ast import literal_eval
from dotenv import load_dotenv

import requests
import os
import pandas as pd
import yaml
import json



load_dotenv()
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# 문서 기반 질문 생성
def generate_questions_from_documents(definitions: str, flows: str, project_id: str) -> dict:

    try:
        print("🚀 문서 기반 질문 생성 시작...")
        
        # 1. Azure 설정 초기화
        print(f"⚙️ Azure 설정 초기화 중... (프로젝트: {project_id})")
        initialize_azure_config(project_id)


        # 3. 텍스트를 기반으로 질문 생성
        print("🤖 Azure OpenAI로 질문 생성 중...")
        questions = create_synthesis_questions(definitions, flows)

        if not questions:
            raise ValueError("질문 생성에 실패했습니다. 빈 결과를 받았습니다.")

        print(f"✅ {len(questions)}개의 질문 생성 완료")

        # 4. 질문을 Excel 파일로 저장
        print("💾 Excel 파일로 저장 중...")
        result = save_questions_to_excel(questions)
        
        if not result:
            raise ValueError("파일 저장에 실패했습니다.")
        
        print("🎉 질문 생성 프로세스 완료!")
        return result

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        print(f"An error occurred in generate_questions_from_documents: {e}", exc_info=True)
        return None

# --- Azure OpenAI 및 DI 환경 변수 설정 ---
def get_azure_config(project_id):

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
        raise ValueError(f"Invalid project_id: {project_id}. Use 'Public', 'Corporate', or 'CLT'")
    
    if not all(config.values()):
        raise ValueError(f"Azure config values for project_id '{project_id}' are not fully set in .env file.")
        
    return config

def initialize_azure_config(project_id):
    """전역 Azure 설정을 초기화합니다."""
    global azure_config
    azure_config = get_azure_config(project_id)
    print(f"Azure config initialized for project_id: {project_id}")


# Azure OpenAI를 호출 > 응답
def get_completion_from_messages(messages, temperature=0.5):

    payload = {
        "temperature": temperature,
        "messages": messages
    }
    r = requests.post(
        f"{azure_config['endpoint']}/openai/deployments/{azure_config['deployment']}/chat/completions",
        json=payload,
        headers={'Content-Type': 'application/json', 'api-key': azure_config["key"]},
        params={'api-version': azure_config["api_version"]}
    )
    r.raise_for_status()  # HTTP 오류 발생 시 예외 발생
    response_json = r.json()
    return response_json['choices'][0]['message']['content']


def create_synthesis_questions(definitions: str, flows: str) -> list:

    # YAML에서 템플릿 문자열 불러오기
    def load_prompt_template(yaml_path: str) -> str:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
        return yaml_data['prompt_template']
    
    prompt_raw = load_prompt_template(f"{BASE_DIR}/function/prompt/generate_question_prompt.yaml")
    prompt_template = prompt_raw.format(definitions=definitions, flows=flows)

    messages = [{'role': 'user', 'content': prompt_template}]
    
    raw_response = get_completion_from_messages(messages)
    
    try:
        # 응답에서 ```json과 ``` 제거
        cleaned_response = raw_response.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response[7:].strip()
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3].strip()
        
        # JSON 파싱
        question_list = json.loads(cleaned_response)
        
        if isinstance(question_list, list) and len(question_list) > 0:
            return question_list
        else:
            print("LLM response was not a valid list. Returning raw response as a single-item list.")
            return [cleaned_response]
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Failed to parse LLM response into a list: {raw_response}. Error: {e}")
        return [raw_response]


# 질문 리스트를 Excel 파일로 저장
def save_questions_to_excel(questions: list) -> dict:
    try:
        # questions가 리스트이고 각 항목이 dict인지 확인
        if not isinstance(questions, list) or not all(isinstance(q, dict) for q in questions):
            print("Questions is not a list of dictionaries. Saving raw data.")
            df = pd.DataFrame({"Generated_Questions": questions})
        else:
            # 필드별로 분리하여 DataFrame 생성
            df = pd.DataFrame(questions, columns=["Question", "Answer", "type", "reference"])
        
        directory_path = f'{BASE_DIR}/result/final_result'
        os.makedirs(directory_path, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f'generate_query_list_{timestamp}.xlsx'
        full_path = os.path.join(directory_path, file_name)

        df.to_excel(full_path, index=False)
        print(f"Successfully saved questions to {full_path}")

        return {'file_name': file_name}
    except Exception as e:
        print(f"Error in save_questions_to_excel: {e}")
        return None

