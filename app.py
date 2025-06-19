from logger_config import setup_logging
import logging
setup_logging()
logger = logging.getLogger(__name__)

from agent.rag_agent import handle_rag
import os
import re
import openpyxl
import json
import pandas as pd
import uvicorn
import test
import random
import ast
import auto_generator.sentence_generator
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from typing import Union
from tempfile import NamedTemporaryFile
from enum import Enum
from pydantic import BaseModel

if __name__ == "__main__" :
    uvicorn.run("app:app", host = "0.0.0.0", port=8000, reload = True)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS 허용 (로컬 프론트엔드 개발 시 필요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 서비스 시에는 도메인 제한 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    answer = handle_rag(req.question)
    return {"answer": answer}

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running!"}

@app.get("/chat-ui", response_class=HTMLResponse)
async def chat_ui(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request}) 

@app.get("/RAG_Management", response_class=HTMLResponse)
async def RAG_Management(request: Request):
    return templates.TemplateResponse("RAG_Management.html", {"request": request})

@app.get("/learning-data", response_class=HTMLResponse)
async def get_learning_data(request: Request):
    return templates.TemplateResponse("learning-data.html",{"request" : request, "title" : "Learning Data Input"})


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
                logger.error(f"File with invalid extension uploaded: {upload_file.filename}")
                raise ValueError(f"Invalid file extension for {upload_file.filename}")
            temp_file = NamedTemporaryFile(delete=False, suffix=".xlsx")
            with open(temp_file.name, 'wb') as f:
                while True:
                    chunk = await upload_file.read(1024 * 1024)  # 1MB chunks
                    if not chunk:
                        break
                    f.write(chunk)
            logger.info(f"File saved to temporary location: {temp_file.name}")
            return temp_file.name

        # Q&A Set(질답셋) 저장
        file_path = await save_file_to_temp(file1)
        
        # Entity Dict(엔티티 사전) 저장
        file_path2 = await save_file_to_temp(file2)

        # 데이터 프레임 로드 및 검증
        df = pd.read_excel(file_path)
        edf = pd.read_excel(file_path2)
        
        if (df.columns[0] != 'Answer') and (edf.columns[0] != 'Entry'):
            logger.warning("File contents do not meet the expected format")
            raise ValueError("File contents do not meet expected format")

        # 데이터 저장 (project_id 제거)
        result = auto_generator.sentence_generator.Save_data(field_business, user_type, df, edf, Constraints)
        logger.info(f"Save_data result: {result}")
        if not result or 'file_name' not in result:
            logger.error(f"Returned result does not contain file_name! result: {result}")
        logger.info("Data successfully saved.")
        return result

    except ValueError as e:
        logger.exception("A value error occurred")
        return {"error": str(e)}
    except Exception as e:
        logger.exception("An unexpected error occurred")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 임시 파일 삭제
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Temporary file {file_path} deleted.")
        if 'file_path2' in locals() and os.path.exists(file_path2):
            os.remove(file_path2)
            logger.info(f"Temporary file {file_path2} deleted.")


# 학습데이터 결과 파일 다운로드
@app.get("/downloadfiles/sentence/{filename}/")
def download_files(filename: str):
    logger.info(f"Download request received for file: {filename}")
    
    base_directory = os.getenv('DOWNLOAD_DIRECTORY', 'save_result/sentence')
    filenames = os.path.basename(filename)
    file_path = os.path.join(base_directory, filenames)  # 안전한 파일 경로 생성
    
    logger.info(f"Attempting to download file from path: {file_path}")
    
    if not os.path.isfile(file_path):
        logger.error(f"File not found at path: {file_path}")
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=filename)


# 사업부 드롭다운 데이터 가져오기
@app.get("/get-business-department")
async def get_dropdown_business_department():
    file_path = "./docs/public/business_department.xlsx"
    df = pd.read_excel(file_path, sheet_name="Sheet1")

    projects = df[["ProjectID", "ProjectName"]].dropna().to_dict(orient="records")

    return {"options": projects}

# 로그 데이터 반환 API
@app.get("/api/log")
async def get_logs():
    try:
        log_file_path = os.path.join(os.path.dirname(__file__), "logs", "debug.log")
        
        if not os.path.exists(log_file_path):
            logger.warning(f"Log file not found: {log_file_path}")
            return {"logs": [], "error": "Log file not found"}
        
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_lines = f.readlines()
        
        # 최근 100줄만 반환 (성능 고려)
        recent_logs = log_lines[-100:] if len(log_lines) > 100 else log_lines
        
        logger.info(f"Log data requested, returning {len(recent_logs)} lines")
        return {"logs": recent_logs}
        
    except Exception as e:
        logger.error(f"Error reading log file: {e}")
        return {"logs": [], "error": str(e)}