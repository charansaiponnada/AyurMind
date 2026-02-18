import React, { useState, useEffect, useRef, useCallback } from 'react';
import io, { Socket } from 'socket.io-client';
import './ChatLayout.css';
import HistorySidebar from './HistorySidebar';

interface ChatLayoutProps {
  onLogout: () => void;
}

interface Message {
  id: number | string;
  text: string;
  sender: 'user' | 'assistant';
}

let socket: Socket;

const ChatLayout: React.FC<ChatLayoutProps> = ({ onLogout }) => {
  const [userMode, setUserMode] = useState('Expert');
  const [currentMessage, setCurrentMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, text: 'Select a conversation from the left, or start a new one.', sender: 'assistant' },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [historyNeedsRefresh, setHistoryNeedsRefresh] = useState(0);

  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // --- WebSocket Connection ---
  useEffect(() => {
    socket = io('http://localhost:5000');
    socket.on('connect', () => console.log('Connected to WebSocket server with ID:', socket.id));

    socket.on('response_token', (data: { token: string }) => {
      setMessages(prev => {
        const last = prev[prev.length - 1];
        if (last && last.sender === 'assistant') {
          return [...prev.slice(0, -1), { ...last, text: last.text + data.token }];
        } else {
          return [...prev, { id: Date.now(), text: data.token, sender: 'assistant' }];
        }
      });
    });

    socket.on('stream_end', () => {
      setIsLoading(false);
      // After a message is fully received, refresh the history list to show the new title
      setHistoryNeedsRefresh(c => c + 1);
    });
    
    socket.on('error', (data: { error: string }) => {
      console.error('Socket Error:', data.error);
      setIsLoading(false);
    });
    
    socket.on('conversation_started', (data: { conversation_id: string }) => {
      setActiveConversationId(data.conversation_id);
      setHistoryNeedsRefresh(c => c + 1);
    });

    return () => {
      console.log('Disconnecting socket...');
      socket.disconnect();
    };
  }, []);

  // --- Data Fetching for Selected Conversation ---
  useEffect(() => {
    const fetchMessages = async () => {
      if (!activeConversationId) {
        setMessages([{ id: 1, text: 'Select a conversation or start a new one.', sender: 'assistant' }]);
        return;
      };
      
      setIsLoading(true);
      try {
        const response = await fetch(`http://localhost:5000/api/conversation/${activeConversationId}`);
        if (!response.ok) throw new Error('Failed to fetch messages.');
        const data = await response.json();
        setMessages(data.length > 0 ? data : [{id: 1, text: 'This conversation is empty.', sender: 'assistant'}]);
      } catch (error) {
        console.error(error);
        setMessages([{ id: Date.now(), text: 'Failed to load conversation.', sender: 'assistant' }]);
      } finally {
        setIsLoading(false);
      }
    };
    fetchMessages();
  }, [activeConversationId]);

  // --- Event Handlers ---
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentMessage.trim() || isLoading) return;

    const userMessage: Message = { id: Date.now(), text: currentMessage, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    socket.emit('chat_message', {
      message: currentMessage,
      user_mode: userMode.toLowerCase(),
      history: messages.slice(-10),
      conversation_id: activeConversationId, // Pass current convo ID
    });

    setCurrentMessage('');
  };

  const handleNewConversation = () => {
    setActiveConversationId(null);
    setMessages([{ id: 1, text: 'New chat started. How can I help?', sender: 'assistant' }]);
  };

  return (
    <div className="chat-layout">
      <HistorySidebar 
        activeConversationId={activeConversationId}
        onConversationSelect={setActiveConversationId}
        onNewConversation={handleNewConversation}
        needsRefresh={historyNeedsRefresh}
      />

      <main className="main-content">
        <header className="chat-header">🌿 AyurMind</header>

        <section className="chat-messages">
          {messages.map(message => (
            <div key={message.id} className={`message-placeholder ${message.sender}`}>
              {message.text}
            </div>
          ))}
          {isLoading && messages[messages.length - 1]?.sender === 'user' && (
            <div className="message-placeholder loading">
              <span className="typing-indicator"></span>
              <span className="typing-indicator"></span>
              <span className="typing-indicator"></span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </section>

        <section className="chat-input-area">
          <form className="chat-input-form" onSubmit={handleSubmit}>
            <input
              type="text"
              className="chat-input"
              placeholder={isLoading ? "Waiting for response..." : "Describe your concern..."}
              value={currentMessage}
              onChange={(e) => setCurrentMessage(e.target.value)}
              disabled={isLoading}
            />
            <button type="submit" className="chat-send-button" disabled={isLoading}>
              {isLoading ? '...' : 'Send'}
            </button>
          </form>
        </section>
      </main>

      <aside className="right-sidebar">
        <div className="right-sidebar-content">
          <div>
            <h2 className="sidebar-title">Controls</h2>
            <div className="expertise-selector">
              <p className="sidebar-title">Expertise Level</p>
              {['Beginner', 'Intermediate', 'Expert'].map(level => (
                <label key={level}>
                  <input
                    type="radio"
                    name="expertise"
                    value={level}
                    checked={userMode === level}
                    onChange={() => setUserMode(level)}
                    disabled={isLoading}
                  />
                  {level}
                </label>
              ))}
            </div>
          </div>
          <button onClick={onLogout} className="logout-button">Logout</button>
        </div>
      </aside>
    </div>
  );
};

export default ChatLayout;
