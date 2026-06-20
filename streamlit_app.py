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
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="app-header">
    <h1>⚡ Caption Generator</h1>
    <p>Groq AI — Instagram Captions</p>
</div>
""", unsafe_allow_html=True)

# =========================
# NO API KEY INPUT NEEDED!
# It's loaded from Secrets automatically
# =========================

col1, col2 = st.columns(2)

with col1:
    topic = st.selectbox("Topic", VALID_TOPICS)

with col2:
    style = st.selectbox("Style", VALID_STYLES)

if st.button("Generate Captions"):
    with st.spinner("Generating..."):
        try:
            # Get client with API key from Secrets
            client = get_client()
            captions, elapsed = generate_captions(topic, style, client)
            hashtags = make_hashtags(topic, style)

            st.session_state["captions"] = captions
            st.session_state["hashtags"] = hashtags
            st.session_state["elapsed"] = elapsed

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("💡 Make sure you've added GROQ_API_KEY to Secrets in Streamlit Cloud settings!")

if st.session_state.get("captions"):
    captions = st.session_state["captions"]
    hashtags = st.session_state["hashtags"]
    elapsed = st.session_state["elapsed"]

    st.markdown("### 📝 Captions")

    for i, cap in enumerate(captions, 1):
        st.markdown(f"""
        <div class="caption-card">
            <span class="caption-text">{i}. {cap}</span>
        </div>
        """, unsafe_allow_html=True)

    all_text = "\n".join(f"{i}. {c}" for i, c in enumerate(captions, 1))
    st.text_area("Copy all captions", value=all_text, height=140)

    st.markdown("### #️⃣ Hashtags")
    hashtag_html = " ".join(f'<span>{tag}</span>' for tag in hashtags.split())
    st.markdown(f'<div class="hashtag-box">{hashtag_html}</div>', unsafe_allow_html=True)
    st.text_area("Copy hashtags", value=hashtags, height=68)

    st.markdown(f"⏱ {elapsed}s")