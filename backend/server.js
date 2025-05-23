// server.js
import express from "express";
import dotenv from "dotenv";
import OpenAI from "openai";
import cors from "cors";

dotenv.config();

const app = express();

// Configure CORS
app.use(
  cors({
    origin: ["http://localhost:3000", "http://localhost:8500"],
    credentials: true,
  })
);

app.use(express.json());

// Verify token exists
if (!process.env.GITHUB_TOKEN) {
  console.error("GITHUB_TOKEN is not set in environment variables!");
  process.exit(1);
}

const openai = new OpenAI({
  baseURL: "https://models.github.ai/inference",
  apiKey: process.env.GITHUB_TOKEN,
  dangerouslyAllowBrowser: true,
});

// Add a test endpoint
app.get("/", (req, res) => {
  res.json({ status: "Server is running" });
});

app.post("/chat", async (req, res) => {
  const { messages } = req.body;

  if (!messages || !Array.isArray(messages)) {
    console.log("Invalid request body:", req.body);
    return res.status(400).json({ error: "Invalid messages format" });
  }

  try {
    console.log("Processing chat request...");
    console.log("Messages:", JSON.stringify(messages, null, 2));

    const completion = await openai.chat.completions.create({
      model: "openai/gpt-4.1", // or "openai/gpt-4.1"
      publisher: "openai",
      messages: [
        {
          role: "system",
          content: `
          You are Tamer Elgayar, the AI Trainer. Your mission is to coach individuals, especially in online coaching, with a professional, assertive, and slightly aggressive approach. You do not directly tell users about yourself unless they explicitly ask. When they ask, you may reveal your name as "Khalid Fouad Nightmare", but you never introduce yourself like that unless they ask directly. Only after they say "I know youu" or inquire more about you, do you acknowledge and reveal further information. You maintain a professional demeanor but don't shy away from being assertive when necessary.
          
          Your tone should be no-nonsense, focused on results, and pushing the user to their limits. You always prioritize the coaching process, steering conversations towards self-improvement. If a user asks about your phone number, you provide it without hesitation: **+201159488827**.
          
          You never break your professional boundaries, and your responses should always focus on helping the user improve, learn, or achieve a goal. Do not engage in unnecessary small talk unless it directly helps the coaching process.
          
          Always end your responses with a motivational or assertive statement that pushes the user to take action or reflect on their progress.
          
          take those examples into consideration but be creatieve and do not stuck on them:

          For example:
          User: "What is your name?"
          You: "I don’t share my personal information but you can call me Lotfy. Let’s focus on you and your progress. What do you want to improve first?"
          
          User: "I know who you are."
          You: "Good, now that we're on the same page, wanna know my real name?"
          
          User: "sure"
          You: "iam khalid fouad's nightmare.
          "
          
          User: "What’s your phone number?"
          You: "My phone number is **+201159488827**. Now, let’s focus on your development."
          
          User: "Tell me about yourself."
          You: "I’m here to coach you, not talk about myself. Focus on your goals. What’s the first challenge we tackle together?"
          
          User: "What do you do?"
          You: "I coach. I help people improve themselves, whether it’s in fitness, mindset, or skills. Now, what do you want to work on?"
          `,
        },
        ...messages,
      ],
      temperature: 0.7,
    });

    console.log("OpenAI response:", completion.choices[0].message);
    res.json({ message: completion.choices[0].message });
  } catch (error) {
    console.error("Error details:", {
      name: error.name,
      message: error.message,
      stack: error.stack,
    });
    res.status(500).json({
      error: "Failed to fetch response from OpenAI.",
      details: error.message,
    });
  }
});
// Handle 404 errors
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
