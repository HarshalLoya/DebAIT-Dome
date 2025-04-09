# Multi-AI-Agent-Debate-System 🤖🗣️

Welcome to the **Multi-AI-Agent-Debate-System**!  
This project simulates a **real-time AI debate** where two intelligent agents engage in a multi-round debate, complete with live-streamed arguments, scoring, and an interactive UI.

---

## 📁 Project Structure

```plaintext
Multi-AI-Agent-Debate-System/
├── agents/
│   ├── __init__.py
│   └── models.py         # Classes for Agent, Debater, and Moderator
├── llm/
│   ├── __init__.py
│   └── query.py          # Interfaces with LLM (e.g., Groq's LLaMA 70B API)
├── debate/
│   ├── __init__.py
│   ├── evaluation.py     # Scoring and evaluation logic
│   └── simulation.py     # Core debate simulation engine
├── ui/
│   ├── __init__.py
│   ├── app.py            # Main Streamlit UI
│   └── style.css         # Custom CSS styling
├── requirements.txt      
└── README.md             
```

---

## ✨ Key Features

- 🧠 **Multi-Round Debates**  
  Simulate structured debates with opening statements, rebuttals, and closing arguments.

- 📡 **Live Argument Streaming**  
  Watch AI agents "speak" with animated word-by-word message streaming.

- 📊 **Real-Time Scoring System**  
  A dynamic scoreboard updates after every round in the top-right corner.

- ⚙️ **Customizable Debate Settings**  
  Configure topic, number of rounds, tone, and response length using the sidebar.

- 🔌 **LLM-Powered Debates**  
  Integrates external LLMs (e.g., Groq LLaMA 70B) to generate human-like arguments.

---

## 🛠️ Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/HarshalLoya/Multi-AI-Agent-Debate-System.git
cd Multi-AI-Agent-Debate-System
```

### 2. (Optional) Create a Virtual Environment

```bash
python -m venv venv

# Activate on Unix/macOS:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Your API Key

Export your LLM API key as an environment variable:

```bash
# Unix/macOS:
export GROQ_LLAMA_70B_VERSATILE_API_KEY=<YOUR_API_KEY>

# Windows:
set GROQ_LLAMA_70B_VERSATILE_API_KEY=<YOUR_API_KEY>
```

---

## 🚀 Run the App

Launch the Streamlit UI:

```bash
streamlit run ui/app.py
```

Your default browser will open the app where you can initiate, configure, and view live AI debates.

---

## 📌 Additional Notes

- Debates are animated in real-time for an engaging experience.
- The system is **modular and extendable**, making it easy to add new features, agents, or scoring logic.
- Great for showcasing **LLM capabilities** in an interactive setting.

---

## 📜 License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to fork the repo, open issues, or submit pull requests.

Happy debating! 🎉🗣️🤖
