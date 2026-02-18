import React, { useState, useEffect } from 'react';
import './HistorySidebar.css';

interface Conversation {
  id: string;
  title: string;
  timestamp: number;
}

interface HistorySidebarProps {
  activeConversationId: string | null;
  onConversationSelect: (id: string) => void;
  onNewConversation: () => void;
}

const HistorySidebar: React.FC<HistorySidebarProps> = ({ 
  activeConversationId, 
  onConversationSelect,
  onNewConversation
}) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/history');
        if (!response.ok) {
          throw new Error('Failed to fetch conversation history.');
        }
        const data = await response.json();
        setConversations(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred.');
        console.error(err);
      }
    };

    fetchHistory();
  }, [needsRefresh]);

  return (
    <aside className="history-sidebar">
      <div className="sidebar-header">
        <button onClick={onNewConversation} className="new-chat-button">
          + New Chat
        </button>
      </div>
      <div className="conversation-list">
        {error && <p style={{color: 'red', padding: '1rem'}}>Error: {error}</p>}
        {conversations.map(convo => (
          <div
            key={convo.id}
            className={`conversation-item ${convo.id === activeConversationId ? 'active' : ''}`}
            onClick={() => onConversationSelect(convo.id)}
            title={convo.title}
          >
            {convo.title}
          </div>
        ))}
      </div>
    </aside>
  );
};

export default HistorySidebar;
