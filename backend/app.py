import os
import sys
from pathlib import Path

# 상위 디렉토리의 .env 파일을 로드하기 위해 경로 추가
sys.path.append(str(Path(__file__).parent.parent))

# BASE_DIR 정의 (backend root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import logging
from logger_config import setup_logging
setup_logging()
logger = logging.getLogger("app")

from agent.rag_agent import handle_rag
import re
import openpyxl
import json
import pandas as pd
import uvicorn
import random
import ast
import io
import auto_generator.sentence_generator
import auto_generator.pdf_question_generator
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from typing import Union, List
from tempfile import NamedTemporaryFile
from enum import Enum
from pydantic import BaseModel

from agent.document_processing.allegronx_chunker import process_files_in_directory, batch_process_directory, merge_adjacent_table, parse_table_for_embedding, replace_markdown_with_llm_data, divide_large_passage
from agent.embedding import process_chunks, process_chunks_with_metadata
from agent.document_processing.clear_collection import list_collections, get_collections_info, clear_collection, clear_all_collections



def detect_table_content(content_str: str) -> bool:
    """
    텍스트가 테이블 내용인지 감지하는 함수
    """
    # 테이블 마크다운 패턴
    table_patterns = [
        r'\|[^|]+\|[^|]+\|',  # | 컬럼1 | 컬럼2 |
        r'[A-Za-z]+\s*:\s*[A-Za-z0-9\s]+,\s*[A-Za-z]+\s*:\s*[A-Za-z0-9\s]+',  # 컬럼1: 값1, 컬럼2: 값2
        r'^\s*[A-Za-z]+\s*:\s*[A-Za-z0-9\s]+\s*$',  # 단일 컬럼: 값
    ]
    
    for pattern in table_patterns:
        if re.search(pattern, content_str, re.MULTILINE):
            return True
    
    return False

def calculate_table_match_score(content_str: str, table_data: dict) -> int:
    """
    테이블 매칭 점수를 계산하는 함수
    """
    score = 0
    
    # llm_generate_data 매칭
    if table_data.get('llm_generate_data'):
        for llm_item in table_data['llm_generate_data']:
            if llm_item in content_str:
                score += len(llm_item) * 2  # 더 긴 매칭에 더 높은 점수
    
    # 테이블 구조 패턴 매칭
    table_pattern = r'\|[^|]+\|[^|]+\|'
    if re.search(table_pattern, content_str):
        score += 50
    
    # 페이지 번호 일치 (정수를 문자열로 변환하여 비교)
    if 'page' in table_data and str(table_data['page']) in content_str:
        score += 100
    
    return score

if __name__ == "__main__" :
    uvicorn.run("app:app", host = "0.0.0.0", port=8000, reload = True)

app = FastAPI()

# CORS 허용 (프론트엔드와의 통신을 위해)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 서비스 시에는 도메인 제한 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

@app.post("/process-pdf")
async def process_pdf_endpoint(files: List[UploadFile] = File(...)):
    logger.info("✅ /process-pdf 엔드포인트 호출 시작")
    try:
        logger.info(f"📄 업로드된 파일 개수: {len(files)}")
        
        # 업로드 디렉토리 생성 (docs 하위)
        upload_dir = os.path.join(BASE_DIR, "docs", "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        
        # 모든 파일을 업로드 디렉토리에 저장
        uploaded_files = []
        
        for i, file in enumerate(files):
            logger.info(f"📄 파일 {i+1} 처리 중: {file.filename}")
            
            # 파일명 정리 (특수문자 제거, 중복 방지)
            safe_filename = f"upload_{i+1}_{file.filename.replace(' ', '_')}"
            file_path = os.path.join(upload_dir, safe_filename)
            
            # 파일 저장
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            uploaded_files.append(file_path)
            logger.info(f"💾 파일 {i+1} 저장 완료: {file_path}")
        
        logger.info(f"💾 총 {len(uploaded_files)}개 파일 저장 완료")
        logger.info(f"📁 업로드 디렉토리: {upload_dir}")
        logger.info(f"📄 저장된 파일들: {uploaded_files}")

        # allgeronx_chunker.py의 함수들을 순서대로 호출
        logger.info(">> 1. PDF -> Markdown 변환 시작")
        results, md_files = process_files_in_directory(upload_dir)
        if not results:
            logger.error("❌ PDF 처리 실패: 'results'가 비어있습니다.")
            raise HTTPException(status_code=400, detail="PDF 파일 처리 중 오류가 발생했습니다.")
        logger.info("✅ 1. PDF -> Markdown 변환 완료")

        # 첫 번째 파일명을 기준으로 사용 (타임스탬프 제거)
        filename_wo_ext = os.path.splitext(os.path.basename(files[0].filename))[0]
        md_file_name = filename_wo_ext

        logger.info(">> 2. 마크다운 Chunking 시작")
        df = batch_process_directory(md_files[0], md_file_name)  # md_files는 리스트이므로 첫 번째 파일 사용
        if df.empty:
            logger.error("❌ 마크다운 처리 실패: 데이터프레임이 비어있습니다.")
            raise HTTPException(status_code=400, detail="마크다운 파일 처리 중 오류가 발생했습니다.")
        logger.info(f"✅ 2. 마크다운 Chunking 완료. {len(df)}개 패시지 생성.")

        all_tables_data = []
        for result in results:
            all_tables_data.extend(result['tables_data'])

        logger.info(">> 3. 테이블 병합 시작")
        df, all_tables_data = merge_adjacent_table(df, all_tables_data, md_file_name)
        logger.info("✅ 3. 테이블 병합 완료")

        logger.info(">> 4. 테이블 데이터 문장 변환 시작")
        all_tables_data = parse_table_for_embedding(all_tables_data)
        df, all_tables_data = replace_markdown_with_llm_data(df, all_tables_data, md_file_name)
        logger.info("✅ 4. 테이블 데이터 문장 변환 완료")

        logger.info(">> 5. 대용량 패시지 분할 시작")
        df = divide_large_passage(df, md_file_name)
        logger.info("✅ 5. 대용량 패시지 분할 완료")


        # process_chunks 함수에 맞게 데이터 가공 (테이블 메타데이터 활용)
        logger.info(">> 6. 임베딩 데이터 가공 시작")
        chunks_for_embedding = []
        for _, row in df.iterrows():
            page = row['pages'][0] if row['pages'] else 1
            
            # processing_pdf.py에서 생성한 튜플 구조를 (text, page) 형태로 변환
            if isinstance(row['content'], tuple) and len(row['content']) >= 5:
                # 튜플인 경우: (대제목, 중제목, 소제목, 세제목, 내용, ...)
                content_text = row['content'][4]  # 5번째 요소가 실제 내용
            else:
                # 문자열인 경우: 그대로 사용
                content_text = row['content']
            
            # 테이블 데이터인지 확인하고 메타데이터 매칭 (개선된 버전)
            table_metadata = None
            content_str = str(row['content'])
            
            # 방법 1: 개선된 점수 기반 매칭
            best_match_score = 0
            best_match_table = None
            
            # 테이블 내용인지 먼저 감지
            is_table_content = detect_table_content(content_str)
            
            for table in all_tables_data:
                match_score = calculate_table_match_score(content_str, table)
                
                # 페이지 번호 일치 시 추가 점수
                if table['page'] == page:
                    match_score += 100
                
                # 테이블 내용이 감지된 경우 추가 점수
                if is_table_content:
                    match_score += 200
                
                # 더 높은 점수의 매칭 선택
                if match_score > best_match_score:
                    best_match_score = match_score
                    best_match_table = table
            
            if best_match_table and best_match_score > 100:  # 최소 임계값 상향 조정
                table_metadata = best_match_table
                logger.info(f"📊 테이블 메타데이터 매칭 (점수 기반): {table_metadata['key']} (페이지: {table_metadata['page']}, 점수: {best_match_score})")
            
            # 방법 2: 백업 매칭 (페이지 기반)
            if not table_metadata and is_table_content:
                # 페이지 번호로 매칭 (테이블 내용이 감지된 경우에만)
                for table in all_tables_data:
                    if table['page'] == page:
                        table_metadata = table
                        logger.info(f"📊 테이블 메타데이터 매칭 (페이지 백업): {table['key']} (페이지: {table['page']})")
                        break
            
            # 테이블 메타데이터가 있으면 테이블 정보를 포함하여 저장
            if table_metadata:
                # 테이블 카테고리 생성 (예: "Table_5x3", "Table_10x4")
                category = f"Table_{table_metadata['rows']}x{table_metadata['columns']}"
                
                # 테이블 키를 토픽으로 사용 (길이 제한 및 정제)
                topic = table_metadata['key'][:200] if len(table_metadata['key']) > 200 else table_metadata['key']
                
                # 병합된 테이블인지 확인
                if table_metadata.get('merged_indices'):
                    category += "_Merged"
                    topic = f"Merged_{topic}"
                
                # 테이블 데이터인지 확인 (llm_generate_data가 있으면 테이블)
                if table_metadata.get('llm_generate_data'):
                    logger.info(f"📊 테이블 데이터 감지: {category} - {topic}")
                else:
                    logger.info(f"📄 일반 텍스트 (테이블 메타데이터 있음): {category} - {topic}")
                
                chunks_for_embedding.append((content_text, page, category, topic, table_metadata))
            else:
                # 일반 텍스트인 경우
                category = "Text"
                topic = f"Page_{page}"
                logger.info(f"📄 일반 텍스트: {category} - {topic}")
                chunks_for_embedding.append((content_text, page, category, topic, None))
                
        logger.info(f"✅ 6. 임베딩 데이터 가공 완료. {len(chunks_for_embedding)}개 청크 준비.")

        # 임베딩 및 저장 (테이블 메타데이터 포함)
        logger.info(">> 7. Milvus 임베딩 및 저장 시작")
        # PDF 처리 시에는 기본 컬렉션 사용
        process_chunks_with_metadata(chunks_for_embedding, collection_name="Booking_Embedding")
        logger.info("✅ 7. Milvus 임베딩 및 저장 완료")


        # 업로드된 파일들 삭제
        for uploaded_file_path in uploaded_files:
            if os.path.exists(uploaded_file_path):
                os.remove(uploaded_file_path)
                logger.info(f"🗑️ 업로드 파일 삭제: {uploaded_file_path}")
        
        # 업로드 디렉토리가 비어있으면 삭제
        try:
            if os.path.exists(upload_dir) and not os.listdir(upload_dir):
                os.rmdir(upload_dir)
                logger.info(f"🗑️ 빈 업로드 디렉토리 삭제: {upload_dir}")
        except Exception as e:
            logger.warning(f"⚠️ 업로드 디렉토리 삭제 실패: {e}")

        # 성공적으로 처리되었을 때 반환
        logger.info("🎉 모든 처리 성공! JSON 응답을 반환합니다.")
        return JSONResponse(content={"success": True, "message": "PDF 파일 처리 및 임베딩이 완료되었습니다.", "chunk_count": len(df)})

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"❗️❗️❗️ PDF 처리 파이프라인 중 심각한 오류 발생 ❗️❗️❗️\n{error_details}")
        return JSONResponse(
            status_code=500,
            content={"error": "백엔드 처리 중 심각한 오류 발생", "details": str(e), "traceback": error_details}
        )



@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    answer = handle_rag(req.question)
    return {"answer": answer}


@app.post("/api/v1/agent/excel_rag_generator")
async def excel_rag_generator_endpoint(
    file: UploadFile = File(...),
    collection_name: str = Form(...)
):
    """
    엑셀 파일을 받아 'question' 컬럼의 각 질문에 대한 RAG 답변을 생성하고,
    'answer' 컬럼을 추가하여 수정된 엑셀 파일을 반환합니다.
    """
    logger.info(f"✅ /api/v1/agent/excel_rag_generator 엔드포인트 호출 시작 (컬렉션: {collection_name})")
    
    # 파일 확장자 검사
    if not file.filename.endswith((".xlsx", ".xls")):
        logger.error(f"❌ 지원하지 않는 파일 형식: {file.filename}")
        raise HTTPException(status_code=400, detail="잘못된 파일 형식입니다. .xlsx 또는 .xls 파일을 업로드해주세요.")

    try:
        # 엑셀 파일 읽기
        content = await file.read()
        df = pd.read_excel(content)
        logger.info(f"📄 엑셀 파일 로드 완료: {file.filename}, {len(df)}개 행")

        # 'question' 컬럼 확인
        if 'question' not in df.columns:
            logger.error("❌ 'question' 컬럼을 찾을 수 없습니다.")
            raise HTTPException(status_code=400, detail="'question' 컬럼을 찾을 수 없습니다.")

        # 각 질문에 대해 RAG 답변 생성 (선택된 컬렉션 사용)
        answers = []
        for question in df['question']:
            if pd.isna(question) or not str(question).strip():
                answers.append("") # 질문이 비어있는 경우
                continue
            
            logger.info(f"💬 RAG 에이전트 호출: '{question}' (컬렉션: {collection_name})")
            answer = handle_rag(str(question), collection_name=collection_name)
            answers.append(answer)
            logger.info("💡 RAG 답변 수신")

        # 답변 컬럼 추가
        df['answer'] = answers
        logger.info("✅ 모든 질문에 대한 답변 생성 및 'answer' 컬럼 추가 완료")

        # 수정된 엑셀 파일을 메모리에 저장
        output = io.BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        
        # 결과 파일명 생성
        result_filename = f"result_{file.filename}"
        download_directory = os.getenv('DOWNLOAD_DIRECTORY', 'save_result')
        
        # 디렉토리 생성
        os.makedirs(os.path.join(download_directory, 'answer'), exist_ok=True)

        # 파일을 디스크에 저장
        result_path = os.path.join(download_directory, 'answer', result_filename)
        with open(result_path, 'wb') as f:
            f.write(output.getvalue())
        
        logger.info(f"💾 결과 파일 저장 완료: {result_path}")
        
        # JSON 응답 반환
        return JSONResponse({
            "status": "success",
            "file_name": result_filename,
            "message": "RAG 답변 생성이 완료되었습니다."
        })

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"❗️❗️❗️ 엑셀 처리 중 심각한 오류 발생 ❗️❗️❗️\n{error_details}")
        raise HTTPException(
            status_code=500,
            detail=f"엑셀 파일 처리 중 오류가 발생했습니다: {str(e)}"
        )

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "backend"}

# HTML 템플릿 엔드포인트들은 프론트엔드에서 처리하므로 제거
# 프론트엔드: http://localhost:3000 에서 웹 페이지 서빙


# 학습 데이터 업로드 Form (PDF, 이미지, XML 기반 질문 생성)
@app.post("/uploadfiles/pdf")
async def create_upload_documents(
    project_id: str = Form(...),
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    
    async def save_file_to_temp(upload_file: UploadFile):
        # 지원하는 파일 확장자
        supported_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.xml']
        file_extension = os.path.splitext(upload_file.filename)[1].lower()
        
        if file_extension not in supported_extensions:
            logger.error(f"app.py: File with invalid extension uploaded: {upload_file.filename}")
            raise ValueError(f"지원하지 않는 파일 형식입니다: {file_extension}. 지원 형식: {', '.join(supported_extensions)}")
        
        temp_file = NamedTemporaryFile(delete=False, suffix=file_extension)
        with open(temp_file.name, 'wb') as f:
            content = await upload_file.read()
            f.write(content)
        
        logger.info(f"app.py: File saved to temporary location: {temp_file.name}")
        return temp_file.name

    file_path1 = None
    file_path2 = None
    try:
        file_path1 = await save_file_to_temp(file1)
        file_path2 = await save_file_to_temp(file2)

        result = auto_generator.pdf_question_generator.generate_questions_from_documents(
            file_path1=file_path1,
            file_path2=file_path2,
            project_id=project_id
        )

        if not result or 'file_name' not in result:
            logger.error(f"app.py: Question generation failed or returned an invalid result: {result}")
            raise HTTPException(status_code=500, detail="질문 생성에 실패했습니다.")
        
        logger.info(f"app.py: Successfully generated questions. Result: {result}")
        return result

    except ValueError as e:
        logger.exception("app.py: A value error occurred during document processing")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("app.py: An unexpected error occurred during document processing")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if file_path1 and os.path.exists(file_path1):
            os.remove(file_path1)
            logger.info(f"app.py: Temporary file {file_path1} deleted.")
        if file_path2 and os.path.exists(file_path2):
            os.remove(file_path2)
            logger.info(f"app.py: Temporary file {file_path2} deleted.")

# 학습 데이터 업로드 Form
@app.post("/uploadfiles/sentence")
async def create_upload_files(
    field_business: Union[str, None] = Form(None),
    user_type: Union[str, None] = Form(None),
    Constraints: Union[str, None] = Form(None),
    project_id: str = Form(...),
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    try:
        # Azure 설정 초기화
        auto_generator.sentence_generator.initialize_azure_config(project_id)
        
        # 파일 저장 함수
        async def save_file_to_temp(upload_file: UploadFile):
            if not upload_file.filename.endswith(".xlsx"):
                logger.error(f"app.py: File with invalid extension uploaded: {upload_file.filename}")
                raise ValueError(f"Invalid file extension for {upload_file.filename}")
            temp_file = NamedTemporaryFile(delete=False, suffix=".xlsx")
            with open(temp_file.name, 'wb') as f:
                while True:
                    chunk = await upload_file.read(1024 * 1024)  # 1MB chunks
                    if not chunk:
                        break
                    f.write(chunk)
            logger.info(f"app.py: File saved to temporary location: {temp_file.name}")
            return temp_file.name

        # Q&A Set(질답셋) 저장
        file_path = await save_file_to_temp(file1)
        
        # Entity Dict(엔티티 사전) 저장
        file_path2 = await save_file_to_temp(file2)

        # 데이터 프레임 로드 및 검증
        df = pd.read_excel(file_path)
        edf = pd.read_excel(file_path2)
        
        if (df.columns[0] != 'Answer') and (edf.columns[0] != 'Entry'):
            logger.warning("app.py: File contents do not meet the expected format")
            raise ValueError("File contents do not meet expected format")

        # 데이터 저장 (project_id 제거)
        result = auto_generator.sentence_generator.Save_data(field_business, user_type, df, edf, Constraints)
        logger.info(f"app.py: Save_data result: {result}")
        if not result or 'file_name' not in result:
            logger.error(f"app.py: Returned result does not contain file_name! result: {result}")
        logger.info("app.py: Data successfully saved.")
        return result

    except ValueError as e:
        logger.exception("app.py: A value error occurred")
        return {"error": str(e)}
    except Exception as e:
        logger.exception("app.py: An unexpected error occurred")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 임시 파일 삭제
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"app.py: Temporary file {file_path} deleted.")
        if 'file_path2' in locals() and os.path.exists(file_path2):
            os.remove(file_path2)
            logger.info(f"app.py: Temporary file {file_path2} deleted.")


# 학습데이터 결과 파일 다운로드
@app.get("/downloadfiles/{folder}/{filename}/")
def download_files(folder: str, filename: str):
    logger.info(f"app.py: Download request received for file: {filename} in folder: {folder}")
    
    # 허용된 폴더 목록으로 보안 강화
    allowed_folders = ['sentence', 'pdf_questions']
    if folder not in allowed_folders:
        logger.error(f"app.py: Forbidden folder access attempt: {folder}")
        raise HTTPException(status_code=403, detail="Forbidden folder")

    base_directory = os.getenv('DOWNLOAD_DIRECTORY', f'save_result/{folder}')
    # 경로 조작 공격 방지
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(base_directory, safe_filename)
    
    logger.info(f"app.py: Attempting to download file from path: {file_path}")
    
    if not os.path.isfile(file_path):
        # 만약 기본 경로에 파일이 없다면, 프로젝트 루트 기준으로 재시도
        # (save_result가 아닌 docs/save_result 등에 저장되는 경우 대비)
        alt_base_directory = os.path.join('docs', 'save_result', folder)
        file_path = os.path.join(alt_base_directory, safe_filename)
        logger.info(f"app.py: File not in primary path, trying alternative: {file_path}")
        if not os.path.isfile(file_path):
             logger.error(f"app.py: File not found at path: {file_path}")
             raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=filename)


# 사업부 드롭다운 데이터 가져오기
@app.get("/get-business-department")
async def get_dropdown_business_department():
    file_path = "/app/docs/public/business_department.xlsx"
    df = pd.read_excel(file_path, sheet_name="Sheet1")

    projects = df[["ProjectID", "ProjectName"]].dropna().to_dict(orient="records")

    return {"options": projects}

# 로그 데이터 반환 API
@app.get("/log")
async def get_logs():
    try:
        log_file_path = "/app/logs/debug.log"
        
        if not os.path.exists(log_file_path):
            logger.warning(f"app.py: Log file not found: {log_file_path}")
            return {"logs": [], "error": "Log file not found"}
        
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_lines = f.readlines()
        
        # 최근 500줄 반환 (더 많은 로그 표시)
        recent_logs = log_lines[-500:] if len(log_lines) > 500 else log_lines
        
        # 실제 로그 내용이 있는지 확인 (중요한 로그만 필터링)
        valid_logs = []
        for line in recent_logs:
            line = line.strip()
            if line and not line.startswith("returning"):
                # HTTP 디버그 로그 제외하고 중요한 로그만 포함
                if any(keyword in line for keyword in [
                    "INFO", "ERROR", "WARNING", "SUCCESS", "FAILED", 
                    "Milvus", "Azure", "RAG", "Question", "File", "Upload"
                ]):
                    valid_logs.append(line)
        
        # 로그 API 호출 메시지는 DEBUG 레벨로 변경 (화면에 표시되지 않음)
        logger.debug(f"app.py: Log data requested, returning {len(valid_logs)} filtered log lines")
        return {"logs": valid_logs}
        
    except Exception as e:
        logger.error(f"app.py: Error reading log file: {e}")
        return {"logs": [], "error": str(e)}

# mcp 연동 테스트 API
@app.get("/api/mcp")
async def get_mcp_data():
    mcp_file_path = os.path.join(os.path.dirname(__file__), ".gemini", "mcp_test.json")
    try:
        with open(mcp_file_path, 'r', encoding='utf-8') as f:
            mcp_data = json.load(f)
        logger.info(f"app.py: Successfully loaded MCP data from {mcp_file_path}")
        return JSONResponse(content=mcp_data)
    except FileNotFoundError:
        logger.error(f"app.py: MCP data file not found at: {mcp_file_path}")
        raise HTTPException(status_code=404, detail="MCP data file not found")
    except Exception as e:
        logger.exception("app.py: An error occurred while processing MCP data")
        raise HTTPException(status_code=500, detail=str(e))

# 컬렉션 관리 API
@app.get("/api/collections")
async def get_collections():
    """컬렉션 목록을 가져오는 API"""
    try:
        collections = list_collections()
        return JSONResponse(content={"collections": collections})
    except Exception as e:
        logger.error(f"❌ 컬렉션 목록 가져오기 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/collections/info")
async def get_collections_info():
    """컬렉션 상세 정보를 가져오는 API"""
    try:
        collections_info = get_collections_info()
        return JSONResponse(content={"collections_info": collections_info})
    except Exception as e:
        logger.error(f"❌ 컬렉션 정보 가져오기 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/collections/{collection_name}")
async def delete_collection(collection_name: str):
    """특정 컬렉션을 삭제하는 API"""
    try:
        clear_collection(collection_name)
        return JSONResponse(content={"success": True, "message": f"컬렉션 '{collection_name}' 삭제 완료"})
    except Exception as e:
        logger.error(f"❌ 컬렉션 삭제 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/collections")
async def delete_all_collections():
    """모든 컬렉션을 삭제하는 API"""
    try:
        clear_all_collections()
        return JSONResponse(content={"success": True, "message": "모든 컬렉션 삭제 완료"})
    except Exception as e:
        logger.error(f"❌ 모든 컬렉션 삭제 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/excel-rag/{filename}")
async def download_excel_rag(filename: str):
    """
    Excel RAG 결과 파일을 다운로드하는 엔드포인트
    """
    try:
        # 파일 경로 설정
        download_directory = os.getenv('DOWNLOAD_DIRECTORY', 'save_result')
        file_path = os.path.join(download_directory, 'answer', filename)
        
        logger.info(f"📥 Excel RAG 파일 다운로드 요청: {filename}")
        
        # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            logger.error(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다")
        
        # 파일 다운로드 응답
        return FileResponse(
            file_path, 
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Excel RAG 파일 다운로드 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"파일 다운로드 중 오류가 발생했습니다: {str(e)}")