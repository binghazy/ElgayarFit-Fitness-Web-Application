import { useEffect } from "react";

export function Toast({ message, type = "info", onClose, duration = 3000 }) {
  useEffect(() => {
    const timer = setTimeout(onClose, duration);
    return () => clearTimeout(timer);
  }, [duration, onClose]);

  return (
    <div
      className={`
      fixed bottom-4 right-4 p-4 rounded-lg shadow-lg
      ${type === "error" ? "bg-red-600" : "bg-green-600"} 
      text-white
      transform transition-transform duration-300 ease-in-out
    `}
    >
      {message}
    </div>
  );
}
