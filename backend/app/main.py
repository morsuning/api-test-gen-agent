from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import router as api_router
import logging
import sys
import json
from app.utils.logger_utils import recursive_decode_json
from app.core.settings import SettingsManager
from app.services.debug_logger import DebugLogger

app = FastAPI(title="API Test Case Generation Agent", version="1.0.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允许所有来源，生产环境应限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("api_logger")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录所有请求的详细信息 (Debug用)"""
    # 1. Check Debug Mode from Settings
    try:
        settings = SettingsManager.load_settings()
        is_debug = settings.debug_mode
    except Exception:
        is_debug = False
        
    logger.info(f"Started: {request.method} {request.url}")
    
    if is_debug:
        try:
            # 读取 Body (注意: 会消耗 Stream, 需要重新构造)
            body = await request.body()
            if body:
                try:
                    # Try initial JSON load
                    json_body = json.loads(body)
                    # Use recursive decode to clean up nested JSON strings
                    clean_body = recursive_decode_json(json_body)
                    
                    # Log to Debug File
                    DebugLogger.log_request(request.method, str(request.url), clean_body)
                    
                    # Optionally still log to console info if needed, but avoiding duplication
                    logger.info(f"debug_mode=True. Request logged to debug file.")
                except:
                    logger.info(f"Request Body: {body.decode('utf-8', errors='replace')}")
            
            # 重置 Body 供后续使用
            async def receive():
                return {"type": "http.request", "body": body, "more_body": False}
            request._receive = receive
            
        except Exception as e:
            logger.error(f"Error reading body: {e}")
    else:
        # If not debug mode, maybe don't log body or log only minimal info?
        # Current behavior implies we should skip detailed body logging if control is desired.
        pass

    response = await call_next(request)
    logger.info(f"Completed: Status {response.status_code}")
    return response

# 注册路由
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}
