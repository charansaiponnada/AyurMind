

# --- REST Endpoints for History ---

@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Fetches the list of all conversations.
    NOTE: In a real multi-user app, this would be scoped to the logged-in user.
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row # This allows accessing columns by name
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, title, timestamp FROM conversations ORDER BY timestamp DESC")
        conversations = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return jsonify(conversations)
    except Exception as e:
        print(f"ERROR in /api/history: {e}")
        return jsonify({"error": "Failed to fetch history."}), 500

@app.route('/api/conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """
    Fetches all messages for a specific conversation.
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, sender, text, timestamp FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
            (conversation_id,)
        )
        messages = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return jsonify(messages)
    except Exception as e:
        print(f"ERROR in /api/conversation/{conversation_id}: {e}")
        return jsonify({"error": "Failed to fetch conversation."}), 500
