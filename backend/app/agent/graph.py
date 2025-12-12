from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import parser_node, planner_node, batch_generator_node, aggregator_node
from app.services.debug_logger import DebugLogger
from typing import Callable, Dict, Any

def debug_wrapper(node_func: Callable, node_name: str):
    """
    包装节点函数以增加 Debug 日志功能。
    """
    def wrapped_node(state: AgentState) -> Dict:
        result = node_func(state)
        # 异步或同步写入日志
        DebugLogger.log_node_execution(node_name, state, result)
        return result
    return wrapped_node

# --- 1. 初始化图 ---
# StateGraph 是 LangGraph 的核心，它定义了状态的结构 (`AgentState`)。
workflow = StateGraph(AgentState)

# --- 2. 添加节点 ---
# 节点是执行具体逻辑的函数。它们接收当前状态，执行操作，并返回状态更新。

# Parser 节点：负责解析 OpenAPI 文档
# Parser 节点：负责解析 OpenAPI 文档
workflow.add_node("parser", debug_wrapper(parser_node, "parser"))

# Planner 节点：负责生成测试计划
# Planner 节点：负责生成测试计划
workflow.add_node("planner", debug_wrapper(planner_node, "planner"))

# Generator 节点：负责生成代码
# 注意：目前使用 batch_generator_node 串行处理所有生成任务以简化实现
workflow.add_node("generator", debug_wrapper(batch_generator_node, "generator"))

# Aggregator 节点：负责聚合代码
# Aggregator 节点：负责聚合代码
workflow.add_node("aggregator", debug_wrapper(aggregator_node, "aggregator"))

# --- 3. 定义边 (Edges) ---
# 边定义了节点之间的流转方向。

# 入口点：图执行开始时首先进入 parser 节点
workflow.set_entry_point("parser")

# 正常流程：Parser -> Planner
# 这里我们添加一个条件边（虽然目前是简单的线性流，但未来可以添加错误检查）
def check_parser_success(state: AgentState):
    if state.get("error"):
        return END # 如果解析失败，直接结束
    return "planner"

workflow.add_conditional_edges(
    "parser",
    check_parser_success,
    {
        "planner": "planner",
        END: END
    }
)

# Planner -> Generator
# 如果规划失败，也应该处理（简化起见这里直接流转，依靠后续错误处理）
def check_planner_success(state: AgentState):
    if state.get("error"):
        return END
    return "generator"

workflow.add_conditional_edges(
    "planner",
    check_planner_success,
    {
        "generator": "generator",
        END: END
    }
)

# Generator -> Aggregator
workflow.add_edge("generator", "aggregator")

# Aggregator -> END
workflow.add_edge("aggregator", END)

# --- 4. 编译图 ---
# 编译后的 app 可被直接调用 (`app.invoke(inputs)`)
agent_app = workflow.compile()
