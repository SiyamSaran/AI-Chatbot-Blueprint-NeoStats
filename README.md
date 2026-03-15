# 🤖 NeoStats AI ChatBot

A professional, feature-rich AI ChatBot built with **Streamlit** and **LangChain**. This application supports Retrieval-Augmented Generation (RAG) for document querying, live web searching, chat session management, and exporting conversations to PDF.

## 🌟 Features

- **Multi-Source Intelligence**:
  - **RAG (Retrieval-Augmented Generation)**: Upload a PDF and chat directly with its content using FAISS vector storage.
  - **Live Web Search**: Toggle real-time web search capabilities powered by Tavily.
  - **AI Knowledge**: Built-in general knowledge from Groq-hosted LLMs (like Llama 3).
- **Session Management**: 
  - Save, delete, and switch between multiple chat sessions.
  - Automatic persistent storage of chat history.
- **Advanced Export**: Download your entire chat session as a clean, professionally formatted PDF.
- **Customizable UI**: 
  - Sleek, modern "Professional Light White & Ash" theme.
  - Response mode toggles (Concise vs. Detailed).
- **Multi-Provider Support**: Integrates with Groq, Google Generative AI, and Hugging Face.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Framework**: LangChain
- **Orchestration**: Python Dotenv
- **Vector Database**: FAISS
- **Search API**: Tavily
- **Embeddings**: HuggingFace / Google AI
- **LLM**: Groq (Llama 3 / Mixtral)

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- [Groq API Key](https://console.groq.com/)
- [Google API Key](https://aistudio.google.com/) (Optional, for embeddings)
- [Tavily API Key](https://tavily.com/) (Optional, for web search)

### 2. Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/neostats-chatbot.git
   cd neostats-chatbot
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration

1. Create a `.env` file in the root directory (or rename `.env.example`):
   ```bash
   cp .env.example .env
   ```
2. Fill in your API keys in the `.env` file:
   ```env
   GROQ_API_KEY=your_key_here
   GOOGLE_API_KEY=your_key_here
   TAVILY_API_KEY=your_key_here
   ```

### 4. Running the App

```bash
streamlit run app.py
```

---

## 🔒 Security Note
This project uses a `.gitignore` file to ensure that your private `.env` file and API keys are **never** uploaded to GitHub. Always keep your keys secret!

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
