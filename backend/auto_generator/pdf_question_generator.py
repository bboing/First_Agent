import os
import openai
import requests
import pandas as pd
import json
from dotenv import load_dotenv
load_dotenv("/app/.env")
from datetime import datetime
import logging
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from ast import literal_eval
from pathlib import Path

# .env 파일 로드 (상위 디렉토리의 .env 파일)
dotenv_path = Path(__file__).parent.parent.parent / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

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
    logging.info(f"Azure config initialized for project_id: {project_id}")


# 파일 형식에 따라 텍스트를 추출
def extract_text_from_file(file_path: str) -> str:

    try:
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return extract_text_from_pdf(file_path)
        elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']:
            return extract_text_from_image(file_path)
        elif file_extension == '.xml':
            return extract_text_from_xml(file_path)
        else:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {file_extension}")
            
    except Exception as e:
        logging.error(f"Error extracting text from file {file_path}: {e}")
        raise

# PDF 파일에서 텍스트를 추출
def extract_text_from_pdf(file_path: str) -> str:
    """
    Azure Document Intelligence를 사용하여 PDF에서 텍스트를 추출합니다.
    """
    try:
        endpoint = os.getenv("AZURE_DI_ENDPOINT")
        key = os.getenv("AZURE_DI_KEY")
        
        if not endpoint or not key:
            raise ValueError("AZURE_DI_ENDPOINT와 AZURE_DI_KEY가 .env 파일에 설정되지 않았습니다.")
        
        # Azure Document Intelligence 클라이언트 초기화
        client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        
        print(f"📄 PDF 분석 시작: {os.path.basename(file_path)}")
        
        # PDF 파일을 바이너리로 읽기
        with open(file_path, "rb") as f:
            # Document Intelligence로 문서 분석
            poller = client.begin_analyze_document("prebuilt-document", f)
            result = poller.result()
        
        # 추출된 텍스트 가져오기
        extracted_text = result.content
        
        if not extracted_text or not extracted_text.strip():
            print(f"⚠️ 경고: {os.path.basename(file_path)}에서 텍스트를 추출할 수 없습니다.")
            return ""
        
        print(f"✅ PDF 텍스트 추출 완료: {os.path.basename(file_path)} ({len(extracted_text)} 문자)")
        return extracted_text
        
    except Exception as e:
        print(f"❌ PDF 텍스트 추출 실패 ({os.path.basename(file_path)}): {e}")
        raise


# 이미지 파일에서 텍스트를 추출
def extract_text_from_image(file_path: str) -> str:

    try:
        endpoint = os.getenv("AZURE_DI_ENDPOINT")
        key = os.getenv("AZURE_DI_KEY")
        
        if not endpoint or not key:
            raise ValueError("AZURE_DI_ENDPOINT와 AZURE_DI_KEY가 .env 파일에 설정되지 않았습니다.")
        
        # Azure Document Intelligence 클라이언트 초기화
        client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        
        print(f"🖼️ 이미지 분석 시작: {os.path.basename(file_path)}")
        
        # 이미지 파일을 바이너리로 읽기
        with open(file_path, "rb") as f:
            # Document Intelligence로 문서 분석
            poller = client.begin_analyze_document("prebuilt-document", f)
            result = poller.result()
        
        # 추출된 텍스트 가져오기
        extracted_text = result.content
        
        if not extracted_text or not extracted_text.strip():
            print(f"⚠️ 경고: {os.path.basename(file_path)}에서 텍스트를 추출할 수 없습니다.")
            return ""
        
        print(f"✅ 이미지 텍스트 추출 완료: {os.path.basename(file_path)} ({len(extracted_text)} 문자)")
        return extracted_text
        
    except Exception as e:
        print(f"❌ 이미지 텍스트 추출 실패 ({os.path.basename(file_path)}): {e}")
        raise

# XML 파일에서 텍스트를 추출
def extract_text_from_xml(file_path: str) -> str:

    try:
        import xml.etree.ElementTree as ET
        
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # XML의 모든 텍스트 내용을 추출
        text_content = []
        
        def extract_text_from_element(element):
            if element.text and element.text.strip():
                text_content.append(element.text.strip())
            for child in element:
                extract_text_from_element(child)
            if element.tail and element.tail.strip():
                text_content.append(element.tail.strip())
        
        extract_text_from_element(root)
        
        extracted_text = ' '.join(text_content)
        logging.info(f"Successfully extracted text from XML {os.path.basename(file_path)}.")
        return extracted_text
        
    except Exception as e:
        logging.error(f"Error extracting text from XML {file_path}: {e}")
        raise


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

def create_synthesis_questions(text1: str, text2: str) -> list:

    text1_snippet = text1[:4000]
    text2_snippet = text2[:4000]

    prompt_template = f'''
# 첫 번째 문서 내용:
{text1_snippet}
---
# 두 번째 문서 내용:
{text2_snippet}

# 지시사항:
- 첫 번째 문서는 업무 프로세스 정보를 담고 있습니다.
- 두 번째 문서는 첫 번째 문서의 bpmn으로 task를 구분한 내용을 담고 있습니다.
- 위 두 문서의 내용을 종합적으로 분석하여, 질문자가 두 문서를 모두 깊이 이해했는지 확인할 수 있는 **질문 30개**를 생성해주세요.
- 질문은 구체적이고 명확해야 합니다.

# 예시:
'Create General BKG' 프로세스 관련 질문:
* 'General BKG' 프로세스의 목적은 무엇인가요? 
* 예약 변경 요청은 어떻게 접수되나요? 
* 수동으로 예약을 생성하는 과정은 어떻게 되나요? 
* E-Booking 업로드 과정은 어떻게 되나요? 
* Booking Status가 'Firm'으로 확정되는 조건은 무엇인가요? 
* Booking Status를 변경하는 방법에는 어떤 것들이 있나요? 
* 예약 취소는 어떻게 이루어지나요? 
* Empty Pick-up Order는 어떻게 전송되나요? 
* Booking Receipt Notice는 어떻게 발송되나요? 
* 'Create General BKG' 프로세스와 관련된 주요 프로그램은 무엇인가요? 
데이터 및 시스템 연동 관련 질문:
* 'Empty Pick-up' 서브 프로세스에서 외부 포털은 어떤 정보를 연동하나요?
* 'Customer' 서브 프로세스에서 E-Service, E-Mail, FAX는 어떤 역할을 하나요?
* 'Customer' (EDI) 서브 프로세스에서 EDI는 어떤 역할을 하나요?
* EDI 설정은 어떤 역할을 하며, 어떤 정보가 포함되나요?
* Booking Master 프로그램은 어떤 외부 시스템과 연동되나요? 
* Empty Container Release Order 발송 시 EDI 연결 여부에 따라 어떤 차이가 있나요? 
* Booking Receipt Notice 발송 시 고객에게 EDI를 보내려면 어떤 설정이 필요한가요? 
* Booking Status가 'Firm'이 되면 재무 모듈로 어떤 정보가 전달되나요? 
* 터미널로 IFTMBC 또는 COPARN 메시지가 전송될 수 있나요? 
* 'Empty Pick-up Order' 및 'Booking Notice'와 관련된 외부 인터페이스 항목은 무엇인가요? 
기타 질문:
* 이 프로세스의 전체적인 문서화 목표는 무엇인가요?
* Special Cargo Process는 어떤 역할을 하며, 어떤 주의사항이 있나요?
* Inland Transport 준비는 어떤 상황에서 이루어지나요?
* Vessel Space Control, Update Schedule, Create Schedule, Service Network 이벤트는 어떤 트리거 역할을 하나요?

# 출력 형식:
- 예시:["question1","question2","question3","question4","question5","question6","question7","question8","question9",..,"question30"]
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


# 질문 리스트를 Excel 파일로 저장
def save_questions_to_excel(questions: list) -> dict:

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

# 문서 기반 질문 생성
def generate_questions_from_documents(file_path1: str, file_path2: str, project_id: str) -> dict:

    try:
        print("🚀 문서 기반 질문 생성 시작...")
        
        # 1. Azure 설정 초기화
        print(f"⚙️ Azure 설정 초기화 중... (프로젝트: {project_id})")
        initialize_azure_config(project_id)

        # 2. 두 파일에서 텍스트 추출
        print("📖 문서에서 텍스트 추출 중...")
        print(f"📄 파일 1: {os.path.basename(file_path1)}")
        text1 = extract_text_from_file(file_path1)
        
        print(f"📄 파일 2: {os.path.basename(file_path2)}")
        text2 = extract_text_from_file(file_path2)

        # 텍스트 검증
        if not text1.strip() or not text2.strip():
            raise ValueError("하나 이상의 파일에서 텍스트를 추출할 수 없습니다.")

        print(f"✅ 텍스트 추출 완료 - 파일1: {len(text1)}자, 파일2: {len(text2)}자")

        # 3. 텍스트를 기반으로 질문 생성
        print("🤖 Azure OpenAI로 질문 생성 중...")
        questions = create_synthesis_questions(text1, text2)

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
        logging.error(f"An error occurred in generate_questions_from_documents: {e}", exc_info=True)
        return None

if __name__ == '__main__':

    print("🌐 브라우저에서 /pdf-question-generator 페이지에 접속하여 파일을 업로드하세요.") 