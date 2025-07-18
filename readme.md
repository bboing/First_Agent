# RAG 기반 문서 처리 및 챗봇 시스템

Azure OpenAI와 Milvus 벡터 데이터베이스를 활용한 RAG(Retrieval-Augmented Generation) 기반 문서 처리 및 챗봇 시스템입니다. PDF 문서 업로드, 자동 청킹, 임베딩, 질의응답 기능을 제공합니다.

## 🏗️ 프로젝트 구조

```
sub_lang/
├── 📁 backend/                          # 백엔드 서비스
│   ├── 📁 agent/                        # RAG 에이전트 및 AI 관련 모듈
│   │   ├── 📁 document_processing/      # 문서 처리 모듈
│   │   │   ├── allegronx_chunker.py     # PDF 청킹 및 처리
│   │   │   └── clear_collection.py      # Milvus 컬렉션 관리
│   │   ├── embedding.py                 # 벡터 임베딩 생성 및 Milvus 검색
│   │   ├── rag_agent.py                 # RAG 쿼리 처리
│   │   ├── config.py                    # 에이전트 설정
│   │   ├── admin.py                     # 관리자 기능
│   │   └── ping.py                      # 시스템 상태 확인
│   ├── 📁 auto_generator/               # 자동 생성 모듈
│   │   ├── pdf_question_generator.py    # PDF 기반 질문 자동 생성
│   │   └── sentence_generator.py        # 문장 자동 생성
│   ├── 📁 router/                       # 요청 라우팅
│   │   └── agent_orchestrator.py        # 에이전트 오케스트레이션
│   ├── 📁 dst/                          # 상태 추적
│   │   └── state_tracker.py             # 사용자 의도 추적
│   ├── 📁 docs/                         # 문서 저장소
│   │   ├── 📁 save_result/              # 처리 결과 저장
│   │   │   ├── 📁 save/                 # 임시 파일
│   │   │   ├── 📁 pdf_result/           # PDF 처리 결과
│   │   │   ├── 📁 pdf_questions/        # 질문 생성 결과
│   │   │   └── 📁 sentence/             # 문장 생성 결과
│   │   └── 📁 public/                   # 공개 문서
│   ├── 📁 logs/                         # 로그 파일
│   ├── 📁 result/                       # 결과 파일 (마크다운, 테이블)
│   ├── app.py                           # FastAPI 메인 애플리케이션
│   ├── main.py                          # CLI 진입점
│   ├── requirements.txt                 # Python 의존성
│   ├── Dockerfile                       # 백엔드 컨테이너 설정
│   └── .dockerignore                    # Docker 빌드 제외 파일
├── 📁 frontend/                         # 프론트엔드 서비스
│   ├── 📁 templates/                    # 웹 UI 템플릿
│   │   ├── RAG_Chat.html                # RAG 챗봇 인터페이스
│   │   ├── document-chunking.html       # 문서 업로드 및 청킹
│   │   ├── pdf_question_generator.html  # PDF 질문 생성
│   │   ├── csv_question_generator.html  # 학습 데이터 입력
│   │   └── node_editor.html             # React Flow 노드 편집기
│   ├── 📁 static/                       # 정적 파일
│   │   ├── chat.css                     # 챗봇 스타일
│   │   ├── style.css                    # 공통 스타일
│   │   ├── 📁 Hahmlet_Font/             # 폰트 파일
│   │   └── 📁 logo/                     # 로고 이미지
│   ├── server.js                        # Express 정적 서버
│   ├── package.json                     # Node.js 의존성
│   ├── Dockerfile                       # 프론트엔드 컨테이너 설정
│   └── .dockerignore                    # Docker 빌드 제외 파일
├── 📁 infra/                            # 인프라 설정
│   ├── docker-compose.yml               # 멀티 컨테이너 설정
│   ├── redis_client.py                  # Redis 연결
│   └── env_test.py                      # 환경 변수 테스트
├── 📁 logs/                             # 전체 로그
├── .env                                 # 환경 변수
├── .gitignore                           # Git 제외 파일
└── readme.md                            # 프로젝트 문서
```

## 🚀 주요 기능

### 1. 📄 문서 처리 및 임베딩
- **PDF 문서 업로드**: Azure Document Intelligence를 통한 텍스트 추출
- **자동 청킹**: 문서 구조 기반 스마트 청킹 (1~4 depth 제목 구조)
- **벡터 임베딩**: Azure OpenAI 임베딩 모델을 통한 벡터 생성
- **Milvus 저장**: 고성능 벡터 데이터베이스에 저장

### 2. 🤖 RAG 챗봇
- **문서 기반 질의응답**: 업로드된 문서 내용 기반 답변
- **유사도 검색**: Milvus를 통한 고속 벡터 유사도 검색
- **Azure OpenAI 연동**: GPT 모델을 통한 자연어 생성
- **실시간 대화**: 웹 인터페이스를 통한 실시간 챗봇

### 3. 🔧 컬렉션 관리
- **동적 컬렉션 목록**: 웹 UI에서 Milvus 컬렉션 조회
- **선택적 삭제**: 특정 컬렉션 삭제 기능
- **전체 삭제**: 모든 컬렉션 일괄 삭제
- **자동 재생성**: 컬렉션 없을 시 자동 생성

### 4. 📊 자동 질문 생성
- **PDF 기반 질문**: 문서 내용을 바탕으로 한 질문 자동 생성
- **Excel 출력**: 생성된 질문을 Excel 파일로 저장
- **다중 파일 지원**: PDF, 이미지, XML 파일 지원

### 5. 📝 문장 생성
- **학습 데이터 입력**: Excel 파일을 통한 학습 데이터 관리
- **자동 문장 생성**: 입력된 데이터 기반 문장 생성
- **결과 저장**: 생성된 문장을 Excel 파일로 저장

### 6. 🎨 웹 관리 인터페이스
- **문서 업로드**: 드래그 앤 드롭 파일 업로드
- **실시간 처리**: 진행 상황 실시간 모니터링
- **결과 다운로드**: 처리된 파일 다운로드
- **컬렉션 관리**: Milvus 컬렉션 관리 UI

## 🛠️ 기술 스택

### 백엔드
- **FastAPI**: 고성능 웹 프레임워크
- **Azure OpenAI**: GPT 모델 및 임베딩 서비스
- **Azure Document Intelligence**: 문서 텍스트 추출
- **Milvus**: 벡터 데이터베이스
- **Redis**: 캐싱 및 세션 관리
- **PostgreSQL**: 관계형 데이터베이스

### 프론트엔드
- **Express.js**: 정적 파일 서버
- **HTML/CSS/JavaScript**: 웹 인터페이스
- **Bootstrap**: 반응형 UI 프레임워크
- **SweetAlert2**: 알림 및 모달

### 인프라
- **Docker**: 컨테이너화
- **Docker Compose**: 멀티 컨테이너 오케스트레이션
- **MinIO**: 객체 저장소
- **etcd**: 분산 키-값 저장소

## 🚀 시작하기

### 1. 환경 설정
```bash
# .env 파일 생성 및 설정
cp .env.example .env

# 필수 환경 변수 설정
AZURE_OPENAI_API_KEY=your_openai_key
AZURE_OPENAI_ENDPOINT=your_openai_endpoint
AZURE_DI_ENDPOINT=your_di_endpoint
AZURE_DI_KEY=your_di_key
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

### 2. Docker Compose로 전체 서비스 실행
```bash
cd infra
docker-compose up -d
```

### 3. 서비스 접속
- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000
- **Milvus 관리**: http://localhost:3001
- **MinIO 관리**: http://localhost:9001

### 4. 개발 모드 실행
```bash
# 백엔드 개발
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# 프론트엔드 개발
cd frontend
npm install
npm run dev
```

## 📝 사용법

### 1. 문서 업로드 및 임베딩
1. 프론트엔드 접속: http://localhost:3000/document-chunking
2. "Document Chunking" 페이지 접속
3. PDF 파일 업로드
4. 자동 청킹 및 임베딩 처리 대기
5. 처리 완료 후 벡터 데이터베이스에 저장

### 2. RAG 챗봇 사용
1. 프론트엔드 접속: http://localhost:3000/RAG_Chat
2. "RAG Chat" 페이지 접속
3. 문서 관련 질문 입력
4. RAG 기반 답변 확인

### 3. 컬렉션 관리
1. "Document Chunking" 페이지에서 컬렉션 목록 확인
2. 특정 컬렉션 선택 후 삭제
3. "Delete All Collections" 버튼으로 전체 삭제

### 4. 질문 자동 생성
1. "PDF Question Generator" 페이지 접속
2. PDF 파일 업로드
3. 자동 질문 생성 및 Excel 다운로드

### 5. 문장 생성
1. "CSV Question Generator" 페이지 접속
2. Excel 파일 업로드
3. 자동 문장 생성 및 결과 다운로드

## 🔧 설정 및 커스터마이징

### 유사도 임계값 조정
```python
# backend/agent/embedding.py
def search_similar_texts(query: str, limit: int = 3, similarity_threshold: float = 0.7):
    # similarity_threshold 값을 조정하여 검색 정확도 조절
    # 높은 값 (0.7+): 정확한 답변, 적은 결과
    # 낮은 값 (0.3-): 다양한 답변, 많은 결과
```

### Milvus 인덱스 타입 설정
```bash
# .env 파일에 추가
MILVUS_INDEX_TYPE=IVF_FLAT        # 기본 (정확도 우선)
MILVUS_INDEX_TYPE=IVF_SQ8         # 메모리 효율적
MILVUS_INDEX_TYPE=IVF_PQ          # 균형
MILVUS_INDEX_TYPE=HNSW            # 고속 검색
```

### 청킹 크기 조정
```python
# backend/agent/document_processing/allegronx_chunker.py
def divide_large_passage(df, md_file_name, chunk_size=2000):
    # chunk_size 값을 조정하여 청킹 크기 변경
```

## 🐳 Docker 컨테이너 구조

### 서비스 구성
- **backend** (포트 8000): FastAPI 백엔드 서비스
- **frontend** (포트 3000): Express.js 프론트엔드 서비스
- **postgres** (포트 5432): PostgreSQL 데이터베이스
- **redis** (포트 6379): Redis 캐시
- **standalone** (포트 19530): Milvus 벡터 데이터베이스
- **etcd**: Milvus 메타데이터 저장소
- **minio** (포트 9000, 9001): MinIO 객체 저장소
- **attu** (포트 3001): Milvus 관리 UI

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
- `POST /process-pdf`: PDF 문서 처리 및 임베딩
- `POST /uploadfiles/pdf`: PDF 질문 생성
- `POST /uploadfiles/sentence`: 문장 생성
- `GET /collections`: Milvus 컬렉션 목록 조회
- `DELETE /collections/{name}`: 특정 컬렉션 삭제
- `DELETE /collections`: 모든 컬렉션 삭제
- `GET /downloadfiles/{folder}/{filename}`: 파일 다운로드
- `GET /api/log`: 로그 조회

### 프론트엔드 (포트 3000)
- `GET /`: RAG 챗봇 페이지
- `GET /document-chunking`: 문서 청킹 페이지
- `GET /pdf_question_generator`: PDF 질문 생성 페이지
- `GET /csv_question_generator`: CSV 질문 생성 페이지
- `GET /node_editor`: 노드 편집기 페이지
- `GET /health`: 헬스체크

## 📊 모니터링 및 로깅

### 로그 관리
- **백엔드 로그**: `backend/logs/`
- **전체 로그**: `logs/`
- **실시간 로그 조회**: `GET /api/log`
- **로그 레벨**: DEBUG, INFO, WARNING, ERROR

### 헬스체크
- **백엔드**: `http://localhost:8000/health`
- **프론트엔드**: `http://localhost:3000/health`
- **Milvus**: `http://localhost:9091/healthz`

## 🔧 개발 가이드

### 백엔드 개발
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
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

## 🔧 문제 해결

### 일반적인 문제들

1. **Milvus 연결 실패**
   ```bash
   # Milvus 서비스 상태 확인
   docker-compose ps
   # Milvus 재시작
   docker-compose restart standalone
   ```

2. **Azure OpenAI API 오류**
   ```bash
   # 환경 변수 확인
   cat .env | grep AZURE_OPENAI
   # API 키 및 엔드포인트 유효성 검증
   ```

3. **메모리 부족**
   ```bash
   # Docker 메모리 제한 확인
   docker stats
   # 불필요한 컨테이너 정리
   docker system prune
   ```

## 📝 라이센스

MIT License

## 🤝 기여

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의
bboing@wisenut.co.kr
프로젝트 관련 문의사항이 있으시면 이슈를 생성해 주세요.
