def get_theme_css(theme_name, mode):
    # ---------------- colour palette ----------------
    if mode == "dark":
        bg_app = "linear-gradient(135deg, #0f0c29, #302b63, #24243e)"
        bg_sidebar = "rgba(10, 10, 20, 0.85)"
        bg_main = "rgba(20, 20, 35, 0.7)"
        text = "#e0e0e0"
        text_secondary = "#aaaaaa"
        border = "rgba(255,255,255,0.1)"
        input_bg = "rgba(255,255,255,0.08)"
        chat_user = "rgba(108,99,255,0.15)"
        chat_assistant = "rgba(255,255,255,0.05)"
        button_bg = "rgba(255,255,255,0.15)"
        button_hover = "rgba(255,255,255,0.25)"
        expander_bg = "rgba(255,255,255,0.03)"
        progress_bg = "rgba(255,255,255,0.1)"
    else:
        bg_app = "linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)"
        bg_sidebar = "rgba(255,255,255,0.55)"
        bg_main = "rgba(255,255,255,0.35)"
        text = "#2d2d2d"
        text_secondary = "#555555"
        border = "rgba(255,255,255,0.3)"
        input_bg = "rgba(255,255,255,0.25)"
        chat_user = "rgba(108,99,255,0.1)"
        chat_assistant = "rgba(255,255,255,0.5)"
        button_bg = "rgba(255,255,255,0.3)"
        button_hover = "rgba(255,255,255,0.5)"
        expander_bg = "rgba(255,255,255,0.1)"
        progress_bg = "rgba(255,255,255,0.3)"

    if theme_name == "modern":
        primary = "#6C63FF" if mode == "light" else "#BB86FC"
    elif theme_name == "classic":
        primary = "#4A90E2" if mode == "light" else "#82B1FF"
    elif theme_name == "retro":
        primary = "#E63946" if mode == "light" else "#FF8A80"

    css = f"""
    <style>
    /* ---------- global overrides ---------- */
    .stApp {{
        background: {bg_app} !important;
        color: {text} !important;
    }}
    /* main container */
    .main .block-container {{
        background: {bg_main} !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        border: 1px solid {border} !important;
        padding: 2rem !important;
    }}
    /* sidebar */
    section[data-testid="stSidebar"] > div:first-child {{
        background: {bg_sidebar} !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        margin: 8px !important;
        border: 1px solid {border} !important;
        color: {text} !important;
    }}
    /* sidebar text */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] .stSelectbox label {{
        color: {text} !important;
    }}
    /* headings */
    h1, h2, h3, h4, h5, h6 {{
        color: {text} !important;
    }}
    /* paragraphs */
    p, span, div {{
        color: {text} !important;
    }}
    /* buttons */
    .stButton > button, .stDownloadButton > button {{
        background: {button_bg} !important;
        backdrop-filter: blur(5px) !important;
        border: 1px solid {border} !important;
        border-radius: 10px !important;
        color: {text} !important;
    }}
    .stButton > button:hover {{
        background: {button_hover} !important;
        border-color: {primary} !important;
    }}
    /* inputs & text areas */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div > div > select {{
        background: {input_bg} !important;
        border: 1px solid {border} !important;
        border-radius: 12px !important;
        color: {text} !important;
    }}
    /* expanders */
    .streamlit-expanderHeader {{
        background: {expander_bg} !important;
        border-radius: 12px !important;
        border: 1px solid {border} !important;
        color: {text} !important;
    }}
    .streamlit-expanderContent {{
        background: transparent !important;
    }}
    /* progress bars */
    .stProgress > div > div > div > div {{
        background-color: {primary} !important;
    }}
    .stProgress > div > div > div {{
        background: {progress_bg} !important;
    }}
    /* chat messages */
    .stChatMessage {{
        background: transparent !important;
    }}
    .stChatMessage:nth-child(odd) {{   /* user messages */
        background: {chat_user} !important;
        border-radius: 18px !important;
        padding: 0.8rem !important;
        margin: 0.5rem 0 !important;
    }}
    .stChatMessage:nth-child(even) {{  /* assistant messages */
        background: {chat_assistant} !important;
        border-radius: 18px !important;
        padding: 0.8rem !important;
        margin: 0.5rem 0 !important;
    }}
    /* chat input container (squircle, expandable) */
    .stChatInputContainer textarea {{
        background: {input_bg} !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 30px !important;
        border: 1px solid {border} !important;
        padding: 12px 50px 12px 20px !important;
        color: {text} !important;
        min-height: 50px !important;
        max-height: 120px !important;
        line-height: 1.4 !important;
        transition: border-radius 0.2s ease !important;
    }}
    .stChatInputContainer textarea:focus {{
        border-radius: 18px !important;
        box-shadow: 0 0 12px {primary} !important;
    }}
    /* remove ugly white backgrounds from file uploader */
    .stFileUploader {{
        background: transparent !important;
    }}
    /* links */
    a {{
        color: {primary} !important;
    }}
    /* custom primary colour for widgets */
    .st-cb, .st-dt, .st-dh, .st-cq, .st-cp {{
        border-color: {primary} !important;
    }}
    </style>
    """
    return css