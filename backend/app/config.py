import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://meetmind_user:meetmind_password@db:5432/meetmind_db"
)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_BASE = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")

# Pick AI model provider
AI_API_KEY = OPENROUTER_API_KEY or OPENAI_API_KEY
AI_API_BASE = OPENROUTER_API_BASE if OPENROUTER_API_KEY else None
AI_MODEL = os.getenv("AI_MODEL") or (OPENROUTER_MODEL if OPENROUTER_API_KEY else OPENAI_MODEL)

# Application Configuration
APP_NAME = "MeetMind AI"
APP_VERSION = "0.1.0"
DEBUG = os.getenv("DEBUG", "True") == "True"

# CORS Configuration
CORS_ORIGINS = ["http://localhost:8501", "http://frontend:8501"]

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
