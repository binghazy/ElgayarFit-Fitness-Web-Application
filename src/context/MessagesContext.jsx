import { createContext, useContext, useState } from "react";

const MessagesContext = createContext();

export function MessagesProvider({ children }) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const addMessage = (message) => {
    setMessages(prev => {
      // Remove thinking message and add new message
      const filteredMessages = prev.filter(msg => !msg.isThinking);
      return [...filteredMessages, message];
    });
  };

  const clearMessages = () => {
    setMessages([]);
  };

  return (
    <MessagesContext.Provider
      value={{
        messages,
        loading,
        setLoading,
        addMessage,
        clearMessages,
      }}
    >
      {children}
    </MessagesContext.Provider>
  );
}

export const useMessages = () => useContext(MessagesContext);

