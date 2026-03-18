# ✨ LLM Prompt Enhancer

A Streamlit web app that transforms vague, rough prompts into high-quality, structured prompts ready for use in any LLM — ChatGPT, Claude, Gemini, and more.

---

## Features

- **Multi-provider support** — Groq, OpenAI, and Gemini via a single unified interface
- **Structured prompt engineering** — every enhanced prompt follows the Context → Objective → Constraints → Output Format → Chain of Thought framework
- **Streaming output** — response streams silently and renders as the final clean prompt
- **Copy to clipboard** — one-click copy button with animated confirmation
- **Responsive layout** — two equal-height panels that adapt to your screen size
- **Resizable input** — drag the bottom-right handle to grow the input textarea

---

## Preview

| Panel     | Description                                  |
| --------- | -------------------------------------------- |
| **Left**  | Paste your raw / vague prompt                |
| **Right** | Receive the fully structured enhanced prompt |

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/GKrishnaRao/llm_prompt_generate.git
cd llm_prompt_generate
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy the example file and fill in your API keys:

```bash
cp .env.example .env
```

`.env` format:

```
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

> You only need the key for the provider you intend to use.

| Provider | Get API Key                          |
| -------- | ------------------------------------ |
| Groq     | https://console.groq.com             |
| OpenAI   | https://platform.openai.com/api-keys |
| Gemini   | https://aistudio.google.com/apikey   |

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Supported Models

| Provider   | Models                                                                          |
| ---------- | ------------------------------------------------------------------------------- |
| **Groq**   | llama-3.3-70b-versatile, llama-3.1-8b-instant, mixtral-8x7b-32768, gemma2-9b-it |
| **OpenAI** | gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo                                 |
| **Gemini** | gemini-2.0-flash, gemini-1.5-pro, gemini-1.5-flash, gemini-1.0-pro              |

---

## Prompt Engineering Framework

Every enhanced prompt is structured around five components:

| Component            | Purpose                                     |
| -------------------- | ------------------------------------------- |
| **Context**          | Defines the AI persona and expertise        |
| **Objective**        | States the precise task and desired outcome |
| **Constraints**      | Lists rules, limits, and things to avoid    |
| **Output Format**    | Specifies structure, tone, and length       |
| **Chain of Thought** | Triggers step-by-step reasoning             |

---

## Project Structure

```
prompt_generate/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # API keys (not committed)
├── .env.example        # API key template
├── .gitignore
└── README.md
```

---

## Dependencies

```
streamlit>=1.37.0
openai>=1.30.0
python-dotenv>=1.0.0
```

---

## License

MIT
