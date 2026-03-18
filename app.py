import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
from dotenv import load_dotenv
import re
import os

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Prompt Enhancer",
    page_icon="✨",
    layout="wide",
)

# ── Global styles — Claude.ai-inspired warm light theme ──────────────────────
st.markdown("""
<style>
  /* ── Page background ── */
  .stApp { background: #faf9f7 !important; }
  .stApp > header { background: transparent !important; }

  /* ── Remove default block padding ── */
  .block-container {
    padding-top: 3.5rem !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: #f3f1ec !important;
    border-right: 1px solid #e8e2d8 !important;
  }
  [data-testid="stSidebar"] * { color: #3d3830 !important; }
  [data-testid="stSidebar"] input {
    background: #fff !important;
    border: 1px solid #ddd8ce !important;
    color: #3d3830 !important;
    border-radius: 8px !important;
  }
  [data-testid="stSidebar"] select {
    background: #fff !important;
    border: 1px solid #ddd8ce !important;
    color: #3d3830 !important;
    border-radius: 8px !important;
  }

  /* ── Header text ── */
  .main-title {
    font-size: 1.85rem;
    font-weight: 700;
    color: #1a1815;
    margin-bottom: 0.15rem;
    letter-spacing: -0.02em;
  }
  .sub-title {
    font-size: 0.9rem;
    color: #9a9080;
    margin-bottom: 0.85rem;
  }

  /* ── Badges ── */
  .badge {
    display: inline-block;
    padding: 3px 11px;
    border-radius: 20px;
    font-size: 0.71rem;
    font-weight: 600;
    margin-right: 5px;
    letter-spacing: 0.01em;
  }
  .badge-context { background: #e8f0fb; color: #3b6dbf; }
  .badge-obj     { background: #e6f5ec; color: #2e7d52; }
  .badge-const   { background: #fef3e2; color: #b45309; }
  .badge-format  { background: #f3ebfc; color: #7c3aed; }
  .badge-cot     { background: #fde8e8; color: #b91c1c; }

  /* ── Both columns: same warm card ── */
  div[data-testid="stHorizontalBlock"] {
    align-items: stretch !important;
    gap: 1.1rem !important;
  }

  /* Shared card style */
  div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
    background: #ffffff !important;
    border: 1px solid #e8e2d8 !important;
    border-radius: 14px !important;
    height: calc(95vh - 196px) !important;
    min-height: 420px !important;
    padding: 0 0 20px 0 !important;
    display: flex !important;
    flex-direction: column !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03) !important;
  }

  /* Left column: scrollable so textarea resize handle can grow freely */
  div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]:first-child {
    overflow-y: auto !important;
    overflow-x: hidden !important;
  }

  /* Right column: clip the iframe */
  div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]:last-child {
    overflow: hidden !important;
  }

  /* ── Left column inner layout ── */
  div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]:first-child
    > div[data-testid="stVerticalBlockBorderWrapper"],
  div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]:first-child
    > div[data-testid="stVerticalBlock"] {
    display: flex !important;
    flex-direction: column !important;
    padding: 18px 20px 32px 20px !important;
    gap: 10px !important;
  }

  /* ── Panel header label ── */
  .panel-header {
    font-size: 0.69rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #b0a898;
    padding-bottom: 2px;
    flex-shrink: 0;
  }

  /* ── Textarea: free to resize, no flex constraints ── */
  div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]:first-child
    textarea {
    min-height: 220px !important;
    resize: vertical !important;
    background: #faf9f7 !important;
    border: 1px solid #e4ddd4 !important;
    border-radius: 10px !important;
    color: #2d2924 !important;
    font-size: 0.93rem !important;
    line-height: 1.7 !important;
    padding: 14px 15px !important;
    caret-color: #c96a4e;
    font-family: inherit !important;
    width: 100% !important;
  }
  div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]:first-child
    textarea::placeholder { color: #c4bdb4 !important; }
  div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]:first-child
    textarea:focus {
    border-color: #c9b8a4 !important;
    box-shadow: 0 0 0 3px rgba(201,106,78,0.08) !important;
    outline: none !important;
  }

  /* ── Enhance button ── */
  div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]:first-child
    [data-testid="stButton"] { flex-shrink: 0 !important; }
  div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]:first-child
    [data-testid="stButton"] button {
    width: 100% !important;
    background: #1a1815 !important;
    color: #f5f3ef !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 0.93rem !important;
    font-weight: 600 !important;
    padding: 11px !important;
    cursor: pointer !important;
    letter-spacing: 0.01em !important;
    transition: background .15s !important;
  }
  div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]:first-child
    [data-testid="stButton"] button:hover {
    background: #2e2b26 !important;
  }

  /* ── Right column iframe wrapper ── */
  div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]:last-child
    > div[data-testid="stVerticalBlockBorderWrapper"],
  div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]:last-child
    > div[data-testid="stVerticalBlock"] {
    height: 100% !important;
    padding: 0 !important;
  }
  div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]:last-child
    [data-testid="stVerticalBlock"] > div { height: 100% !important; }
  div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]:last-child
    iframe {
    display: block !important;
    width: 100% !important;
    height: 100% !important;
    border: none !important;
  }
</style>
""", unsafe_allow_html=True)

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert Prompt Engineer. Your goal is to transform vague user requests into high-quality, structured prompts optimised for use in other LLM models.

When given a raw/vague prompt, produce an enhanced, fully structured version following this framework:

## Context
Define the **persona** the AI should adopt (role, expertise, tone).

## Objective
State **clearly and precisely** what the AI needs to achieve. Be specific about the task, audience, and desired outcome.

## Constraints
List what the AI must **avoid** or **strictly follow** (e.g., length limits, style rules, topics to exclude, safety guidelines).

## Output Format
Specify the exact response format:
- Structure (Markdown / JSON / plain text / numbered list / etc.)
- Tone (formal / casual / technical / empathetic)
- Length or detail level

## Chain of Thought
Instruct the AI to reason step-by-step for complex tasks. Include reasoning triggers like:
- "Think step-by-step before answering."
- "First analyse X, then Y, finally Z."

---

Rules:
- Output ONLY the enhanced prompt wrapped in a single ```markdown ... ``` code block. Nothing else.
- Keep the enhanced prompt self-contained — it must work without extra context.
- Use clear, imperative language in the prompt itself.
"""

# ── Provider config ───────────────────────────────────────────────────────────
PROVIDERS = {
    "Groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "env_key":  "GROQ_API_KEY",
        "key_label": "Groq API Key",
        "key_help":  "console.groq.com",
        "models": [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
        ],
    },
    "OpenAI": {
        "base_url": None,
        "env_key":  "OPENAI_API_KEY",
        "key_label": "OpenAI API Key",
        "key_help":  "platform.openai.com/api-keys",
        "models": [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
        ],
    },
    "Gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "env_key":  "GEMINI_API_KEY",
        "key_label": "Gemini API Key",
        "key_help":  "aistudio.google.com/apikey",
        "models": [
            "gemini-2.0-flash",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro",
        ],
    },
}


def extract_prompt(response: str) -> str:
    match = re.search(r"```(?:\w+)?\n([\s\S]*?)```", response)
    return match.group(1).strip() if match else response.strip()


def right_panel(text: str) -> None:
    """Right output panel — Claude.ai warm light theme."""
    escaped = (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )
    content_html = (
        f"<pre id='content'>{escaped}</pre>"
        if text
        else "<p class='empty'>Your enhanced prompt will appear here…</p>"
    )

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 100%; height: 100%;
    background: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', sans-serif;
    overflow: hidden;
    color: #2d2924;
  }}

  .panel {{
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100vh;
    background: #ffffff;
  }}

  /* ── Header ── */
  .header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 20px;
    background: #faf9f7;
    border-bottom: 1px solid #eee8e0;
    flex-shrink: 0;
  }}
  .header-label {{
    font-size: 0.69rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #b0a898;
  }}
  .copy-btn {{
    display: flex; align-items: center; gap: 6px;
    background: #fff;
    border: 1px solid #e4ddd4;
    border-radius: 8px;
    padding: 5px 11px;
    cursor: pointer;
    color: #8c8070;
    font-size: 0.74rem;
    font-weight: 500;
    font-family: inherit;
    transition: background .15s, color .15s, border-color .15s;
  }}
  .copy-btn:hover  {{ background: #f5f3ef; color: #3d3830; border-color: #ccc4b8; }}
  .copy-btn.copied {{ color: #2e7d52; border-color: #a8d5b8; background: #f0faf5; }}
  .copy-btn svg {{ width: 13px; height: 13px; fill: currentColor; flex-shrink: 0; }}

  /* ── Scrollable body ── */
  .body {{
    flex: 1;
    overflow-y: auto;
    padding: 22px 24px 32px 24px;
    scrollbar-width: thin;
    scrollbar-color: #e0d8ce transparent;
  }}
  .body::-webkit-scrollbar {{ width: 5px; }}
  .body::-webkit-scrollbar-thumb {{ background: #e0d8ce; border-radius: 3px; }}

  pre {{
    white-space: pre-wrap;
    word-break: break-word;
    font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', 'Courier New', monospace;
    font-size: 0.875rem;
    line-height: 1.85;
    color: #2d2924;
  }}
  .empty {{
    color: #c8bfb4;
    font-size: 0.88rem;
    font-style: italic;
    margin-top: 6px;
  }}

  /* ── Toast ── */
  .toast {{
    display: none;
    position: fixed;
    bottom: 16px; right: 16px;
    background: #fff;
    border: 1px solid #e0d8ce;
    color: #2e7d52;
    padding: 8px 16px;
    border-radius: 9px;
    font-size: 0.76rem;
    font-weight: 500;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    z-index: 99;
    pointer-events: none;
  }}
</style>
</head>
<body>
<div class="panel" id="panel">
  <div class="header">
    <span class="header-label">Enhanced Prompt</span>
    <button class="copy-btn" id="copyBtn" onclick="copyText()">
      <svg viewBox="0 0 24 24"><path d="M16 1H4C2.9 1 2 1.9 2 3v14h2V3h12V1zm3 4H8C6.9 5 6 5.9 6 7v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
      Copy
    </button>
  </div>
  <div class="body">{content_html}</div>
</div>
<div class="toast" id="toast">✓ Copied to clipboard</div>

<script>
  function fitHeight() {{
    try {{
      var ph = window.parent.innerHeight;
      if (ph) {{
        var h = Math.max(ph - 196, 420);
        document.getElementById('panel').style.height = h + 'px';
        window.parent.postMessage({{ type: 'streamlit:setFrameHeight', height: h }}, '*');
      }}
    }} catch(e) {{}}
  }}
  fitHeight();
  window.addEventListener('resize', fitHeight);

  function copyText() {{
    var el = document.getElementById('content');
    if (!el) return;
    navigator.clipboard.writeText(el.innerText).then(function() {{
      var btn  = document.getElementById('copyBtn');
      var toast = document.getElementById('toast');
      btn.classList.add('copied');
      btn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg> Copied!';
      toast.style.display = 'block';
      setTimeout(function() {{
        btn.classList.remove('copied');
        btn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M16 1H4C2.9 1 2 1.9 2 3v14h2V3h12V1zm3 4H8C6.9 5 6 5.9 6 7v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg> Copy';
        toast.style.display = 'none';
      }}, 2200);
    }});
  }}
</script>
</body>
</html>"""
    components.html(html, height=700, scrolling=False)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")

    provider = st.selectbox(
        "Provider",
        list(PROVIDERS.keys()),
        index=0,
    )
    cfg = PROVIDERS[provider]

    st.markdown("---")

    api_key_input = st.text_input(
        cfg["key_label"],
        type="password",
        value=os.environ.get(cfg["env_key"], ""),
        help=f"Get your key at {cfg['key_help']}",
    )
    if api_key_input:
        os.environ[cfg["env_key"]] = api_key_input

    st.markdown("---")

    model_choice = st.selectbox(
        "Model",
        cfg["models"],
        index=0,
    )

    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
- Be as vague or specific as you like.
- Works for: coding assistants, chatbots, content writers, analysts, tutors.
- Copy the output directly into ChatGPT, Claude, Gemini, etc.
    """)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">✨ Prompt Enhancer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Transform any vague idea into a precise, structured LLM prompt.</p>', unsafe_allow_html=True)
st.markdown("""
<span class="badge badge-context">Context</span>
<span class="badge badge-obj">Objective</span>
<span class="badge badge-const">Constraints</span>
<span class="badge badge-format">Output Format</span>
<span class="badge badge-cot">Chain of Thought</span>
""", unsafe_allow_html=True)
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Two equal panels ──────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="medium")

with left:
    st.markdown('<p class="panel-header">Your Raw Prompt</p>', unsafe_allow_html=True)
    raw_prompt = st.text_area(
        label="raw_prompt",
        label_visibility="collapsed",
        placeholder=(
            "e.g.  Write a prompt that helps me summarise research papers.\n\n"
            "or    I need a prompt for a customer support chatbot.\n\n"
            "or    Create a prompt to review Python code for bugs."
        ),
        height=380,
    )
    enhance_btn = st.button("✨ Enhance Prompt", use_container_width=True)

with right:
    output_slot = st.empty()
    with output_slot:
        right_panel("")

# ── Enhancement logic ─────────────────────────────────────────────────────────
if enhance_btn:
    api_key = os.environ.get(cfg["env_key"], "")
    if not raw_prompt.strip():
        st.warning("Please enter a prompt to enhance.")
    elif not api_key:
        st.error(f"Add your {cfg['key_label']} in the sidebar first.")
    else:
        client_kwargs = {"api_key": api_key}
        if cfg["base_url"]:
            client_kwargs["base_url"] = cfg["base_url"]
        client = OpenAI(**client_kwargs)

        with st.spinner(f"Enhancing with {provider} · {model_choice}…"):
            collected = []
            stream = client.chat.completions.create(
                model=model_choice,
                max_tokens=4096,
                stream=True,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": f"Enhance this prompt:\n\n{raw_prompt.strip()}"},
                ],
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                if delta:
                    collected.append(delta)

        enhanced = extract_prompt("".join(collected))
        with output_slot:
            right_panel(enhanced)
