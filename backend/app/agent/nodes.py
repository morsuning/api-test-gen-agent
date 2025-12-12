import json
import re
import yaml
from typing import List, Dict, Any
from app.agent.state import AgentState
from app.services.parser_service import ParserService
from app.agent.prompts.factory import PromptFactory
from app.core.llm import get_llm
from app.models.schemas import TestCase, LLMConfig
from app.utils.json_parser import robust_json_parse
from langchain_core.messages import SystemMessage, HumanMessage

def parser_node(state: AgentState) -> Dict:
    """
    **解析器节点**
    
    职责:
    1. 解析输入的 OpenAPI 字符串。
    2. 验证格式。
    3. 生成简化版的 Spec Summary 供 LLM 使用。
    
    输出更新 State:
    - parse_result
    - spec_summary
    """
    print("--- 正在执行 Parser Node ---")
    content = state["openapi_spec_content"]
    
    try:
        # 1. 解析
        parsed = ParserService.parse_spec_content(content)
        # 2. 验证
        ParserService.validate_spec(parsed)
        # 3. 简化
        summary = ParserService.simplify_spec(parsed)
        
        return {
            "parse_result": parsed,
            "spec_summary": summary,
            "error": None
        }
    except Exception as e:
        return {"error": str(e)}

def planner_node(state: AgentState) -> Dict:
    """
    **规划器节点**
    
    职责:
    1. 获取用户配置 (LLM, Tier)。
    2. 选择合适的 Prompt 策略。
    3. 调用 LLM 生成测试计划列表。
    
    输出更新 State:
    - test_plan
    """
    print("--- 正在执行 Planner Node ---")
    spec_summary = state["spec_summary"]
    user_prefs = state["user_preferences"]
    
    # 构建 LLM Config 对象
    llm_config = LLMConfig(**user_prefs["llm_config"])
    llm = get_llm(llm_config)
    
    # 获取 Prompt 策略
    tier = llm_config.tier
    strategy = PromptFactory.get_strategy(tier)
    
    # 生成 Prompt
    prompt_text = strategy.plan_tests_prompt(spec_summary)
    
    # 调用 LLM
    try:
        response = llm.invoke([HumanMessage(content=prompt_text)])
        content = response.content
        
        # 清理 Output (提取 JSON)
        json_str = content
        
        # 1. 尝试提取 ```json ... ``` 或 ``` ... ```
        pattern = r"```(?:json)?\s*(.*?)```"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            
        # 2. 尝试寻找最外层的列表 [] 结构 (防止代码块外有额外文字)
        # 寻找第一个 [ 和最后一个 ]
        start = json_str.find('[')
        end = json_str.rfind(']')
        if start != -1 and end != -1 and end > start:
            json_str = json_str[start:end+1]
            
        # 解析 JSON (多策略尝试)
        # 解析 JSON (使用 Robust Parser)
        try:
            plan_data = robust_json_parse(json_str)
            # Ensure it is a list
            if not isinstance(plan_data, list):
                if isinstance(plan_data, dict):
                    plan_data = [plan_data]
                else:
                    raise ValueError("Parsed data is not a list or dict")
        except Exception as je:
             print(f"All parse attempts failed.")
             print(f"Raw Content: {content}")
             print(f"Extracted String: {json_str}")
             raise je

        test_cases = [TestCase(**item) for item in plan_data]
        
        return {"test_plan": test_cases}
    except Exception as e:
        print(f"Planner Error: {e}")
        error_msg = str(e)
        if "Expecting" in error_msg: # JSON error usually contains "Expecting"
             return {"error": f"Planning failed: LLM output is not valid JSON. Check logs for raw output. ({error_msg})"}
        if "404" in error_msg and "url" in error_msg:
             return {"error": f"Planning failed: LLM Endpoint not found (404). Please check your Base URL in Settings. (Original error: {error_msg})"}
        return {"error": f"Planning failed: {error_msg}"}

def generator_node(state: AgentState, test_case: TestCase) -> Dict:
    """
    **生成器节点**
    
    注意：此节点设计为在循环或映射中被调用。
    它不直接接收完整的 State 并返回更新的 State，而是处理单个 TestCase。
    但是在当前 LangGraph 简单的线性结构中，我们将它适配为：
    接收 State，处理其中 *一个* 待处理的任务，或者如果是并行映射，则逻辑略有不同。
    
    为了简化实现并适配 LangGraph 的 `Send` API (Map-Reduce)，
    我们假设这个函数被包装在一个可以并行调用的结构中。
    
    但在基础版本中，我们通过一个循环在图中顺序或并行执行。
    这里实现为：接收单个 TestCase 和 上下文，返回生成的代码。
    
    **实际 LangGraph 实现路径：**
    我们会使用 LangGraph 的 conditional edges 来实现 Map-Reduce。
    或者简单地，在此节点内部循环生成（如果不追求并行性能）。
    
    为了演示 LangGraph 的逻辑，我们这里依然将其写为处理单个 Case 的逻辑，
    稍后在 graph.py 中通过 `Send` API 进行并行调度。
    """
    # 注意：这只是一个逻辑单元，graph.py 中会定义如何调度它
    pass

# 由于 LangGraph 的 Map-Reduce 模式（Send API）需要特定的节点签名，
# 我们重新定义 generator 逻辑以适配。
# 这里的 generator_step 将接收 state 和 特定的 test_case 参数

def generate_single_case(state: AgentState, test_case_id: str):
    """
    辅助函数：生成单个用例的代码。
    """
    # Find the case
    case = next((c for c in state["test_plan"] if c.id == test_case_id), None)
    if not case:
        return None, "Case not found"
        
    spec_summary = state["spec_summary"]
    user_prefs = state["user_preferences"]
    target_language = user_prefs["target_language"]
    
    llm_config = LLMConfig(**user_prefs["llm_config"])
    llm = get_llm(llm_config)
    strategy = PromptFactory.get_strategy(llm_config.tier)
    
    prompt = strategy.generate_code_prompt(case, spec_summary, target_language)
    
    try:
        resp = llm.invoke([HumanMessage(content=prompt)])
        code = resp.content
        # 简单清理
        if "```" in code:
            lines = code.split("\n")
            # 移除第一行 ```language 和最后一行 ```
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            code = "\n".join(lines)
        return code, None
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg and "url" in error_msg:
            return None, f"LLM 404 Error: Check Base URL. ({error_msg})" 
        return None, error_msg

def batch_generator_node(state: AgentState) -> Dict:
    """
    **批量生成器节点**
    
    为了简化，我们先在一个节点内串行生成所有代码。
    未来优化：使用 LangGraph 的 Map-Reduce 并行生成。
    
    输出更新 State:
    - generated_code_map
    """
    print("--- 正在执行 Batch Generator Node ---")
    test_plan = state["test_plan"]
    code_map = {}
    
    for case in test_plan:
        print(f"Generating code for case: {case.id}")
        code, err = generate_single_case(state, case.id)
        if code:
            code_map[case.id] = code
        else:
            code_map[case.id] = f"// Error generating code: {err}"
            

    return {"generated_code_map": code_map}

def aggregator_node(state: AgentState) -> Dict:
    """
    **聚合器节点**
    
    职责:
    1. 收集所有生成的代码片段。
    2. 根据目标语言，组装成最终的可执行文件内容 (添加 Imports, Main 函数等)。
    
    输出更新 State:
    - final_output
    """
    print("--- 正在执行 Aggregator Node ---")
    code_map = state.get("generated_code_map", {})
    test_plan = state.get("test_plan", [])
    user_prefs = state.get("user_preferences", {})
    target_language = user_prefs.get("target_language", "curl")
    
    final_output = ""
    
    print(f"Aggregator: Test Plan size: {len(test_plan)}")
    
    if target_language == "go":
        # Go 语言聚合策略
        final_output += "package main\n\n"
        final_output += "import (\n"
        final_output += "\t\"testing\"\n"
        final_output += "\t\"net/http\"\n"
        final_output += "\t\"net/http/httptest\"\n"
        final_output += "\t\"strings\"\n"
        final_output += "\t\"encoding/json\"\n"
        final_output += ")\n\n"
        
        for case in test_plan:
            code = code_map.get(case.id, "")
            if code:
                # 确保代码片段没有 package main 或多余的 imports
                # 简单清理：如果包含 package main，移除之
                if "package main" in code:
                    code = code.replace("package main", "")
                # 移除 import 块 (假设每个片段都有，这里简单粗暴做展示，实际应更智能解析)
                # 更好的做法是在 Prompt 中要求不生成 package/import
                
                final_output += f"// Test Case: {case.name} ({case.id})\n"
                final_output += code + "\n\n"
                
    elif target_language == "java":
        # Java 语言聚合策略 (RestAssured)
        final_output += "import org.junit.Test;\n"
        final_output += "import static io.restassured.RestAssured.*;\n"
        final_output += "import static org.hamcrest.Matchers.*;\n\n"
        final_output += "public class ApiTest {\n\n"
        
        for case in test_plan:
            code = code_map.get(case.id, "")
            if code:
                final_output += f"    // Test Case: {case.name} ({case.id})\n"
                # 缩进处理
                indented_code = "\n".join(["    " + line for line in code.split("\n")])
                final_output += indented_code + "\n\n"
                
        final_output += "}\n"
        
    else:
        # Default / cURL
        for case in test_plan:
            code = code_map.get(case.id, "")
            if code:
                final_output += f"# Test Case: {case.name} ({case.id})\n"
                final_output += code + "\n\n"
                
    return {"final_output": final_output}
