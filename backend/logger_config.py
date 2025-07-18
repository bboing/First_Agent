import logging
import os

def setup_logging():
    log_dir = "/app/logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "debug.log")
    
    # 루트 로거 설정
    logging.basicConfig(
        level=logging.DEBUG,  # DEBUG로 임시 변경
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    
    # HTTP 라이브러리들의 로그 레벨을 높여서 불필요한 디버그 로그 제거
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    # 애플리케이션 로거는 INFO 레벨 유지
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.INFO) 