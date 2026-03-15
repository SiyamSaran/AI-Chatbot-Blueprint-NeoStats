import os
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.config import OPENAI_API_KEY, GOOGLE_API_KEY

def get_embedding_model(provider="google"):
    """Initialize and return the embedding model"""
    try:
        if provider == "openai" and OPENAI_API_KEY:
            return OpenAIEmbeddings(api_key=OPENAI_API_KEY)
        elif provider == "google" and GOOGLE_API_KEY:
            # Let's try Google, but if the key is invalid (Maps API instead of Studio), this will fail during query.
            return GoogleGenerativeAIEmbeddings(api_key=GOOGLE_API_KEY, model="models/text-embedding-004")
        elif provider == "huggingface":
            # 100% Free Local Embeddings (Does not need API keys!)
            from langchain_huggingface import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        else:
            return None
    except Exception as e:
        print(f"Error initializing embedding model: {e}")
        return None
