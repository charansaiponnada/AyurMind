import { useState } from 'react';
import './LoginPage.css'; // This is still needed for the login part
import ChatLayout from './components/ChatLayout'; // Import the new layout

function App() {
  // Initialize state from sessionStorage to persist across reloads
  const [isAuthenticated, setIsAuthenticated] = useState(sessionStorage.getItem('isAuthenticated') === 'true');
  
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (username === 'admin' && password === '123') {
      // Save to sessionStorage on successful login
      sessionStorage.setItem('isAuthenticated', 'true');
      setIsAuthenticated(true);
      setError('');
    } else {
      setError('Invalid username or password');
    }
  };

  const handleLogout = () => {
    // Clear from sessionStorage on logout
    sessionStorage.removeItem('isAuthenticated');
    setIsAuthenticated(false);
  };

  if (!isAuthenticated) {
    return (
      <div className="login-container">
        <div className="login-form-panel">
          <h1>AyurMind</h1>
          <form onSubmit={handleLogin} className="login-form">
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="login-input"
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="login-input"
            />
            <button type="submit" className="login-button">Login</button>
            {error && <p className="login-error">{error}</p>}
          </form>
        </div>
        <div className="login-display-panel" />
      </div>
    );
  }

  // Render the main chat interface after login, passing the logout handler
  return <ChatLayout onLogout={handleLogout} />;
}

export default App;
