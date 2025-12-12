from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.schemas import GenerateRequest, GenerateResponse, TestCase
from app.core.settings import SettingsManager, AppSettings
from app.agent.graph import agent_app
from langchain_core.messages import HumanMessage
import uuid
import traceback

router = APIRouter()

@router.get("/settings", response_model=AppSettings)
async def get_settings():
    """获取当前全局配置"""
    return SettingsManager.load_settings()

@router.post("/settings", response_model=AppSettings)
async def save_settings(settings: AppSettings):
    """保存全局配置"""
    SettingsManager.save_settings(settings)
    return settings

@router.post("/generate", response_model=GenerateResponse)
async def generate_test_cases(request: GenerateRequest):
    """
    触发测试用例生成工作流。
    """
    task_id = str(uuid.uuid4())
    
    # 构建初始状态
    initial_state = {
        "openapi_spec_content": request.openapi_content,
        "user_preferences": {
            "target_language": request.target_language,
            "llm_config": request.llm_config.dict(),
            "include_boundary": request.include_boundary,
            "include_negative": request.include_negative
        },
        # 初始化其他字段为空
        "parse_result": {},
        "spec_summary": "",
        "test_plan": [],
        "generated_code_map": {},
        "final_output": "",
        "error": None
    }
    
    try:
        # 调用 LangGraph
        # 注意: 这里是同步调用 invoke，生产环境对于长时间任务应使用后台任务或异步队列
        print(f"Starting workflow for task {task_id}")
        final_state = agent_app.invoke(initial_state)
        
        if final_state.get("error"):
            return GenerateResponse(
                task_id=task_id,
                status="failed",
                error=final_state["error"]
            )
            
        result_data = {
            "test_plan": [case.dict() for case in final_state.get("test_plan", [])],
            "generated_code": final_state.get("generated_code_map", {})
        }
        
        return GenerateResponse(
            task_id=task_id,
            status="completed",
            result=result_data
        )
        
    except Exception as e:
        print(f"Workflow execution failed: {e}")
        return GenerateResponse(
            task_id=task_id,
            status="failed",
            error=str(e)
        )
