import os
import sys
from dotenv import load_dotenv

# .env 파일 로드
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Azure Document Intelligence 테스트
def test_azure_di():
    try:
        from azure.ai.formrecognizer import DocumentAnalysisClient
        from azure.core.credentials import AzureKeyCredential
        
        endpoint = os.getenv("AZURE_DI_ENDPOINT")
        key = os.getenv("AZURE_DI_KEY")
        
        if not endpoint or not key:
            print("❌ AZURE_DI_ENDPOINT 또는 AZURE_DI_KEY가 설정되지 않았습니다.")
            return False
        
        print("✅ Azure DI 설정 확인됨")
        print(f"Endpoint: {endpoint}")
        print(f"Key: {key[:10]}...")
        
        # 클라이언트 초기화 테스트
        client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        print("✅ Azure Document Intelligence 클라이언트 초기화 성공")
        
        return True
        
    except Exception as e:
        print(f"❌ Azure DI 테스트 실패: {e}")
        return False

def test_pdf_extraction():
    try:
        from azure.ai.formrecognizer import DocumentAnalysisClient
        from azure.core.credentials import AzureKeyCredential
        
        endpoint = os.getenv("AZURE_DI_ENDPOINT")
        key = os.getenv("AZURE_DI_KEY")
        
        client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        
        # 테스트 PDF 파일 경로
        pdf_path = "./docs/Customer Service_Booking_Manual.pdf"
        
        if not os.path.exists(pdf_path):
            print(f"❌ 테스트 PDF 파일을 찾을 수 없습니다: {pdf_path}")
            return False
        
        print(f"📄 PDF 파일 분석 시작: {os.path.basename(pdf_path)}")
        
        with open(pdf_path, "rb") as f:
            poller = client.begin_analyze_document("prebuilt-document", f)
            result = poller.result()
        
        extracted_text = result.content
        
        if not extracted_text or not extracted_text.strip():
            print("❌ PDF에서 텍스트를 추출할 수 없습니다.")
            return False
        
        print(f"✅ PDF 텍스트 추출 성공!")
        print(f"📊 추출된 텍스트 길이: {len(extracted_text)} 문자")
        print(f"📝 텍스트 미리보기: {extracted_text[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF 추출 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Azure Document Intelligence 테스트 시작...")
    print("=" * 50)
    
    # 1. Azure DI 설정 테스트
    print("1️⃣ Azure DI 설정 테스트")
    if not test_azure_di():
        sys.exit(1)
    
    print()
    
    # 2. PDF 추출 테스트
    print("2️⃣ PDF 텍스트 추출 테스트")
    if not test_pdf_extraction():
        sys.exit(1)
    
    print()
    print("🎉 모든 테스트 통과!")
    print("✅ Azure Document Intelligence가 정상적으로 작동합니다.") 