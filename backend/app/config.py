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

# Application Configuration
APP_NAME = "MeetMind AI"
APP_VERSION = "0.1.0"
DEBUG = os.getenv("DEBUG", "True") == "True"

# CORS Configuration
CORS_ORIGINS = ["http://localhost:8501", "http://frontend:8501"]

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
