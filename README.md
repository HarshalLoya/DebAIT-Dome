# Multi-AI-Agent-Debate-System 🤖🗣️

Welcome to the **Multi-AI-Agent-Debate-System**! This repository features a **real-time debate simulation** where two AI agents engage in a live debate with multiple rounds, animated streaming of their arguments, and a dynamic scoreboard.

## 📂 Directory Structure
```

Multi-AI-Agent-Debate-System/
├── agents/
│ ├── **init**.py
│ └── models.py # Model definitions for Agent, Debater, and Moderator
├── llm/
│ ├── **init**.py
│ └── query.py # LLM query function (e.g., using Groq's Llama 70B API)
├── debate/
│ ├── **init**.py
│ ├── evaluation.py # Functions to evaluate and score arguments
│ └── simulation.py # Multi-round debate simulation
├── ui/
│ ├── **init**.py
│ ├── app.py # Main Streamlit UI application
│ ├── components.py # Helper UI functions (if used)
│ └── style.css # Custom CSS for the UI styling
├── requirements.txt # Python dependencies
└── README.md # This file

````

## ✨ Features

- **Multi-Round Debates:** Engage in debates with several rounds of opening arguments and rebuttals.
- **Live Streaming Animation:** Watch debate messages stream in word-by-word for a dynamic experience.
- **Real-Time Scoring:** A fixed scoreboard in the top-right corner updates live as the debate proceeds.
- **Customizable Settings:** Configure debate parameters like topic, number of rounds, tone, and response length via the sidebar.
- **LLM Integration:** Leverages an external LLM API (e.g., Groq's Llama 70B) to generate debate content.

## 🛠️ Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/HarshalLoya/Multi-AI-Agent-Debate-System.git
   cd Multi-AI-Agent-Debate-System
````

2. **Create & Activate a Virtual Environment (optional but recommended):**

   ```bash
   python -m venv venv
   # On Unix/macOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Your API Key:**  
   Make sure to set the environment variable for your LLM API key. For example:

   ```bash
   export GROQ_LLAMA_70B_VERSATILE_API_KEY=<YOUR_API_KEY>
   # On Windows:
   set GROQ_LLAMA_70B_VERSATILE_API_KEY=<YOUR_API_KEY>
   ```

## 🚀 Running the Application

Start the Streamlit UI by running:

```bash
streamlit run ui/app.py
```

This will open the application in your default browser so you can configure debate parameters and watch the live debate simulation in action.

## 📌 Notes

- The debate is streamed incrementally with lively animations, presenting the text in small word chunks.
- The scoreboard is fixed at the top-right and updates in real time.
- The design is modular, allowing you to easily modify debate rules, scoring, and UI elements.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to contribute, report issues, or fork the repository. Happy debating! 🎉🗣️🤖

```
