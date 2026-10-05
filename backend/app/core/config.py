
import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    database_url: str = os.getenv('DATABASE_URL', 'sqlite:///./dev.db')
    llm_provider: str = (os.getenv('LLM_PROVIDER') or 'openai').lower()
    openai_api_key: Optional[str] = os.getenv('OPENAI_API_KEY')
    groq_api_key: Optional[str] = os.getenv('GROQ_API_KEY')
    groq_base_url: str = os.getenv('GROQ_BASE_URL', 'https://api.groq.com/openai/v1')
    groq_model: str = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
    frontend_origin: Optional[str] = os.getenv('FRONTEND_ORIGIN')
    langsmtih_api_key: Optional[str] = os.getenv('LANGSMITH_API_KEY')
    langgraph_api_key: Optional[str] = os.getenv('LANGGRAPH_API_KEY')
    port: int = int(os.getenv('PORT') or 8000)


settings = Settings()
