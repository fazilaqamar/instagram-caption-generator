import streamlit as st
from caption_generator_api import (
    get_client,
    generate_captions,
    make_hashtags,
    VALID_TOPICS,
    VALID_STYLES
)

st.set_page_config(
    page_title="AI Caption Generator",
    page_icon="⚡",
    layout="centered",
)

st.markdown("""
<style>
.main .block-container {
    max-width: 720px;
    padding: 2rem 1.5rem 4rem;
}
.app-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid #1e1e1e;
    margin-bottom: 2rem;
}
.app-header h1 {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #fff 0%, #888 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.app-header p {
    color: #555;
    font-size: 0.9rem;
    margin: 0;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.settings-box {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
}
.settings-box label {
    color: #888;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
div.stButton > button {
    width: 100%;
    background: #f0f0f0;
    color: #0a0a0a;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
}
div.stButton > button:hover {
    background: #fff;
    transform: translateY(-1px);
}
.caption-card {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
}
.caption-text {
    font-size: 0.95rem;
    color: #e8e8e8;
}
.hashtag-box {
    background: #0e0e0e;
    border: 1px dashed #222;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: #555;
    line-height: 1.8;
}
.hashtag-box span {
    color: #3a7fff;
    margin-right: 4px;
}
textarea {
    background: #111 !important;
    border: 1px solid #222 !important;
    color: #888 !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
}
div[data-baseweb="select"] > div {
    background: #111 !important;
    border: 1px solid #222 !important;
    border-radius: 8px !important;
    color: #f0f0f0 !important;
}
div[data-baseweb="slider"] > div {
    color: #f0f0f0 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="app-header">
    <h1>⚡ Caption Generator</h1>
    <p>Groq AI — Instagram Captions</p>
</div>
""", unsafe_allow_html=True)

# =========================
# SETTINGS - Language & Creativity
# =========================
st.markdown('<div class="settings-box">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "🌐 Language",
        options=["English", "Spanish", "French", "German", "Hindi", "Urdu", "Arabic"],
        index=0
    )

with col2:
    creativity = st.slider(
        "🎨 Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        step=0.1,
        help="Higher = more creative, Lower = more predictable"
    )

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TOPIC & STYLE
# =========================
col1, col2 = st.columns(2)

with col1:
    topic = st.selectbox("📚 Topic", VALID_TOPICS)

with col2:
    style = st.selectbox("🎨 Style", VALID_STYLES)

# =========================
# NUMBER OF CAPTIONS
# =========================
num_captions = st.slider(
    "📝 Number of Captions",
    min_value=3,
    max_value=8,
    value=5,
    step=1
)

# =========================
# GENERATE BUTTON
# =========================
if st.button("✨ Generate Captions", type="primary"):
    with st.spinner("🎨 Cooking up some fire captions..."):
        try:
            client = get_client()
            captions, elapsed = generate_captions(
                topic, 
                style, 
                client,
                language=language,
                num_captions=num_captions,
                creativity=creativity
            )
            hashtags = make_hashtags(topic, style)

            st.session_state["captions"] = captions
            st.session_state["hashtags"] = hashtags
            st.session_state["elapsed"] = elapsed

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("💡 Make sure you've added GROQ_API_KEY to Secrets in Streamlit Cloud settings!")

# =========================
# DISPLAY RESULTS
# =========================
if st.session_state.get("captions"):
    captions = st.session_state["captions"]
    hashtags = st.session_state["hashtags"]
    elapsed = st.session_state["elapsed"]

    st.markdown("---")
    st.markdown("### 📝 Captions")

    for i, cap in enumerate(captions, 1):
        char_count = len(cap)
        color = "green" if char_count <= 150 else "orange" if char_count <= 200 else "red"
        st.markdown(f"""
        <div class="caption-card">
            <span class="caption-text"><strong>{i}.</strong> {cap}</span>
            <br>
            <small style="color: {color};">📝 {char_count}/150 characters</small>
        </div>
        """, unsafe_allow_html=True)

    all_text = "\n".join(f"{i}. {c}" for i, c in enumerate(captions, 1))
    st.text_area("📋 Copy all captions", value=all_text, height=140)

    st.markdown("### #️⃣ Hashtags")
    hashtag_html = " ".join(f'<span>{tag}</span>' for tag in hashtags.split())
    st.markdown(f'<div class="hashtag-box">{hashtag_html}</div>', unsafe_allow_html=True)
    st.text_area("📋 Copy hashtags", value=hashtags, height=68)

    # Download options
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Download TXT",
            data=all_text,
            file_name=f"captions_{topic}_{style}.txt",
            mime="text/plain"
        )
    with col2:
        st.download_button(
            label="📥 Download CSV",
            data=f"Caption,Character Count\n" + "\n".join(f"{c},{len(c)}" for c in captions),
            file_name=f"captions_{topic}_{style}.csv",
            mime="text/csv"
        )

    st.markdown(f"⏱ Generated in {elapsed}s")
