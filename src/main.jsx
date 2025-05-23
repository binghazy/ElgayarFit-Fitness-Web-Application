import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./theme.css";
import App from "./App.jsx";
import { MessagesProvider } from "./context/MessagesContext";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <MessagesProvider>
      <App />
    </MessagesProvider>
  </StrictMode>
);
