import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# Default Models
GROQ_DEFAULT_MODEL = "llama-3.1-8b-instant"
OPENAI_DEFAULT_MODEL = "gpt-3.5-turbo"
GEMINI_DEFAULT_MODEL = "gemini-1.5-flash"
