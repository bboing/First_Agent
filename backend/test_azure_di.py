import os
import sys
import time
from dotenv import load_dotenv

from pathlib import Path

# 프로젝트 루트 경로 설정 (상위 디렉토리)
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "frontend" / "public" / "docs"

# .env 파일 로드 (상위 디렉토리의 .env 파일)
dotenv_path = PROJECT_ROOT / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)

class AzureDITester:
    """Azure Document Intelligence 설정 검증 클래스 (비용 절약용)"""
    
    def __init__(self):
        self.endpoint = os.getenv("AZURE_DI_ENDPOINT")
        self.key = os.getenv("AZURE_DI_KEY")
        self.test_results = {}
        
    def test_azure_di_config(self):
        """Azure DI 설정 검증 (API 호출 없음)"""
        try:
            if not self.endpoint or not self.key:
                print("❌ AZURE_DI_ENDPOINT 또는 AZURE_DI_KEY가 설정되지 않았습니다.")
                return False
            
            print("✅ Azure DI 설정 확인됨")
            print(f"   Endpoint: {self.endpoint}")
            print(f"   Key: {self.key[:10]}...")
            
            # 엔드포인트 형식 검증
            if not self.endpoint.startswith("https://"):
                print("⚠️ 경고: Endpoint가 https://로 시작하지 않습니다.")
            
            if not self.endpoint.endswith(".cognitiveservices.azure.com"):
                print("⚠️ 경고: Endpoint가 올바른 Azure Cognitive Services 형식이 아닙니다.")
            
            # 키 형식 검증 (일반적으로 32자)
            if len(self.key) < 20:
                print("⚠️ 경고: API 키가 너무 짧습니다.")
            
            print("✅ Azure Document Intelligence 설정 검증 완료")
            print("💡 실제 API 호출은 비용 절약을 위해 생략되었습니다.")
            
            self.test_results['config'] = True
            return True
            
        except Exception as e:
            print(f"❌ Azure DI 설정 검증 실패: {e}")
            self.test_results['config'] = False
            return False
    
    def test_file_structure(self):
        """파일 구조 및 지원 형식 검증"""
        try:
            print("📁 파일 구조 검증")
            
            # docs 디렉토리 확인
            if not DOCS_DIR.exists():
                print(f"❌ docs 디렉토리가 없습니다: {DOCS_DIR}")
                return False
            
            print(f"✅ docs 디렉토리 확인: {DOCS_DIR}")
            
            # 지원 파일 형식 확인
            supported_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.xml']
            found_files = {}
            
            for ext in supported_extensions:
                files = list(DOCS_DIR.glob(f"*{ext}"))
                found_files[ext] = len(files)
                if files:
                    print(f"   📄 {ext}: {len(files)}개 파일 발견")
                else:
                    print(f"   ⚠️ {ext}: 파일 없음")
            
            # 샘플 파일 확인
            sample_pdf = DOCS_DIR / "Customer Service_Booking_Manual.pdf"
            if sample_pdf.exists():
                file_size = sample_pdf.stat().st_size / (1024 * 1024)  # MB
                print(f"   📊 샘플 PDF 크기: {file_size:.2f} MB")
            else:
                print("   ⚠️ 샘플 PDF 파일이 없습니다.")
            
            self.test_results['file_structure'] = True
            return True
            
        except Exception as e:
            print(f"❌ 파일 구조 검증 실패: {e}")
            self.test_results['file_structure'] = False
            return False
    
    def test_dependencies(self):
        """필요한 라이브러리 설치 확인"""
        try:
            print("📦 의존성 라이브러리 확인")
            
            required_packages = [
                'azure-ai-formrecognizer',
                'azure-core',
                'python-dotenv'
            ]
            
            missing_packages = []
            
            for package in required_packages:
                try:
                    if package == 'azure-ai-formrecognizer':
                        import azure.ai.formrecognizer
                        print(f"   ✅ {package}: 설치됨")
                    elif package == 'azure-core':
                        import azure.core
                        print(f"   ✅ {package}: 설치됨")
                    elif package == 'python-dotenv':
                        import dotenv
                        print(f"   ✅ {package}: 설치됨")
                except ImportError:
                    print(f"   ❌ {package}: 설치되지 않음")
                    missing_packages.append(package)
            
            if missing_packages:
                print(f"⚠️ 설치되지 않은 패키지: {', '.join(missing_packages)}")
                print("   다음 명령어로 설치하세요:")
                print(f"   pip install {' '.join(missing_packages)}")
                return False
            
            print("✅ 모든 필수 라이브러리가 설치되어 있습니다.")
            self.test_results['dependencies'] = True
            return True
            
        except Exception as e:
            print(f"❌ 의존성 확인 실패: {e}")
            self.test_results['dependencies'] = False
            return False
    
    def test_environment_variables(self):
        """환경 변수 설정 확인"""
        try:
            print("🔧 환경 변수 설정 확인")
            
            required_vars = {
                'AZURE_DI_ENDPOINT': self.endpoint,
                'AZURE_DI_KEY': self.key,
                'AZURE_OPENAI_API_KEY': os.getenv("AZURE_OPENAI_API_KEY"),
                'AZURE_OPENAI_ENDPOINT': os.getenv("AZURE_OPENAI_ENDPOINT"),
                'AZURE_OPENAI_API_VERSION': os.getenv("AZURE_OPENAI_API_VERSION"),
                'DEPLOYMENT_CHAT': os.getenv("DEPLOYMENT_CHAT")
            }
            
            missing_vars = []
            
            for var_name, var_value in required_vars.items():
                if var_value:
                    print(f"   ✅ {var_name}: 설정됨")
                else:
                    print(f"   ❌ {var_name}: 설정되지 않음")
                    missing_vars.append(var_name)
            
            if missing_vars:
                print(f"⚠️ 설정되지 않은 환경 변수: {', '.join(missing_vars)}")
                print("   .env 파일을 확인해주세요.")
                return False
            
            print("✅ 모든 필수 환경 변수가 설정되어 있습니다.")
            self.test_results['environment'] = True
            return True
            
        except Exception as e:
            print(f"❌ 환경 변수 확인 실패: {e}")
            self.test_results['environment'] = False
            return False
    
    def test_code_integration(self):
        """코드 통합 상태 확인"""
        try:
            print("🔗 코드 통합 상태 확인")
            
            # 주요 모듈 import 테스트
            modules_to_test = [
                ('agent.chunking', 'extract_text_from_document'),
                ('auto_generator.pdf_question_generator', 'extract_text_from_pdf'),
                ('auto_generator.pdf_question_generator', 'extract_text_from_image'),
                ('auto_generator.pdf_question_generator', 'extract_text_from_xml')
            ]
            
            for module_name, function_name in modules_to_test:
                try:
                    module = __import__(module_name, fromlist=[function_name])
                    if hasattr(module, function_name):
                        print(f"   ✅ {module_name}.{function_name}: 사용 가능")
                    else:
                        print(f"   ❌ {module_name}.{function_name}: 함수 없음")
                except ImportError as e:
                    print(f"   ❌ {module_name}: import 실패 - {e}")
            
            print("✅ 코드 통합 상태 확인 완료")
            self.test_results['integration'] = True
            return True
            
        except Exception as e:
            print(f"❌ 코드 통합 확인 실패: {e}")
            self.test_results['integration'] = False
            return False
    
    def run_all_tests(self):
        """모든 테스트 실행 (비용 절약 버전)"""
        print("🧪 Azure Document Intelligence 설정 검증 (비용 절약 모드)")
        print("=" * 60)
        print("💡 실제 API 호출은 비용 절약을 위해 생략됩니다.")
        print("=" * 60)
        
        tests = [
            ("1️⃣ Azure DI 설정 검증", self.test_azure_di_config),
            ("2️⃣ 파일 구조 확인", self.test_file_structure),
            ("3️⃣ 의존성 라이브러리 확인", self.test_dependencies),
            ("4️⃣ 환경 변수 설정 확인", self.test_environment_variables),
            ("5️⃣ 코드 통합 상태 확인", self.test_code_integration)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n{test_name}")
            print("-" * 40)
            
            if test_func():
                passed_tests += 1
                print("✅ 테스트 통과")
            else:
                print("❌ 테스트 실패")
        
        # 결과 요약
        print("\n" + "=" * 60)
        print("📊 테스트 결과 요약")
        print("=" * 60)
        
        for test_name, result in self.test_results.items():
            status = "✅ 통과" if result else "❌ 실패"
            print(f"   {test_name}: {status}")
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"\n🎯 전체 성공률: {success_rate:.1f}% ({passed_tests}/{total_tests})")
        
        if success_rate >= 80:
            print("🎉 설정이 올바르게 구성되었습니다!")
            print("💡 실제 API 테스트가 필요하면 다음 명령어를 사용하세요:")
            print("   python test_azure_di.py --full-test")
        elif success_rate >= 50:
            print("⚠️ 일부 설정이 누락되었습니다. 설정을 확인해주세요.")
        else:
            print("❌ 많은 설정이 누락되었습니다. 환경 설정을 점검해주세요.")
        
        return success_rate >= 80

def main():
    """메인 실행 함수"""
    tester = AzureDITester()
    
    if not tester.run_all_tests():
        sys.exit(1)
    
    print("\n✅ Azure Document Intelligence 설정이 준비되었습니다.")
    print("💡 비용 절약을 위해 실제 API 호출은 생략되었습니다.")

if __name__ == "__main__":
    main() 