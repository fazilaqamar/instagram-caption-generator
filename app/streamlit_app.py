
# ============================================================
# streamlit_app.py — Instagram Caption Generator UI
# Run: streamlit run streamlit_app.py
# ============================================================

import streamlit as st
from caption_generator_api import (
    get_client,
    generate_captions,
    make_hashtags,
    VALID_TOPICS,
    VALID_STYLES,
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
# SESSION STATE
# =========================
if "captions" not in st.session_state:
    st.session_state["captions"] = []

if "hashtags" not in st.session_state:
    st.session_state["hashtags"] = ""

if "elapsed" not in st.session_state:
    st.session_state["elapsed"] = 0


# =========================
# CUSTOM CSS — DARK LUXURY
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0a;
    color: #f0f0f0;
}

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
    color: #777;
    font-size: 0.9rem;
    margin: 0;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Labels */
label {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #999 !important;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    background: #111 !important;
    border: 1px solid #222 !important;
    border-radius: 8px !important;
    color: #f0f0f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

div[data-baseweb="select"] > div:hover {
    border-color: #555 !important;
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

/* Caption cards */
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
    border-color: #444;
}

.caption-num {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    color: #777;
    letter-spacing: 0.1em;
    min-width: 20px;
}

.caption-text {
    font-size: 0.95rem;
    color: #e8e8e8;
    flex: 1;
    line-height: 1.5;
}

/* Hashtags */
.hashtag-box {
    background: #0e0e0e;
    border: 1px dashed #333;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: #aaa;
    line-height: 1.8;
    word-break: break-all;
    margin-top: 0.5rem;
}

.hashtag-box span {
    color: #3a7fff;
    margin-right: 4px;
}

/* Section labels */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #888;
    margin: 1.5rem 0 0.6rem;
}

/* Speed badge */
.speed-badge {
    display: inline-block;
    background: #111;
    border: 1px solid #333;
    border-radius: 20px;
    padding: 0.2rem 0.7rem;
    font-size: 0.75rem;
    color: #aaa;
    margin-top: 1rem;
}

/* Text areas */
textarea {
    background: #111 !important;
    border: 1px solid #333 !important;
    color: #ddd !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
}

/* Divider */
hr {
    border-color: #222 !important;
    margin: 1.5rem 0 !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================
st.markdown("""
<div class="app-header">
    <h1>⚡ Caption Generator</h1>
    <p>Groq AI — GenZ Instagram Captions</p>
</div>
""", unsafe_allow_html=True)


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


# =========================
# GENERATE BUTTON
# =========================
generate_btn = st.button("Generate Captions →")


# =========================
# GENERATE CAPTIONS
# =========================
if generate_btn:

    with st.spinner("Creating your captions... ⚡"):

        try:
            # Automatically reads GROQ_API_KEY from Streamlit Secrets
            client = get_client()

            captions, elapsed = generate_captions(
                topic,
                style,
                client,
            )

            hashtags = make_hashtags(topic, style)

            # Save results in session
            st.session_state["captions"] = captions
            st.session_state["hashtags"] = hashtags
            st.session_state["elapsed"] = elapsed

        except ValueError as e:
            st.error(f"⚠️ {e}")

        except Exception as e:
            st.error(f"❌ Generation failed: {e}")


# =========================
# DISPLAY RESULTS
# =========================
if st.session_state["captions"]:

    captions = st.session_state["captions"]
    hashtags = st.session_state["hashtags"]
    elapsed = st.session_state["elapsed"]

    # Captions heading
    st.markdown(
        '<div class="section-label">📝 Captions</div>',
        unsafe_allow_html=True,
    )

    # Individual caption cards
    for i, cap in enumerate(captions, 1):

        safe_caption = (
            str(cap)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        st.markdown(f"""
        <div class="caption-card">
            <span class="caption-num">{i:02d}</span>
            <span class="caption-text">{safe_caption}</span>
        </div>
        """, unsafe_allow_html=True)

    # Copy all captions
    all_captions_text = "\n".join(
        f"{i}. {c}"
        for i, c in enumerate(captions, 1)
    )

    st.text_area(
        "Copy all captions",
        value=all_captions_text,
        height=140,
        label_visibility="collapsed",
    )

    # Hashtags heading
    st.markdown(
        '<div class="section-label">#️⃣ Hashtags</div>',
        unsafe_allow_html=True,
    )

    # Hashtag styling
    hashtag_html = " ".join(
        f'<span>{tag}</span>'
        for tag in hashtags.split()
    )

    st.markdown(
        f'<div class="hashtag-box">{hashtag_html}</div>',
        unsafe_allow_html=True,
    )

    # Copy hashtags
    st.text_area(
        "Copy hashtags",
        value=hashtags,
        height=68,
        label_visibility="collapsed",
    )

    # Generation speed
    st.markdown(
        f'<div class="speed-badge">⏱ {elapsed}s</div>',
        unsafe_allow_html=True,
    )

    # Footer
    st.markdown("---")

    st.markdown(
        '<p style="text-align:center;color:#777;font-size:0.75rem;">'
        'Built with Groq AI · Llama 3.1'
        '</p>',
        unsafe_allow_html=True,
    )
