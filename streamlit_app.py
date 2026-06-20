# ============================================================
#  streamlit_app.py  —  Instagram Caption Generator UI
#  Run: streamlit run streamlit_app.py
# ============================================================

# pip install streamlit anthropic
# Place this file in same folder as caption_generator_api.py

import streamlit as st

from caption_generator_api import (
    get_client, generate_captions, make_hashtags,
    VALID_TOPICS, VALID_STYLES,
)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Caption Generator",
    page_icon="⚡",
    layout="centered",
)

# =========================
# CUSTOM CSS — dark luxury aesthetic
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0a;
    color: #f0f0f0;
}

/* Main container */
.main .block-container {
    max-width: 720px;
    padding: 2rem 1.5rem 4rem;
}

/* Header */
.app-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid #1e1e1e;
    margin-bottom: 2rem;
}
.app-header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #fff 0%, #888 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.3rem;
}
.app-header p {
    color: #555;
    font-size: 0.9rem;
    margin: 0;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Selectbox label */
label {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #666 !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: #111 !important;
    border: 1px solid #222 !important;
    border-radius: 8px !important;
    color: #f0f0f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: #444 !important;
}

/* Generate button */
div.stButton > button {
    width: 100%;
    background: #f0f0f0;
    color: #0a0a0a;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    margin-top: 0.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
}
div.stButton > button:hover {
    background: #fff;
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(255,255,255,0.08);
}

/* Caption card */
.caption-card {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color 0.2s;
}
.caption-card:hover {
    border-color: #333;
}
.caption-num {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    color: #333;
    letter-spacing: 0.1em;
    min-width: 20px;
}
.caption-text {
    font-size: 0.95rem;
    color: #e8e8e8;
    flex: 1;
    line-height: 1.4;
}

/* Hashtag box */
.hashtag-box {
    background: #0e0e0e;
    border: 1px dashed #222;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: #555;
    line-height: 1.8;
    word-break: break-all;
    margin-top: 0.5rem;
}
.hashtag-box span {
    color: #3a7fff;
    margin-right: 4px;
}

/* Section label */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #444;
    margin: 1.5rem 0 0.6rem;
}

/* Speed badge */
.speed-badge {
    display: inline-block;
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 20px;
    padding: 0.2rem 0.7rem;
    font-size: 0.75rem;
    color: #555;
    margin-top: 1rem;
}

/* Text area for copy */
textarea {
    background: #111 !important;
    border: 1px solid #222 !important;
    color: #888 !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
}

/* API key input */
input[type="password"], input[type="text"] {
    background: #111 !important;
    border: 1px solid #222 !important;
    color: #f0f0f0 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Divider */
hr {
    border-color: #1a1a1a !important;
    margin: 1.5rem 0 !important;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================
st.markdown("""
<div class="app-header">
    <h1>⚡ Caption Generator</h1>
    <p>Claude AI — GenZ Instagram Captions</p>
</div>
""", unsafe_allow_html=True)


# =========================
# API KEY INPUT
# =========================
with st.expander("🔑 API Key Setup", expanded=not st.session_state.get("api_key_saved")):
    api_key_input = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-api03-...",
        help="Get your key at https://console.anthropic.com",
    )
    if api_key_input:
        st.session_state["api_key"] = api_key_input
        st.session_state["api_key_saved"] = True
        st.success("✅ Key saved for this session")

api_key = st.session_state.get("api_key", "")


# =========================
# INPUTS
# =========================
col1, col2 = st.columns(2)

with col1:
    topic = st.selectbox(
        "Topic",
        VALID_TOPICS,
        format_func=lambda x: x.capitalize(),
    )

with col2:
    style = st.selectbox(
        "Style",
        VALID_STYLES,
        format_func=lambda x: x.capitalize(),
    )

generate_btn = st.button("Generate Captions →")


# =========================
# GENERATE
# =========================
if generate_btn:
    if not api_key:
        st.error("❌ API key daalo pehle — upar wale section mein")
        st.stop()

    with st.spinner("Generating..."):
        try:
            client           = get_client(api_key)
            captions, elapsed = generate_captions(topic, style, client)
            hashtags          = make_hashtags(topic, style)

            # save to session
            st.session_state["captions"] = captions
            st.session_state["hashtags"] = hashtags
            st.session_state["elapsed"]  = elapsed

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.stop()


# =========================
# DISPLAY RESULTS
# =========================
if st.session_state.get("captions"):

    captions = st.session_state["captions"]
    hashtags = st.session_state["hashtags"]
    elapsed  = st.session_state["elapsed"]

    st.markdown('<div class="section-label">📝 Captions</div>', unsafe_allow_html=True)

    for i, cap in enumerate(captions, 1):
        st.markdown(f"""
        <div class="caption-card">
            <span class="caption-num">0{i}</span>
            <span class="caption-text">{cap}</span>
        </div>
        """, unsafe_allow_html=True)

    # copy all captions
    all_captions_text = "\n".join(f"{i}. {c}" for i, c in enumerate(captions, 1))
    st.text_area(
        "Copy all captions",
        value=all_captions_text,
        height=140,
        label_visibility="collapsed",
    )

    st.markdown('<div class="section-label">#️⃣ Hashtags</div>', unsafe_allow_html=True)

    # render hashtags as colored spans
    hashtag_html = " ".join(
        f'<span>{tag}</span>' for tag in hashtags.split()
    )
    st.markdown(f'<div class="hashtag-box">{hashtag_html}</div>', unsafe_allow_html=True)

    st.text_area(
        "Copy hashtags",
        value=hashtags,
        height=68,
        label_visibility="collapsed",
    )

    st.markdown(f'<div class="speed-badge">⏱ {elapsed}s</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        '<p style="text-align:center;color:#2a2a2a;font-size:0.75rem;">Built with Claude API · Anthropic</p>',
        unsafe_allow_html=True,
    )
