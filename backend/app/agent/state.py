from typing import List, Dict, TypedDict, Annotated
import operator
from app.models.schemas import TestCase, LLMConfig

class AgentState(TypedDict):
    """
    LangGraph 的状态定义。
    包含在图执行过程中需要在节点之间传递的所有数据。
    """
    
    # 原始输入
    openapi_spec_content: str  # 原始 OpenAPI 字符串
    parse_result: Dict         # 解析后的 OpenAPI 字典
    
    # 无需 LLM 处理的静态数据
    spec_summary: str          # 简化后的 Spec，用于 Prompt
    user_preferences: Dict     # 用户偏好 (语言, 模型配置等)
    
    # 动态生成的数据
    test_plan: List[TestCase]  # 测试计划列表 (由 Planner 生成)
    
    # 生成的代码映射 (Map-Reduce 阶段使用)
    # key: test_case_id, value: generated_code
    generated_code_map: Dict[str, str] 
    
    # 最终输出
    final_output: str          # 组合后的最终代码文件内容
    error: str                 # 错误信息 (如果有)

# 注意: LangGraph 的 StateGraph 可能需要 Annotated 来定义 reducer
# 例如: generated_code_map: Annotated[Dict[str, str], merge_dicts]
# 这里为了简单起见暂未添加 reducer，因为主要流程是线性的或 map-reduce
