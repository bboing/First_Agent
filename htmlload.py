import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime
import time
import json


dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

HTML_DIR = "./docs/html_docs/gimpho"
output_data = []
PROGRESS_FILE = "./docs/save_result/progress.json"
SAVE_INTERVAL = 10  # 10개 파일마다 중간 저장

# Azure OpenAI 설정
def get_azure_config():

    config = {
        "key": os.getenv("AZURE_OPENAI_API_KEY"),
        "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "deployment": os.getenv("DEPLOYMENT_CHAT"),
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION")
    }
    
    if not all(config.values()):
        raise ValueError("Azure OpenAI 설정이 .env 파일에 완전히 설정되지 않았습니다.")
        
    return config

# GPT 프롬프트 정의
def generate_prompt(text):
    return f"""다음은 데이터베이스 구조에 대한 HTML 문서입니다.
문서 내용을 분석하여 다음과 같은 구조화된 형태로 정리해주세요:

1. 사업/서비스명: (제목이나 주요 사업명)
2. 소관 부서: (담당 부서 정보)
3. 민원 분류: (대분류/중분류/소분류)
4. 주요 내용: (핵심 내용을 3-4개 항목으로 정리)
5. 신청/접수 방법: (신청 방법, 접수처 등)
6. 기타 중요 정보: (기타 유의사항이나 추가 정보)

각 항목은 명확하고 간결하게 작성해주세요. HTML 태그나 불필요한 내용은 제외하고 핵심 정보만 추출해주세요.

<문서 내용>
{text}
"""

# HTML 파일에서 텍스트 추출
def extract_text_from_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        print(f"HTML 파일 읽기 오류 ({file_path}): {e}")
        return ""

# Azure OpenAI 호출
def get_azure_openai_response(prompt):
    try:
        azure_config = get_azure_config()
        
        payload = {
            "temperature": 0.3,
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        r = requests.post(
            f"{azure_config['endpoint']}/openai/deployments/{azure_config['deployment']}/chat/completions",
            json=payload,
            headers={'Content-Type': 'application/json', 'api-key': azure_config["key"]},
            params={'api-version': azure_config["api_version"]},
            timeout=30  # 30초 타임아웃 추가
        )
        r.raise_for_status()
        response_json = r.json()
        return response_json['choices'][0]['message']['content'].strip()
        
    except requests.exceptions.Timeout:
        print("⏰ 타임아웃 발생, 재시도 중...")
        time.sleep(2)
        return get_azure_openai_response(prompt)  # 재시도
    except Exception as e:
        print(f"Azure OpenAI 호출 중 오류 발생: {e}")
        raise

# 진행 상황 저장
def save_progress(processed_files, output_data):
    progress = {
        "processed_files": processed_files,
        "total_processed": len(output_data),
        "timestamp": datetime.now().isoformat()
    }
    
    # 진행 상황 저장
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    
    # 중간 결과 저장
    if output_data:
        df = pd.DataFrame(output_data)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_filename = f"temp_results_{timestamp}.xlsx"
        temp_filepath = os.path.join("./docs/save_result", temp_filename)
        df.to_excel(temp_filepath, index=False)
        print(f"💾 중간 저장 완료: {temp_filepath}")

# 진행 상황 복구
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def main():
    # HTML 디렉토리 존재 확인
    if not os.path.exists(HTML_DIR):
        print(f"❌ HTML 디렉토리를 찾을 수 없습니다: {HTML_DIR}")
        return
    
    # HTML 파일 목록 가져오기
    html_files = [f for f in os.listdir(HTML_DIR) if f.endswith('.html')]
    
    if not html_files:
        print(f"❌ {HTML_DIR} 디렉토리에 HTML 파일이 없습니다.")
        return
    
    print(f"📁 처리할 HTML 파일 개수: {len(html_files)}")
    
    # 진행 상황 복구 확인
    progress = load_progress()
    if progress:
        print(f"🔄 이전 진행 상황 발견: {progress['total_processed']}개 파일 처리됨")
        response = input("이어서 처리하시겠습니까? (y/n): ")
        if response.lower() != 'y':
            print("처리를 취소합니다.")
            return
        processed_files = set(progress['processed_files'])
        start_index = len(processed_files)
    else:
        processed_files = set()
        start_index = 0
    
    # 저장 디렉토리 생성
    save_dir = "./docs/save_result/gimpho"
    os.makedirs(save_dir, exist_ok=True)
    
    # 각 HTML 파일 처리
    for i, filename in enumerate(html_files[start_index:], start_index + 1):
        if filename in processed_files:
            continue
            
        print(f"🔄 처리 중... ({i}/{len(html_files)}) {filename}")
        
        filepath = os.path.join(HTML_DIR, filename)
        
        # HTML에서 텍스트 추출
        raw_text = extract_text_from_html(filepath)
        
        if not raw_text.strip():
            print(f"⚠️ {filename}: 텍스트를 추출할 수 없습니다.")
            answer = "❌ 텍스트 추출 실패"
        else:
            # Azure OpenAI로 요약 생성
            prompt = generate_prompt(raw_text)
            try:
                answer = get_azure_openai_response(prompt)
                print(f"✅ {filename}: 요약 완료")
                time.sleep(1)  # API 호출 간격 조절
            except Exception as e:
                answer = f"❌ 오류 발생: {e}"
                print(f"❌ {filename}: 처리 실패 - {e}")

        # 결과 저장
        output_data.append({
            "파일명": filename,
            "Azure OpenAI 요약/답변": answer,
            "처리 시간": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        processed_files.add(filename)
        
        # 중간 저장
        if len(output_data) % SAVE_INTERVAL == 0:
            save_progress(list(processed_files), output_data)
            print(f"💾 {len(output_data)}개 파일 처리 완료, 중간 저장됨")

    # 최종 저장
    df = pd.DataFrame(output_data)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"html_to_azure_openai_responses_{timestamp}.xlsx"
    filepath = os.path.join(save_dir, filename)
    
    df.to_excel(filepath, index=False)
    
    # 진행 상황 파일 삭제
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
    
    print(f"✅ 완료: {filepath} 파일로 저장")
    print(f"📊 총 {len(output_data)}개 파일 처리 완료")

if __name__ == "__main__":
    main()