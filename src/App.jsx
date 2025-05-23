import React, { useState, useEffect, useRef } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useNavigate,
} from "react-router-dom";
import { useMessages } from "./context/MessagesContext";
import { useApi } from "./hooks/useApi";
import {
  MessageSquarePlus,
  BarChart2,
  UtensilsCrossed,
  Dumbbell,
  Calculator,
  User,
  Menu,
  X,
  Send,
} from "lucide-react";
import DE from "./components/DE";

function MainContent() {
  const [input, setInput] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const { messages, loading, addMessage, clearMessages } = useMessages();
  const { sendMessage } = useApi();
  const chatBoxRef = useRef(null);
  const [chats, setChats] = useState([]);
  const [currentChat, setCurrentChat] = useState({
    id: "default",
    name: "New Chat",
    messages: [],
  });
  const [isFirstVisit, setIsFirstVisit] = useState(true);
  const [showDE, setShowDE] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]);

  const generateChatName = (message) => {
    return message.length > 30 ? message.substring(0, 30) + "..." : message;
  };

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    addMessage(userMessage);
    setInput("");

    if (messages.length === 0) {
      const chatName = generateChatName(input);
      setCurrentChat((prev) => ({ ...prev, name: chatName }));
      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat.id ? { ...chat, name: chatName } : chat
        )
      );
    }

    try {
      // Add thinking message
      const thinkingMessage = {
        role: "assistant",
        content: "thinking",
        isThinking: true,
      };
      addMessage(thinkingMessage);

      const response = await sendMessage([...messages, userMessage]);

      if (response.message) {
        // Replace thinking message with actual response
        addMessage({
          ...response.message,
          content: response.message.content,
          isThinking: false,
        });
      }
    } catch (error) {
      // Remove thinking message on error
      addMessage({
        role: "assistant",
        content: "Sorry, there was an error. Please try again.",
        isThinking: false,
      });
      console.error("Error:", error);
    }
  };

  const handleNewChat = () => {
    setIsFirstVisit(false);
    const newChat = {
      id: Date.now().toString(),
      name: "New Chat",
      messages: [],
    };
    setChats((prev) => [...prev, newChat]);
    setCurrentChat(newChat);
    clearMessages();
    setSidebarOpen(false);
  };

  const handleDEClick = () => {
    navigate("/DE");
  };

  return (
    <div className="app-container">
      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="sidebar-content">
          <div className="profile-header">
            <div className="profile-image"></div>
            <div className="profile-title">ELGAYAR FIT</div>
          </div>

          <div className="sidebar-buttons">
            <button onClick={handleNewChat} className="sidebar-button primary">
              <MessageSquarePlus size={20} />
              Add Chat
            </button>

            <div className="chat-list">
              {chats.map((chat) => (
                <button
                  key={chat.id}
                  className={`sidebar-button ${
                    currentChat.id === chat.id ? "active" : ""
                  }`}
                  onClick={() => setCurrentChat(chat)}
                >
                  <MessageSquarePlus size={16} />
                  {chat.name}
                </button>
              ))}
            </div>

            <nav className="flex flex-col gap-2">
              <button
                className="sidebar-button"
                onClick={() => (window.location.href = "http://localhost:8501")}
              >
                <BarChart2 size={20} />
                Metrics Analysis
              </button>
              <button
                className="sidebar-button"
                onClick={() =>
                  (window.location.href = "http://localhost:8501/eat")
                }
              >
                <UtensilsCrossed size={20} />
                Nutrition Guide
              </button>
              <button
                className="sidebar-button"
                onClick={() =>
                  (window.location.href = "http://localhost:8501/fit")
                }
              >
                <Dumbbell size={20} />
                Fitness Excercises
              </button>
              <button className="sidebar-button" onClick={handleDEClick}>
                <Calculator size={20} />
                Advanced Meal Planning{" "}
              </button>
            </nav>
          </div>

          <div className="sidebar-footer">
            <button className="sidebar-button">
              <User size={20} />
              My Profile
            </button>
          </div>
        </div>
      </aside>

      <main className="chat-container">
        <div className="md:hidden p-4 border-b border-[var(--border)]"></div>
        <div ref={chatBoxRef} className="chat-messages">
          {isFirstVisit ? (
            <div className="welcome-message">
              <div className="welcome-gif-container">
                <img
                  src="src\weightlift.gif"
                  alt="Weightlifter"
                  className="welcome-gif"
                />
              </div>
              <h1>Welcome to ElgayarFit Training Coach</h1>
              <p>
                To start a new conversation, please click the "Add Chat" button.
              </p>
            </div>
          ) : (
            messages.map((msg, i) => (
              <div
                key={i}
                className={`message ${msg.role === "user" ? "user" : ""}`}
                style={{ animationDelay: `${i * 100}ms` }}
              >
                <img src="src\Elgayr.jpg" alt="aa" className="avatar" />
                <div className="message-content">
                  {msg.isThinking ? (
                    <div className="thinking-animation">
                      <div className="dot"></div>
                      <div className="dot"></div>
                      <div className="dot"></div>
                    </div>
                  ) : (
                    msg.content
                  )}
                </div>
              </div>
            ))
          )}
        </div>

        <form onSubmit={handleSend} className="input-container">
          <div className="input-wrapper">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={
                isFirstVisit
                  ? "Click 'New Chat' to start..."
                  : "Message Elgayar..."
              }
              className="chat-input"
              disabled={isFirstVisit || loading}
            />
            <button
              type="submit"
              disabled={isFirstVisit || loading || !input.trim()}
              className="send-button"
            >
              <Send size={20} />
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainContent />} />
        <Route path="/DE" element={<DE />} />
      </Routes>
    </Router>
  );
}

export default App;
