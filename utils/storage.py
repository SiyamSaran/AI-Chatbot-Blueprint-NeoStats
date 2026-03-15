import json
import os
import uuid
from datetime import datetime

STORAGE_FILE = "all_chat_sessions.json"

def get_all_sessions():
    """Loads all chat sessions from the local JSON file."""
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure it's a dictionary
                return data if isinstance(data, dict) else {}
        except Exception as e:
            print(f"Error loading sessions: {e}")
            return {}
    return {}

def save_session(session_id, messages, title=None):
    """Saves a specific chat session."""
    sessions = get_all_sessions()
    
    # If it's a new session and no title provided, use first 30 chars of first user message
    if not title and session_id in sessions:
        title = sessions[session_id].get("title", "New Chat")
    elif not title:
        title = "New Chat"
        for m in messages:
            if m["role"] == "user":
                title = m["content"][:30] + ("..." if len(m["content"]) > 30 else "")
                break
    
    sessions[session_id] = {
        "title": title,
        "messages": messages,
        "updated_at": datetime.now().isoformat()
    }
    
    try:
        with open(STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(sessions, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving session: {e}")

def delete_session(session_id):
    """Deletes a specific chat session."""
    sessions = get_all_sessions()
    if session_id in sessions:
        del sessions[session_id]
        with open(STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(sessions, f, ensure_ascii=False, indent=4)

def clear_all_storage():
    """Deletes all history data."""
    if os.path.exists(STORAGE_FILE):
        os.remove(STORAGE_FILE)
