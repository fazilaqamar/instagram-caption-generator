import streamlit as st
from caption_generator_api import (
    get_client,
    generate_captions,
    make_hashtags,
    VALID_TOPICS,
    VALID_STYLES,
    save_favorite_caption,
    get_favorites,
    delete_favorite,
    clear_all_favorites
)

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="⚡ AI Caption Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CUSTOM CSS - PREMIUM DESIGN
# ============================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Main Container */
    .main .block-container {
        max-width: 900px;
        padding: 2rem 2rem 4rem;
    }
    
    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Header */
    .app-header {
        text-align: center;
        padding: 2.5rem 0 1.5rem;
        margin-bottom: 2rem;
    }
    .app-header h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .app-header .subtitle {
        color: rgba(255,255,255,0.5);
        font-size: 1rem;
        letter-spacing: 0.3em;
        text-transform: uppercase;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    .app-header .badge {
        display: inline-block;
        background: rgba(79, 172, 254, 0.2);
        border: 1px solid rgba(79, 172, 254, 0.3);
        color: #4facfe;
        padding: 0.2rem 1rem;
        border-radius: 20px;
        font-size: 0.7rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }
    
    /* Labels */
    .stSelectbox label, .stSlider label {
        color: rgba(255,255,255,0.7) !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }
    
    /* Selectbox */
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: #f0f0f0 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: rgba(79, 172, 254, 0.4) !important;
    }
    
    /* Slider */
    div[data-baseweb="slider"] {
        margin-top: 0.5rem;
    }
    .stSlider [data-baseweb="slider"] {
        background: rgba(255,255,255,0.1) !important;
    }
    .stSlider [data-baseweb="slider"] > div > div {
        background: linear-gradient(90deg, #f093fb, #4facfe) !important;
    }
    
    /* Generate Button */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
        color: white;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        border: none;
        border-radius: 14px;
        padding: 0.9rem 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(245, 87, 108, 0.3);
    }
    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 8px 30px rgba(245, 87, 108, 0.5);
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Caption Cards */
    .caption-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .caption-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #f093fb, #4facfe);
        border-radius: 4px 0 0 4px;
    }
    .caption-card:hover {
        background: rgba(255,255,255,0.08);
        border-color: rgba(255,255,255,0.15);
        transform: translateX(4px);
    }
    .caption-number {
        display: inline-block;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        color: rgba(255,255,255,0.3);
        background: rgba(255,255,255,0.06);
        padding: 0.1rem 0.6rem;
        border-radius: 20px;
        margin-right: 0.8rem;
    }
    .caption-text {
        font-size: 1rem;
        color: #e8e8e8;
        line-height: 1.6;
        font-weight: 400;
    }
    .caption-char {
        font-size: 0.7rem;
        color: rgba(255,255,255,0.3);
        margin-left: 0.5rem;
    }
    .caption-char.good { color: #4caf50; }
    .caption-char.ok { color: #ff9800; }
    .caption-char.long { color: #f44336; }
    
    /* Hashtag Box */
    .hashtag-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1rem 1.5rem;
        font-size: 0.85rem;
        color: rgba(255,255,255,0.6);
        line-height: 2;
        word-break: break-all;
    }
    .hashtag-box span {
        color: #4facfe;
        margin-right: 6px;
        transition: color 0.2s;
    }
    .hashtag-box span:hover {
        color: #f093fb;
        cursor: pointer;
    }
    
    /* Favorite Box */
    .favorite-box {
        background: rgba(255, 152, 0, 0.08);
        border: 1px solid rgba(255, 152, 0, 0.15);
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 0.6rem;
        border-left: 3px solid #ff9800;
        transition: all 0.3s ease;
    }
    .favorite-box:hover {
        background: rgba(255, 152, 0, 0.12);
    }
    .favorite-topic {
        color: rgba(255,255,255,0.4);
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .favorite-caption {
        color: #e8e8e8;
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }
    
    /* Text Area */
    textarea {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        color: rgba(255,255,255,0.7) !important;
        border-radius: 12px !important;
        font-size: 0.85rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    textarea:focus {
        border-color: rgba(79, 172, 254, 0.4) !important;
        box-shadow: 0 0 20px rgba(79, 172, 254, 0.05) !important;
    }
    
    /* Download Buttons */
    .download-btn {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        color: rgba(255,255,255,0.7) !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.8rem !important;
        transition: all 0.3s ease !important;
    }
    .download-btn:hover {
        background: rgba(255,255,255,0.1) !important;
        border-color: rgba(255,255,255,0.2) !important;
    }
    
    /* Section Headers */
    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: rgba(255,255,255,0.8);
        margin: 1.5rem 0 1rem;
        letter-spacing: -0.01em;
    }
    .section-title .emoji {
        margin-right: 0.5rem;
    }
    
    /* Badge - Generation time */
    .gen-badge {
        display: inline-block;
        background: rgba(79, 172, 254, 0.1);
        border: 1px solid rgba(79, 172, 254, 0.15);
        color: rgba(255,255,255,0.5);
        padding: 0.2rem 1rem;
        border-radius: 20px;
        font-size: 0.7rem;
        letter-spacing: 0.05em;
    }
    
    /* Star Button */
    .stButton button[kind="secondary"] {
        background: transparent !important;
        border: none !important;
        font-size: 1.5rem !important;
        padding: 0 !important;
        width: auto !important;
        color: rgba(255,255,255,0.2) !important;
        transition: all 0.2s !important;
    }
    .stButton button[kind="secondary"]:hover {
        color: #ff9800 !important;
        transform: scale(1.2) !important;
    }
    
    /* Remove default Streamlit padding */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255,255,255,0.04);
        border-radius: 12px;
        padding: 0.3rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.4rem 1.2rem;
        color: rgba(255,255,255,0.5);
        font-weight: 500;
        font-size: 0.85rem;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(255,255,255,0.08);
        color: white;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
st.markdown("""
<div class="app-header">
    <h1>✨ AI Caption Generator</h1>
    <div class="subtitle">Instagram Captions · Powered by Groq</div>
    <span class="badge">⚡ Llama 3.1</span>
</div>
""", unsafe_allow_html=True)

# ============================================
# SETTINGS
# ============================================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    topic = st.selectbox("📚 Topic", VALID_TOPICS)

with col2:
    style = st.selectbox("🎨 Style", VALID_STYLES)

with col3:
    num_captions = st.slider(
        "📝 Count",
        min_value=3,
        max_value=8,
        value=5,
        step=1
    )

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
        help="Higher = more creative"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# GENERATE BUTTON
# ============================================
if st.button("✨ Generate Captions", type="primary", use_container_width=True):
    with st.spinner("🎨 Crafting your captions..."):
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
            st.info("💡 Make sure GROQ_API_KEY is in Streamlit Secrets!")

# ============================================
# DISPLAY RESULTS
# ============================================
if st.session_state.get("captions"):
    captions = st.session_state["captions"]
    hashtags = st.session_state["hashtags"]
    elapsed = st.session_state["elapsed"]

    st.markdown(f'<span class="gen-badge">⏱ Generated in {elapsed}s</span>', unsafe_allow_html=True)

    st.markdown('<div class="section-title"><span class="emoji">📝</span> Your Captions</div>', unsafe_allow_html=True)

    for i, cap in enumerate(captions, 1):
        char_count = len(cap)
        color_class = "good" if char_count <= 150 else "ok" if char_count <= 200 else "long"
        
        col1, col2 = st.columns([12, 1])
        with col1:
            st.markdown(f"""
            <div class="caption-card">
                <span class="caption-number">#{i}</span>
                <span class="caption-text">{cap}</span>
                <span class="caption-char {color_class}">· {char_count}/150</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("⭐", key=f"fav_{i}"):
                if save_favorite_caption(cap, topic, style):
                    st.success("✅ Saved!")
                    st.rerun()

    # Copy and Download
    all_text = "\n".join(f"{i}. {c}" for i, c in enumerate(captions, 1))
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.text_area("📋 Copy all captions", value=all_text, height=100, label_visibility="collapsed")
    with col2:
        st.download_button(
            label="📥 Download TXT",
            data=all_text,
            file_name=f"captions_{topic}_{style}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # Hashtags
    st.markdown('<div class="section-title"><span class="emoji">#️⃣</span> Hashtags</div>', unsafe_allow_html=True)
    hashtag_html = " ".join(f'<span>{tag}</span>' for tag in hashtags.split())
    st.markdown(f'<div class="hashtag-box">{hashtag_html}</div>', unsafe_allow_html=True)
    st.text_area("📋 Copy hashtags", value=hashtags, height=60, label_visibility="collapsed")

# ============================================
# FAVORITES
# ============================================
st.markdown("---")
st.markdown('<div class="section-title"><span class="emoji">⭐</span> Your Favorites</div>', unsafe_allow_html=True)

favorites = get_favorites()

if favorites:
    for idx, fav in enumerate(reversed(favorites)):
        with st.container():
            st.markdown(f"""
            <div class="favorite-box">
                <span class="favorite-topic">📌 {fav['topic'].upper()} · {fav['style'].upper()} · {fav['timestamp'][:16]}</span>
                <div class="favorite-caption">{fav['caption']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🗑️ Delete", key=f"del_{idx}"):
                if delete_favorite(len(favorites) - 1 - idx):
                    st.success("Deleted!")
                    st.rerun()
else:
    st.info("💡 No favorites yet. Click ⭐ on any caption to save it!")

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div style="text-align: center; padding: 2rem 0 0.5rem; border-top: 1px solid rgba(255,255,255,0.05); margin-top: 2rem;">
    <span style="color: rgba(255,255,255,0.2); font-size: 0.7rem; letter-spacing: 0.1em;">
        Built with ❤️ · Groq AI · Llama 3.1
    </span>
</div>
""", unsafe_allow_html=True)
