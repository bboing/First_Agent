# RAG 기반 챗봇 시스템

이 프로젝트는 Azure OpenAI와 Milvus 벡터 데이터베이스를 활용한 RAG(Retrieval-Augmented Generation) 기반 챗봇 시스템입니다. 문서 업로드, 임베딩, 질의응답 기능을 제공합니다.

## 🏗️ 프로젝트 구조

```
sub_lang/
├── 📁 agent/                    # RAG 에이전트 및 AI 관련 모듈
├── 📁 auto_generator/           # 자동 질문/문장 생성 모듈
├── 📁 docs/                     # 문서 저장소 및 결과물
├── 📁 infra/                    # 인프라 설정 (Docker, Redis)
├── 📁 router/                   # 요청 라우팅 및 오케스트레이션
├── 📁 templates/                # 웹 UI 템플릿
├── 📁 static/                   # 정적 파일 (CSS, JS)
├── 📁 logs/                     # 로그 파일
├── 📁 dst/                      # 상태 추적 및 관리
├── 📄 app.py                    # FastAPI 메인 애플리케이션
├── 📄 main.py                   # CLI 진입점
└── 📄 requirements.txt          # Python 의존성
```

## 📁 디렉토리 상세 설명

### 🤖 agent/ - AI 에이전트 모듈
- **rag_agent.py** (1.7KB): RAG 쿼리 처리 및 Azure OpenAI 연동
- **embedding.py** (8.0KB): 벡터 임베딩 생성 및 Milvus 검색 기능
- **chunking.py** (6.2KB): 문서 청킹 및 텍스트 처리
- **config.py** (1.6KB): 에이전트 설정 관리
- **ml_agent.py** (319B): 머신러닝 에이전트 (미구현)
- **admin.py** (535B): 관리자 기능
- **ping.py** (1.3KB): 시스템 상태 확인

### 🔧 auto_generator/ - 자동 생성 모듈
- **pdf_question_generator.py** (13KB): PDF/이미지/XML 기반 질문 자동 생성
- **sentence_generator.py** (21KB): 문장 및 학습 데이터 자동 생성
- **docs/**: 생성된 문서 저장소

### 📚 docs/ - 문서 및 데이터
- **Customer Service_Booking_Manual.pdf**: 샘플 매뉴얼 문서
- **save_result/**: 생성된 결과물 저장
- **html_docs/**: HTML 문서 저장소
- **public/**: 공개 문서 및 설정

### 🏗️ infra/ - 인프라 설정
- **docker-compose.yml** (2.3KB): Milvus, Redis, PostgreSQL 컨테이너 설정
- **redis_client.py** (621B): Redis 연결 및 캐싱
- **env_test.py** (922B): 환경 변수 테스트

### 🛣️ router/ - 라우팅
- **agent_orchestrator.py** (781B): 쿼리 라우팅 및 에이전트 오케스트레이션

### 🎨 templates/ - 웹 UI
- **chat.html** (4.4KB): RAG 챗봇 인터페이스
- **RAG_Management.html** (11KB): RAG 데이터 관리 화면
- **learning-data.html** (15KB): 학습 데이터 입력 화면
- **pdf_question_generator.html** (8.0KB): PDF 질문 생성 화면
- **upload_and_chunk.html** (3.3KB): 문서 업로드 및 청킹 화면

### 📊 dst/ - 데이터 상태 관리
- **state_tracker.py** (625B): 사용자 의도 추적 및 상태 관리

## 📄 주요 파일 설명

### 🚀 핵심 애플리케이션
- **app.py** (10KB): FastAPI 웹 서버 메인 애플리케이션
  - RAG 챗봇 API 엔드포인트
  - 파일 업로드 및 처리
  - 웹 UI 라우팅
  - 결과 파일 다운로드

- **main.py** (302B): CLI 애플리케이션 진입점
  - 콘솔 기반 챗봇 인터페이스

### 🔧 유틸리티 스크립트
- **test_azure_di.py** (8.5KB): Azure Document Intelligence 종합 테스트
- **logger_config.py** (453B): 로깅 설정

### 📋 설정 파일
- **requirements.txt** (889B): Python 패키지 의존성
- **.gitignore** (5.0B): Git 무시 파일 설정
- **Example_meta.json**: Azure Cognitive Search 인덱스 스키마 예시

## 🚀 주요 기능

### 1. RAG 챗봇
- 문서 기반 질의응답
- Azure OpenAI GPT 모델 연동
- Milvus 벡터 데이터베이스 검색
- 실시간 대화 인터페이스

### 2. 문서 처리
- PDF, 이미지(JPG, PNG, BMP, TIFF), XML 파일 지원
- Azure Document Intelligence 텍스트 추출
- 자동 청킹 및 임베딩
- 다국어 지원 (한국어 최적화)

### 3. 자동 질문 생성
- 문서 기반 질문 자동 생성
- Excel 파일로 결과 저장
- 다중 파일 형식 지원

### 4. 학습 데이터 관리
- 엑셀 기반 학습 데이터 입력
- 자동 문장 생성
- 데이터 검증 및 저장

### 5. 웹 관리 인터페이스
- RAG 데이터 조회 및 관리
- 실시간 로그 모니터링
- 파일 업로드/다운로드

## 🛠️ 기술 스택

### 백엔드
- **FastAPI**: 웹 프레임워크
- **Azure OpenAI**: GPT 모델 및 임베딩
- **Milvus**: 벡터 데이터베이스
- **Redis**: 캐싱 및 세션 관리
- **PostgreSQL**: 관계형 데이터베이스

### 프론트엔드
- **HTML/CSS/JavaScript**: 웹 인터페이스
- **Bootstrap**: UI 프레임워크

### 인프라
- **Docker**: 컨테이너화
- **Azure Document Intelligence**: 문서 분석
- **Azure Cognitive Search**: 검색 엔진 (예시)

## 🚀 시작하기

### 1. 환경 설정
```bash
# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정 (.env 파일)
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

### 2. 인프라 시작
```bash
cd infra
docker-compose up -d
```

### 3. 애플리케이션 실행
```bash
python app.py
```

### 4. 웹 접속
- 챗봇: http://localhost:8000/chat-ui
- RAG 관리: http://localhost:8000/RAG_Chat
- Milvus 관리: http://localhost:3000

## 📝 사용법

### 문서 업로드 및 임베딩
1. RAG 관리 페이지 접속
2. 문서 업로드 (PDF, 이미지, XML)
3. 자동 청킹 및 임베딩 처리
4. 벡터 데이터베이스 저장

### 챗봇 사용
1. 챗봇 페이지 접속
2. 문서 관련 질문 입력
3. RAG 기반 답변 확인

### 질문 자동 생성
1. PDF 질문 생성 페이지 접속
2. 워크플로우 및 상세 Task 문서 업로드
3. 자동 질문 생성 및 Excel 다운로드

## 🔧 설정 및 커스터마이징

### 유사도 임계값 조정
`agent/rag_agent.py`에서 `similarity_threshold` 값을 조정:
- 높은 값 (0.7+): 정확한 답변, 적은 결과
- 낮은 값 (0.3-): 다양한 답변, 많은 결과

### Azure 설정
`.env` 파일에서 Azure OpenAI 및 Document Intelligence 설정:
```
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_DI_ENDPOINT=your_di_endpoint
AZURE_DI_KEY=your_di_key
```

### 임베딩 모델 선택
다양한 임베딩 모델을 선택할 수 있습니다:

```bash
# .env 파일에 추가
EMBEDDING_MODEL_TYPE=azure_openai  # Azure OpenAI (기본)
EMBEDDING_MODEL_TYPE=bge_m3        # BGE-M3 (로컬)
```

#### 모델별 특징
- **Azure OpenAI (text-embedding-ada-002)**: 1536차원, 높은 정확도, API 비용 발생
- **BGE-M3**: 1024차원, 멀티모달 지원, 무료 로컬 실행, 다국어 최적화

## 📊 성능 최적화

### 벡터 검색 최적화
- Milvus 인덱스 설정 조정
- 청크 크기 및 오버랩 최적화
- 배치 처리 구현

### 압축 알고리즘 선택
Milvus에서 다양한 압축 알고리즘을 지원합니다:

#### 환경 변수 설정
```bash
# .env 파일에 추가
MILVUS_INDEX_TYPE=IVF_SQ8        # IVF_FLAT, IVF_SQ8, IVF_PQ, HNSW
MILVUS_NLIST=128                 # IVF 클러스터 개수
MILVUS_PQ_M=8                    # PQ 서브벡터 개수
MILVUS_PQ_NBITS=8                # PQ 비트 수
MILVUS_HNSW_M=16                 # HNSW 연결 수
MILVUS_HNSW_EF_CONSTRUCTION=200  # HNSW 구축 탐색 범위
```

#### 알고리즘별 특징
- **IVF_FLAT**: 무압축, 최고 정밀도, 높은 메모리 사용량
- **IVF_SQ8**: 4배 압축, 95-98% 정밀도, 균형잡힌 성능
- **IVF_PQ**: 16-64배 압축, 85-95% 정밀도, 메모리 효율적
- **HNSW**: 그래프 기반, 매우 빠른 검색, 중간 메모리 사용량

#### 성능 테스트
```bash
python agent/embedding.py --test-compression
```

### 캐싱 전략
- Redis를 활용한 검색 결과 캐싱
- 임베딩 벡터 캐싱
- 세션 관리

## 🐛 문제 해결

### 일반적인 문제
1. **Milvus 연결 실패**: Docker 컨테이너 상태 확인
2. **Azure API 오류**: API 키 및 엔드포인트 확인
3. **메모리 부족**: 청크 크기 조정

### 로그 확인
```bash
tail -f logs/debug.log
```

### Azure Document Intelligence 테스트 (비용 절약 모드)
```bash
python test_azure_di.py
```

💡 **비용 절약**: 실제 API 호출은 생략되어 비용이 발생하지 않습니다.
- 설정 및 환경 변수 검증
- 파일 구조 및 지원 형식 확인
- 의존성 라이브러리 설치 상태 확인
- 코드 통합 상태 검증

## 📈 향후 개발 계획

- [ ] 다중 언어 지원 확장
- [ ] 실시간 협업 기능
- [ ] 고급 분석 대시보드
- [ ] API 문서화 개선
- [ ] 성능 모니터링 도구

## 📄 라이선스

이 프로젝트는 내부 사용을 위한 프로토타입입니다.

## 👥 기여자

- 개발팀: RAG 시스템 개발
- 인프라팀: Docker 및 클라우드 설정
- 데이터팀: 문서 처리 및 임베딩 최적화
