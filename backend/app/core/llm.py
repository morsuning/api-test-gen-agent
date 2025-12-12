from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.schemas import LLMConfig
import os

def get_llm(config: LLMConfig):
    """
    获取通用的 ChatOpenAI 实例。
    所有厂商 (DeepSeek, Qwen, Google-via-OpenAI) 都应兼容 OpenAI 格式。
    """
    base_url = config.base_url.strip()
    if base_url.endswith("/chat/completions"):
        base_url = base_url[:-17]  # Remove /chat/completions
    
    # Remove trailing slash to be safe, though OpenAI client usually handles it
    base_url = base_url.rstrip("/")

    return ChatOpenAI(
        model=config.model_name,
        api_key=config.api_key,
        base_url=base_url,
        temperature=0.2
    )
