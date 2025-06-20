import os
import openai
import requests
import pandas as pd
import json
from dotenv import load_dotenv
from datetime import datetime
import logging
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from ast import literal_eval

# .env 파일 로드
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# --- Azure OpenAI 및 DI 환경 변수 설정 ---

def get_azure_config(project_id):
    """프로젝트 ID에 따라 Azure OpenAI 설정을 가져옵니다."""
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
    logging.info(f"Azure config initialized for project_id: {project_id}")

def extract_text_from_pdf(file_path: str) -> str:
    """Azure Document Intelligence를 사용해 PDF에서 텍스트를 추출합니다."""
    try:
        endpoint = os.getenv("AZURE_DI_ENDPOINT")
        key = os.getenv("AZURE_DI_KEY")
        if not endpoint or not key:
            raise ValueError("AZURE_DI_ENDPOINT and AZURE_DI_KEY must be set in .env file.")
        
        client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

        with open(file_path, "rb") as f:
            poller = client.begin_analyze_document("prebuilt-document", f)
            result = poller.result()
        
        logging.info(f"Successfully extracted text from {os.path.basename(file_path)}.")
        return result.content
    except Exception as e:
        logging.error(f"Error extracting text from PDF {file_path}: {e}")
        raise

def get_completion_from_messages(messages, temperature=0.5):
    """Azure OpenAI를 호출하여 응답을 받습니다."""
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

def create_synthesis_questions(text1: str, text2: str) -> list:
    """두 문서 내용을 기반으로 10개의 종합 질문을 생성합니다."""
    text1_snippet = text1[:4000]
    text2_snippet = text2[:4000]

    prompt_template = f'''
# 첫 번째 문서 (일부):
{text1_snippet}
---
# 두 번째 문서 (일부):
{text2_snippet}

# 지시사항:
- 위 두 문서의 내용을 종합적으로 분석하여, 사용자가 두 문서를 모두 깊이 이해했는지 확인할 수 있는 **질문 10개**를 생성해주세요.
- 질문은 두 문서를 비교/대조하거나, 한 문서의 개념을 다른 문서의 사례에 적용하는 등 종합적인 사고를 요구해야 합니다.
- 질문은 구체적이고 명확해야 합니다.

# 출력 형식:
- 반드시 Python 리스트 형식으로만 반환해주세요.
- 예시: ["문서 1의 A와 문서 2의 B는 어떤 차이점이 있나요?", "문서 2의 사례를 문서 1의 이론에 적용하면 어떻게 설명할 수 있나요?"]
'''
    messages = [{'role': 'user', 'content': prompt_template}]
    
    raw_response = get_completion_from_messages(messages)
    
    try:
        question_list = literal_eval(raw_response)
        if isinstance(question_list, list) and len(question_list) > 0:
            return question_list
        else:
            logging.warning("LLM response was not a valid list. Returning raw response as a single-item list.")
            return [raw_response]
    except (ValueError, SyntaxError) as e:
        logging.error(f"Failed to parse LLM response into a list: {raw_response}. Error: {e}")
        return [raw_response]

def save_questions_to_excel(questions: list) -> dict:
    """질문 리스트를 Excel 파일로 저장하고 파일명을 반환합니다."""
    try:
        df = pd.DataFrame(questions, columns=["Generated_Questions"])
        
        directory_path = os.path.join(os.getcwd(), 'docs', 'save_result', 'pdf_questions')
        os.makedirs(directory_path, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f'Generated_PDF_Questions_{timestamp}.xlsx'
        full_path = os.path.join(directory_path, file_name)

        df.to_excel(full_path, index=False)
        logging.info(f"Successfully saved questions to {full_path}")

        return {'file_name': file_name}
    except Exception as e:
        logging.error(f"Error in save_questions_to_excel: {e}")
        return None

def generate_questions_from_documents(pdf_path1: str, pdf_path2: str, project_id: str) -> dict:
    """두 PDF 파일로부터 질문을 생성하고 파일로 저장하는 메인 함수"""
    try:
        logging.info("Starting question generation from PDF documents.")
        
        # 1. Azure 설정 초기화
        initialize_azure_config(project_id)

        # 2. 두 PDF에서 텍스트 추출
        text1 = extract_text_from_pdf(pdf_path1)
        text2 = extract_text_from_pdf(pdf_path2)

        # 3. 텍스트를 기반으로 질문 생성
        questions = create_synthesis_questions(text1, text2)

        if not questions:
            raise ValueError("Question generation failed, received no questions.")

        # 4. 질문을 Excel 파일로 저장
        result = save_questions_to_excel(questions)
        
        logging.info("Question generation process completed successfully.")
        return result

    except Exception as e:
        logging.error(f"An error occurred in generate_questions_from_documents: {e}", exc_info=True)
        return None

if __name__ == '__main__':
    # 테스트용 코드
    # 이 스크립트를 직접 실행하려면, 아래 경로에 테스트용 PDF 파일을 위치시키세요.
    # 예: sub_lang/docs/test_doc1.pdf, sub_lang/docs/test_doc2.pdf
    
    logging.basicConfig(level=logging.INFO)
    
    # PDF 파일 경로 (실제 파일 경로로 수정 필요)
    test_pdf1 = os.path.join(os.path.dirname(__file__), '..', 'docs', 'test_doc1.pdf')
    test_pdf2 = os.path.join(os.path.dirname(__file__), '..', 'docs', 'test_doc2.pdf')

    if not os.path.exists(test_pdf1) or not os.path.exists(test_pdf2):
        print("="*50)
        print("테스트를 위해 아래 경로에 PDF 파일이 필요합니다:")
        print(f"1. {test_pdf1}")
        print(f"2. {test_pdf2}")
        print("="*50)
    else:
        # 'CLT' 프로젝트 ID로 테스트 실행
        result = generate_questions_from_documents(test_pdf1, test_pdf2, 'CLT')
        if result:
            print(f"테스트 성공! 생성된 파일: {result['file_name']}")
        else:
            print("테스트 실패. 로그를 확인하세요.") 