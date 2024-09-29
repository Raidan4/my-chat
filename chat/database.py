import sqlite3 

# Database Initialization
def init_db():
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  session_id TEXT NOT NULL,
                  question TEXT NOT NULL, 
                  answer TEXT NOT NULL, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Save a conversation
def save_conversation(session_id, question, answer):
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    c.execute("INSERT INTO conversations (session_id, question, answer) VALUES (?, ?, ?)", (session_id, question, answer))
    conn.commit()
    conn.close()

# Retrieve previous conversations
def get_conversations(session_id, page=1, page_size=10):
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    offset = (page - 1) * page_size
    c.execute("SELECT question, answer FROM conversations WHERE session_id = ? LIMIT ? OFFSET ?", (session_id, page_size, offset))
    data = c.fetchall()
    conn.close()
    return data

# Retrieve all unique session_ids
def get_all_sessions():
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT session_id FROM conversations")
    sessions = c.fetchall()
    conn.close()
    return [s[0] for s in sessions]  # Return list of session_ids
