import os
from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY, GROQ_DEFAULT_MODEL

def get_chatgroq_model():
    """Initialize and return the Groq chat model"""
    try:
        if not GROQ_API_KEY:
            return None
        # Initialize the Groq chat model with the API key
        groq_model = ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_DEFAULT_MODEL,
        )
        return groq_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Groq model: {str(e)}")