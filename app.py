import streamlit as st
import os
import sys
import uuid
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from models.llm import get_chatgroq_model
from models.embeddings import get_embedding_model
from utils.rag import process_file_to_vectorstore, retrieve_rag_context
from utils.search import perform_web_search
from utils.export import export_chat_to_pdf
from utils.storage import get_all_sessions, save_session, delete_session, clear_all_storage

def apply_custom_styles():
    """Apply the Professional Light White & Ash (Gray) theme"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Inter', sans-serif;
            color: #1A1A1A !important;
        }

        /* Clean White App Background */
        .stApp {
            background-color: #FFFFFF !important;
            background-image: none !important;
        }
        
        /* Light Gray (Ash) Top Header */
        header[data-testid="stHeader"] {
            background: #F8F9FA !important;
            border-bottom: 2px solid #E9ECEF;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }

        /* Sidebar - Soft Ash Gray */
        [data-testid="stSidebar"] {
            background-color: #F1F3F5 !important;
            border-right: 1px solid #DEE2E6;
        }
        
        /* Sidebar Headings */
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] .stSubheader {
            color: #212529 !important;
            border-bottom: 2px solid #ADB5BD;
            padding-bottom: 8px !important;
            font-weight: 600 !important;
        }
        
        /* Sidebar Text & Labels */
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
            color: #495057 !important;
            font-weight: 500 !important;
        }

        /* Minimalist Chat Bubbles */
        [data-testid="stChatMessage"] {
            background-color: #F8F9FA !important;
            border: 1px solid #E9ECEF !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            margin-bottom: 1.2rem !important;
            color: #212529 !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.02);
        }
        
        /* AI Response - Subtle Ash Highlight */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageHeader"]:contains("assistant")) {
            background-color: #E9ECEF !important;
        }
        
        /* User Message - Clean White */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageHeader"]:contains("user")) {
            background-color: #FFFFFF !important;
            border: 1px solid #DEE2E6 !important;
        }

        /* Buttons - Modern Ash Gray */
        .stButton button, .stDownloadButton button {
            background-color: #E9ECEF !important;
            color: #212529 !important;
            border: 1px solid #CED4DA !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease;
        }
        
        .stButton button:hover, .stDownloadButton button:hover {
            background-color: #DEE2E6 !important;
            border-color: #ADB5BD !important;
            color: #000000 !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05) !important;
            transform: translateY(-1px);
        }

        /* Chat Input - Premium White & Ash */
        [data-testid="stChatInput"] {
            background-color: #FFFFFF !important;
            border: 2px solid #DEE2E6 !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        }

        [data-testid="stChatInput"] textarea {
            background-color: #F8F9FA !important;
            color: #212529 !important; 
            -webkit-text-fill-color: #212529 !important;
            font-size: 1.1rem !important;
            padding: 12px 14px !important;
            caret-color: #495057 !important;
        }

        [data-testid="stChatInput"] textarea::placeholder {
            color: #ADB5BD !important;
            opacity: 1 !important;
        }

        /* Bottom Housing Area */
        [data-testid="stBottom"] {
            background-color: #FFFFFF !important;
            border-top: 1px solid #E9ECEF !important;
        }
        
        [data-testid="stBottomBlockContainer"] {
            background-color: #FFFFFF !important;
        }

        /* Toggle Switches */
        button[role="switch"] {
            border: 1px solid #ADB5BD !important;
            background-color: #DEE2E6 !important;
        }

        /* File Uploader - Light Professional Design */
        [data-testid="stFileUploader"] {
            background-color: #F8F9FA !important;
            border: 2px dashed #CED4DA !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
        }
        
        [data-testid="stFileUploader"]:hover {
            background-color: #E9ECEF !important;
            border-color: #ADB5BD !important;
        }
        
        [data-testid="stFileUploader"] label {
            color: #212529 !important;
            font-weight: 600 !important;
        }
        
        /* Markdown Text Color */
        .stMarkdown p, .stMarkdown li, .stMarkdown span {
            color: #212529 !important;
        }

        /* Sidebar Download Button Styling */
        div.stDownloadButton {
            text-align: right;
        }
        
        div.stDownloadButton button {
            background-color: #E9ECEF !important;
            border: 1px solid #CED4DA !important;
            color: #212529 !important;
            border-radius: 8px !important;
            width: 35px !important;
            height: 35px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            font-size: 1rem !important;
            transition: all 0.2s ease !important;
        }
        
        div.stDownloadButton button:hover {
            background-color: #DEE2E6 !important;
            border-color: #ADB5BD !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
        }
        </style>
    """, unsafe_allow_html=True)

def get_chat_response(chat_model, messages, system_prompt):
    """Get response from the chat model"""
    try:
        formatted_messages = [SystemMessage(content=system_prompt)]
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))
        response = chat_model.invoke(formatted_messages)
        return response.content
    except Exception as e:
        return f"Error getting response: {str(e)}"

def chat_page(response_mode, use_web_search, document_name=None):
    """Main chat interface page"""
    st.title("🤖 AI ChatBot")
    
    system_prompt = "You are a helpful AI assistant. "
    
    # Source Identification & Fallback Logic
    doc_label = f"from {document_name}" if document_name else "the Given Document"
    system_prompt += (
        "\n\nCRITICAL INSTRUCTIONS:\n"
        "1. Read the 'Context from file' (if provided) first.\n"
        "2. If you find the answer in the file context, start your response with '**[from " + doc_label + "]**'.\n"
        "3. ONLY if the answer is NOT found in the file context, look at the 'Web context' (if provided).\n"
        "4. If you use the web context, start your response with '**[from the web]**'.\n"
        "5. If neither context provides the answer, use your internal knowledge and start with '**[from AI Knowledge]**'.\n"
        "6. ALWAYS prioritize the document over the web."
    )
    
    if response_mode == "Concise":
        system_prompt += "\n\nYour replies must be very concise."
    else:
        system_prompt += "\n\nYour replies must be highly detailed."
        
    chat_model = get_chatgroq_model()
    
    # Load messages for the current session
    all_sessions = get_all_sessions()
    if st.session_state.session_id in all_sessions:
        st.session_state.messages = all_sessions[st.session_state.session_id]["messages"]
    else:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if chat_model is None:
        st.info("🔧 No API keys found! Please set them up in your .env file.")
    else:
        if prompt := st.chat_input("Type your message here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            save_session(st.session_state.session_id, st.session_state.messages)
            
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                with st.spinner("Getting response..."):
                    augmented_prompt = system_prompt
                    if st.session_state.vectorstore:
                        rag_context = retrieve_rag_context(st.session_state.vectorstore, prompt)
                        if rag_context:
                            augmented_prompt += f"\n\nContext from file:\n{rag_context}"
                    
                    if use_web_search:
                        web_context = perform_web_search(prompt)
                        augmented_prompt += f"\n\nWeb context:\n{web_context}"
                    
                    response = get_chat_response(chat_model, st.session_state.messages, augmented_prompt)
                    st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            save_session(st.session_state.session_id, st.session_state.messages)

def main():
    st.set_page_config(
        page_title="NEO ChatBot - Professional AI",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    apply_custom_styles()
    
    # Initialize session state variables
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    with st.sidebar:
        # 1. Web Search & Download Header
        col_title, col_dl = st.columns([0.8, 0.2])
        with col_title:
            st.subheader("🌐 Web Search")
        
        # Calculate messages for download
        sessions = get_all_sessions()
        current_messages = []
        if st.session_state.get("session_id") in sessions:
            current_messages = sessions[st.session_state.session_id]["messages"]
        elif st.session_state.get("messages"):
            current_messages = st.session_state.messages

        if current_messages:
            with col_dl:
                pdf_data = export_chat_to_pdf(current_messages)
                st.download_button(
                    label="⬇️",
                    data=pdf_data,
                    file_name=f"chat_{st.session_state.get('session_id', 'export')[:8]}.pdf",
                    mime="application/pdf",
                    key="header_download"
                )

        use_web_search = st.toggle("Enable Live Web Search")
        st.divider()

        # 2. New Chat
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()
            
        st.divider()
        
        # 3. Chat History
        st.subheader("💬 Chat History")
        sessions = get_all_sessions()
        if sessions:
            for sid, sdata in sorted(sessions.items(), key=lambda x: x[1].get('updated_at', ''), reverse=True):
                col1, col2 = st.columns([0.8, 0.2])
                if col1.button(sdata.get('title', 'Untitled'), key=sid, use_container_width=True):
                    st.session_state.session_id = sid
                    st.rerun()
                if col2.button("🗑️", key=f"del_{sid}"):
                    delete_session(sid)
                    if st.session_state.get("session_id") == sid:
                        st.session_state.session_id = str(uuid.uuid4())
                    st.rerun()
            
        st.divider()

        # 4. Response Mode
        st.subheader("⚙️ Settings")
        response_mode = st.radio("Response Mode", ["Concise", "Detailed"])
        st.divider()

        # 5. Document Query
        st.subheader("📄 Document Query (RAG)")
        uploaded_file = st.file_uploader("Upload a PDF to chat with it", type="pdf")
        if uploaded_file and st.button("Process Document"):
            with st.spinner("Processing document..."):
                embed_model = get_embedding_model(provider="huggingface")
                if not embed_model:
                    embed_model = get_embedding_model(provider="google")
                if embed_model:
                    vectorstore = process_file_to_vectorstore(uploaded_file, embed_model)
                    if vectorstore:
                        st.session_state.vectorstore = vectorstore
                        st.success("Document indexed!")
                    else:
                        st.error("Failed to process document.")
                else:
                    st.error("No embedding API key found.")

    chat_page(response_mode, use_web_search, uploaded_file.name if uploaded_file else None)

if __name__ == "__main__":
    main()