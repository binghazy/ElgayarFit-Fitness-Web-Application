import axios from "axios";
import { useState } from 'react';

const API_URL = "http://localhost:3001";

export const useApi = () => {
  const [error, setError] = useState(null);

  const sendMessage = async (messages) => {
    try {
      const response = await fetch('http://localhost:3001/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  return { sendMessage, error };
};
