# RAG 기반 챗봇 시스템

이 프로젝트는 Azure OpenAI와 Milvus 벡터 데이터베이스를 활용한 RAG(Retrieval-Augmented Generation) 기반 챗봇 시스템입니다. 문서 업로드, 임베딩, 질의응답 기능을 제공합니다.

## 🏗️ 프로젝트 구조

```
sub_lang/
├── 📁 backend/                  # 백엔드 서비스
│   ├── 📁 agent/                # RAG 에이전트 및 AI 관련 모듈
│   ├── 📁 auto_generator/       # 자동 질문/문장 생성 모듈
│   ├── 📁 router/               # 요청 라우팅 및 오케스트레이션
│   ├── 📁 dst/                  # 상태 추적 및 관리
│   ├── 📁 logs/                 # 로그 파일
│   ├── 📄 app.py                # FastAPI 메인 애플리케이션
│   ├── 📄 main.py               # CLI 진입점
│   ├── 📄 requirements.txt      # Python 의존성
│   └── 📄 Dockerfile            # 백엔드 컨테이너 설정
├── 📁 frontend/                 # 프론트엔드 서비스
│   ├── 📁 templates/            # 웹 UI 템플릿
│   ├── 📁 static/               # 정적 파일 (CSS, JS)
│   ├── 📁 public/               # 공개 문서 및 설정
│   ├── 📄 server.js             # Express 정적 서버
│   ├── 📄 package.json          # Node.js 의존성
│   └── 📄 Dockerfile            # 프론트엔드 컨테이너 설정
├── 📁 infra/                    # 인프라 설정 (Docker, Redis)
├── 📄 readme.md                 # 프로젝트 문서
└── 📄 .env                      # 환경 변수
```

## 📁 디렉토리 상세 설명

### 🔧 backend/ - 백엔드 서비스
- **app.py** (12KB): FastAPI 웹 서버 메인 애플리케이션
- **main.py** (302B): CLI 애플리케이션 진입점
- **requirements.txt** (1KB): Python 패키지 의존성
- **Dockerfile**: 백엔드 컨테이너 설정

#### 🤖 agent/ - AI 에이전트 모듈
- **rag_agent.py** (1.7KB): RAG 쿼리 처리 및 Azure OpenAI 연동
- **embedding.py** (8.0KB): 벡터 임베딩 생성 및 Milvus 검색 기능
- **chunking.py** (6.2KB): 문서 청킹 및 텍스트 처리
- **config.py** (1.6KB): 에이전트 설정 관리
- **ml_agent.py** (319B): 머신러닝 에이전트 (미구현)
- **admin.py** (535B): 관리자 기능
- **ping.py** (1.3KB): 시스템 상태 확인

#### 🔧 auto_generator/ - 자동 생성 모듈
- **pdf_question_generator.py** (13KB): PDF/이미지/XML 기반 질문 자동 생성
- **sentence_generator.py** (21KB): 문장 및 학습 데이터 자동 생성

#### 🛣️ router/ - 라우팅
- **agent_orchestrator.py** (781B): 쿼리 라우팅 및 에이전트 오케스트레이션

#### 📊 dst/ - 데이터 상태 관리
- **state_tracker.py** (625B): 사용자 의도 추적 및 상태 관리

### 🎨 frontend/ - 프론트엔드 서비스
- **server.js** (1.2KB): Express 정적 파일 서버
- **package.json** (500B): Node.js 의존성
- **Dockerfile**: 프론트엔드 컨테이너 설정

#### 🎨 templates/ - 웹 UI
- **RAG_Chat.html** (4.4KB): RAG 챗봇 인터페이스
- **pdf_question_generator.html** (8.0KB): PDF 질문 생성 화면
- **csv_question_generator.html** (15KB): 학습 데이터 입력 화면
- **document-chunking.html** (3.3KB): 문서 업로드 및 청킹 화면
- **node_editor.html** (5.2KB): React Flow 노드 편집기

#### 📊 static/ - 정적 파일
- **chat.css**: 챗봇 스타일
- **style.css**: 공통 스타일
- **Hahmlet_Font/**: 폰트 파일
- **logo/**: 로고 이미지

#### 📚 public/ - 공개 문서
- **docs/**: 문서 저장소 및 결과물
- **save_result/**: 생성된 결과물 저장

### 🏗️ infra/ - 인프라 설정
- **docker-compose.yml** (3.2KB): 멀티 컨테이너 설정 (백엔드, 프론트엔드, Milvus, Redis, PostgreSQL)
- **redis_client.py** (621B): Redis 연결 및 캐싱
- **env_test.py** (922B): 환경 변수 테스트

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

### 6. 노드 편집기
- React Flow 기반 시각적 워크플로우 편집
- 드래그 앤 드롭 노드 생성
- 커스텀 노드 타입 지원

## 🛠️ 기술 스택

### 백엔드
- **FastAPI**: 웹 프레임워크
- **Azure OpenAI**: GPT 모델 및 임베딩
- **Milvus**: 벡터 데이터베이스
- **Redis**: 캐싱 및 세션 관리
- **PostgreSQL**: 관계형 데이터베이스

### 프론트엔드
- **Express.js**: 정적 파일 서버
- **HTML/CSS/JavaScript**: 웹 인터페이스
- **Bootstrap**: UI 프레임워크
- **React Flow**: 노드 편집기

### 인프라
- **Docker**: 컨테이너화
- **Docker Compose**: 멀티 컨테이너 오케스트레이션
- **Azure Document Intelligence**: 문서 분석
- **Azure Cognitive Search**: 검색 엔진 (예시)

## 🚀 시작하기

### 1. 환경 설정
```bash
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

### 3. 서비스 접속
- **백엔드 API**: http://localhost:8000
- **프론트엔드**: http://localhost:3000
- **Milvus 관리**: http://localhost:3001
- **MinIO 관리**: http://localhost:9001

### 4. 개발 모드 실행
```bash
# 백엔드 개발
cd backend
pip install -r requirements.txt
python app.py

# 프론트엔드 개발
cd frontend
npm install
npm run dev
```

## 📝 사용법

### 문서 업로드 및 임베딩
1. 프론트엔드 접속: http://localhost:3000
2. "Document Chunking" 페이지 접속
3. 문서 업로드 (PDF, 이미지, XML)
4. 자동 청킹 및 임베딩 처리
5. 벡터 데이터베이스 저장

### 챗봇 사용
1. 프론트엔드 접속: http://localhost:3000
2. "RAG Chat" 페이지 접속
3. 문서 관련 질문 입력
4. RAG 기반 답변 확인

### 질문 자동 생성
1. 프론트엔드 접속: http://localhost:3000
2. "PDF Question Generator" 페이지 접속
3. 워크플로우 및 상세 Task 문서 업로드
4. 자동 질문 생성 및 Excel 다운로드

### 노드 편집기 사용
1. 프론트엔드 접속: http://localhost:3000
2. "Node Editor" 페이지 접속
3. 드래그 앤 드롭으로 노드 생성
4. 커스텀 노드 타입 추가

## 🔧 설정 및 커스터마이징

### 유사도 임계값 조정
`backend/agent/rag_agent.py`에서 `similarity_threshold` 값을 조정:
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

### 벡터 압축 알고리즘 설정
Milvus 벡터 압축 알고리즘을 환경 변수로 설정:

```bash
# .env 파일에 추가
MILVUS_INDEX_TYPE=IVF_FLAT        # 기본 (정확도 우선)
MILVUS_INDEX_TYPE=IVF_SQ8         # 메모리 효율적
MILVUS_INDEX_TYPE=IVF_PQ          # 균형
MILVUS_INDEX_TYPE=HNSW            # 고속 검색
```

## 🐳 Docker 컨테이너 구조

### 서비스 구성
- **backend**: FastAPI 백엔드 서비스 (포트 8000)
- **frontend**: Express.js 프론트엔드 서비스 (포트 3000)
- **postgres**: PostgreSQL 데이터베이스 (포트 5432)
- **redis**: Redis 캐시 (포트 6379)
- **milvus-standalone**: Milvus 벡터 데이터베이스 (포트 19530)
- **milvus-etcd**: Milvus 메타데이터 저장소
- **milvus-minio**: Milvus 객체 저장소 (포트 9000, 9001)
- **milvus-attu**: Milvus 관리 UI (포트 3001)

### 볼륨 마운트
- **pgdata**: PostgreSQL 데이터
- **milvus_data**: Milvus 벡터 데이터
- **etcd_data**: Milvus 메타데이터
- **minio_data**: MinIO 객체 저장소

## 🔍 API 엔드포인트

### 백엔드 API (포트 8000)
- `GET /`: 루트 엔드포인트
- `GET /health`: 헬스체크
- `POST /chat`: RAG 챗봇 API
- `POST /uploadfiles/pdf`: PDF 질문 생성
- `POST /uploadfiles/sentence`: 문장 생성
- `GET /downloadfiles/{folder}/{filename}`: 파일 다운로드
- `GET /api/log`: 로그 조회
- `GET /api/mcp`: MCP 데이터 조회

### 프론트엔드 (포트 3000)
- `GET /`: RAG 챗봇 페이지
- `GET /pdf_question_generator`: PDF 질문 생성 페이지
- `GET /csv_question_generator`: CSV 질문 생성 페이지
- `GET /document-chunking`: 문서 청킹 페이지
- `GET /node_editor`: 노드 편집기 페이지
- `GET /health`: 헬스체크

## 📊 모니터링 및 로깅

### 로그 관리
- 백엔드 로그: `backend/logs/`
- 실시간 로그 조회: `GET /api/log`
- 로그 레벨: DEBUG, INFO, WARNING, ERROR

### 헬스체크
- 백엔드: `http://localhost:8000/health`
- 프론트엔드: `http://localhost:3000/health`
- Milvus: `http://localhost:9091/healthz`

## 🚀 배포

### Docker Compose로 전체 서비스 실행
```bash
cd infra
docker-compose up -d
```

### 개별 서비스 실행
```bash
# 백엔드만 실행
cd backend
docker build -t sub-lang-backend .
docker run -p 8000:8000 sub-lang-backend

# 프론트엔드만 실행
cd frontend
docker build -t sub-lang-frontend .
docker run -p 3000:3000 sub-lang-frontend
```

## 🔧 개발 가이드

### 백엔드 개발
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 프론트엔드 개발
```bash
cd frontend
npm install
npm run dev
```

### 테스트
```bash
# 백엔드 테스트
cd backend
python -m pytest

# 프론트엔드 테스트
cd frontend
npm test
```

## 📝 라이센스

MIT License

## 🤝 기여

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
