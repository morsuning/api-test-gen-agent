import json
import os
import datetime
from typing import Any, Dict
from app.core.settings import SettingsManager

class DebugLogger:
    """
    负责在 Debug 模式开启时，将 LangGraph 节点的输入/输出写入日志文件。
    """
    
    @staticmethod
    def log_node_execution(node_name: str, input_state: Dict[str, Any], output_update: Dict[str, Any]):
        """
        记录节点执行信息。
        
        Args:
            node_name: 节点名称
            input_state: 节点接收到的输入状态 (执行前)
            output_update: 节点返回的状态更新 (执行后)
        """
        settings = SettingsManager.load_settings()
        
        if not settings.debug_mode:
            return
            
        log_path = settings.debug_log_path
        
        # 构造日志条目
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "node": node_name,
            # 为了避免日志过大，可以考虑只记录某些字段，或者全部记录
            # 这里记录 output_update，因为它反映了节点做了什么
            "output_update": DebugLogger._sanitize(output_update)
            # 如果需要，也可以记录 input_state 的摘要
        }
        
        log_entry_str = json.dumps(entry, ensure_ascii=False, indent=2)
        
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"--- Node Execution: {node_name} ---\n")
                f.write(log_entry_str)
                f.write("\n\n")
        except Exception as e:
            print(f"Failed to write debug log: {e}")

    @staticmethod
    def log_request(method: str, url: str, body: Any):
        """
        记录 API 请求日志到 Debug 文件。
        """
        settings = SettingsManager.load_settings()
        if not settings.debug_mode:
            return
            
        log_path = settings.debug_log_path
        
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "API_REQUEST",
            "method": method,
            "url": url,
            "body": DebugLogger._sanitize(body)
        }
        
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"--- API Request: {method} {url} ---\n")
                f.write(json.dumps(entry, ensure_ascii=False, indent=2))
                f.write("\n\n")
        except Exception as e:
            print(f"Failed to write debug log: {e}")

    @staticmethod
    def _sanitize(data: Any) -> Any:
        """
        简单的序列化辅助函数，处理非 JSON 可序列化对象。
        """
        if isinstance(data, dict):
            return {k: DebugLogger._sanitize(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [DebugLogger._sanitize(v) for v in data]
        elif hasattr(data, "dict"): # Pydantic models
            return data.dict()
        else:
            try:
                # 尝试默认转换
                json.dumps(data)
                return data
            except:
                return str(data)
