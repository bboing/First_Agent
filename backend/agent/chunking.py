import os
import tempfile
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import sys  
from pathlib import Path


def extract_text_from_document(file_path: str) -> str:
    """
    Azure Document Intelligence를 활용해 문서에서 텍스트를 추출합니다.
    Args:
        file_path (str): 분석할 문서 파일 경로
    Returns:
        str: 추출된 전체 텍스트
    """
    endpoint = os.getenv("AZURE_DI_ENDPOINT")
    key = os.getenv("AZURE_DI_KEY")
    client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-document", document=f, pages="1-9")
        result = poller.result()

    # 모든 페이지의 텍스트를 합침
    full_text = ""
    for page in result.pages:
        for line in page.lines:
            full_text += line.content + "\n"
    return full_text

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200):
    """
    긴 텍스트를 chunk_size 단위로 겹치게 분할합니다.
    Args:
        text (str): 전체 텍스트
        chunk_size (int): 청크 크기
        overlap (int): 청크 간 겹침 길이
    Returns:
        list[str]: 분할된 텍스트 청크 리스트
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def save_chunks_to_temp_file(chunks):
    """
    청킹된 텍스트를 임시 파일로 저장합니다.
    Args:
        chunks (list): 청킹된 텍스트 리스트
    Returns:
        str: 임시 파일 경로
    """
    # 임시 파일 생성
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
    temp_file_path = temp_file.name
    
    try:
        for i, chunk in enumerate(chunks):
            temp_file.write(f"--- Chunk {i+1} ---\n{chunk}\n\n")
        temp_file.close()
        print(f"chunking.py: ✅ 청킹 결과가 임시 파일에 저장되었습니다: {temp_file_path}")
        return temp_file_path
    except Exception as e:
        print(f"chunking.py: ❌ 임시 파일 저장 중 오류: {e}")
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        raise

def process_document_to_temp_file(file_path: str, chunk_size: int = 1000, overlap: int = 200):
    """
    문서를 청킹하고 임시 파일로 저장합니다.
    Args:
        file_path (str): 분석할 문서 파일 경로
        chunk_size (int): 청크 크기
        overlap (int): 청크 간 겹침 길이
    Returns:
        str: 임시 파일 경로
    """
    print(f"chunking.py: 📄 문서 처리 시작: {file_path}")
    
    # 1. 텍스트 추출
    print("chunking.py: 🔍 텍스트 추출 중...")
    text = extract_text_from_document(file_path)
    print(f"chunking.py: ✅ 텍스트 추출 완료 (총 {len(text)} 문자)")
    
    # 2. 청킹
    print("chunking.py: ✂️ 텍스트 청킹 중...")
    chunks = chunk_text(text, chunk_size, overlap)
    print(f"chunking.py: ✅ 청킹 완료 (총 {len(chunks)}개 청크)")
    
    # 3. 임시 파일로 저장
    print("chunking.py: 💾 임시 파일로 저장 중...")
    temp_file_path = save_chunks_to_temp_file(chunks)
    
    print(f"chunking.py: 🎉 청킹 완료! 임시 파일: {temp_file_path}")
    return temp_file_path

def extract_texts_by_page(file_path: str):
    """
    Azure Document Intelligence를 활용해 문서에서 페이지별 텍스트를 추출합니다.
    Returns:
        list[tuple(page_text:str, page_num:int)]
    """
    endpoint = os.getenv("AZURE_DI_ENDPOINT")
    key = os.getenv("AZURE_DI_KEY")
    client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-document", document=f, pages="1-9")
        result = poller.result()

    page_texts = []
    for idx, page in enumerate(result.pages):
        page_text = ""
        for line in page.lines:
            page_text += line.content + "\n"
        page_texts.append((page_text, idx+1))
    return page_texts

def chunk_by_paragraph_with_page_range(file_path: str, min_chunk_len: int = 200):
    """
    페이지별로 텍스트를 추출한 뒤, 의미 단위(문단)로 청킹하고,
    각 청크가 여러 페이지에 걸치면 page='1~2'와 같이 범위로 저장합니다.
    Returns:
        list[tuple(chunk_text:str, page_range:str)]
    """
    page_texts = extract_texts_by_page(file_path)
    paragraphs = []
    page_marks = []
    for text, page_num in page_texts:
        # 문단 단위로 쪼개기
        for para in text.split("\n\n"):
            para = para.strip()
            if para:
                paragraphs.append(para)
                page_marks.append(page_num)
    # 의미 단위로 묶기 (min_chunk_len 이상이 될 때까지 문단 합치기)
    chunks = []
    i = 0
    while i < len(paragraphs):
        chunk = paragraphs[i]
        start_page = page_marks[i]
        end_page = start_page
        j = i + 1
        while len(chunk) < min_chunk_len and j < len(paragraphs):
            chunk += '\n\n' + paragraphs[j]
            end_page = page_marks[j]
            j += 1
        if start_page == end_page:
            page_range = str(start_page)
        else:
            page_range = f"{start_page}~{end_page}"
        chunks.append((chunk, page_range))
        i = j
    return chunks

if __name__ == "__main__":
    # sub_lang/agent/chunking.py에서 sub_lang/docs/로 가는 상대경로
    file_path = "../docs/Customer Service_Booking_Manual.pdf"
    
    # 파일 존재 여부 확인
    if not os.path.exists(file_path):
        print(f"chunking.py: ❌ 파일을 찾을 수 없습니다: {file_path}")
        print(f"chunking.py: 현재 작업 디렉토리: {os.getcwd()}")
        print(f"chunking.py: 절대 경로: {os.path.abspath(file_path)}")
        exit(1)
    
    print(f"chunking.py: ✅ 파일을 찾았습니다: {file_path}")
    
    # 문서 처리 및 임시 파일 저장
    temp_file_path = process_document_to_temp_file(file_path, chunk_size=1000, overlap=200)
    
    print(f"chunking.py: 
📝 다음 명령어로 임베딩을 진행하세요:")
    print(f"chunking.py: python sub_lang/agent/embedding.py {temp_file_path}")