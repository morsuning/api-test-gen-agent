from abc import ABC, abstractmethod
from typing import List
from app.models.schemas import TestCase

class IPromptStrategy(ABC):
    """提示词策略接口"""

    @abstractmethod
    def plan_tests_prompt(self, spec_summary: str) -> str:
        """生成测试计划的提示词"""
        pass

    @abstractmethod
    def generate_code_prompt(self, case: TestCase, spec_summary: str, language: str) -> str:
        """生成代码的提示词"""
        pass

class PromptFactory:
    """提示词策略工厂"""

    @staticmethod
    def get_strategy(tier: str) -> IPromptStrategy:
        from app.agent.prompts.high_tier import HighTierStrategy
        from app.agent.prompts.low_tier import LowTierStrategy
        
        if tier == "high":
            return HighTierStrategy()
        elif tier == "low":
            return LowTierStrategy()
        else:
            return HighTierStrategy() # 默认使用高级策略
