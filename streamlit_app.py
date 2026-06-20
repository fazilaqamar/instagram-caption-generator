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

st.set_page_config(
    page_title="⚡ AI Caption Generator",
    page_icon="✨",
    layout="wide"
)

# ============================================
# COMPLETE DARK THEME - LANGUAGE FIXED
# ============================================
st.markdown("""
<style>
    /* Force dark background on everything */
    .stApp {
        background: #0a0a0f !important;
    }
    
    .main .block-container {
        background: transparent !important;
        max-width: 900px;
        padding: 2rem !important;
    }
    
    /* ALL TEXT WHITE */
    * {
        color: #ffffff !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #ffffff !important;
    }
    
    /* ========== SELECTBOX - LANGUAGE FIX ========== */
    /* Main selectbox container */
    .stSelectbox > div > div {
        background-color: #1a1a2e !important;
        border: 1px solid #333333 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    
    .stSelectbox > div > div > div {
        color: #ffffff !important;
        background-color: #1a1a2e !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #4facfe !important;
    }
    
    /* Dropdown menu - THE IMPORTANT PART! */
    ul[role="listbox"] {
        background-color: #1a1a2e !important;
        border: 1px solid #333333 !important;
        border-radius: 10px !important;
        padding: 4px 0 !important;
    }
    
    ul[role="listbox"] li {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        padding: 8px 12px !important;
        font-size: 0.9rem !important;
    }
    
    ul[role="listbox"] li:hover {
        background-color: #2a2a4e !important;
    }
    
    ul[role="listbox"] li[aria-selected="true"] {
        background-color: #4facfe !important;
        color: #ffffff !important;
    }
    
    /* Selectbox label */
    .stSelectbox label {
        color: rgba(255,255,255,0.8) !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        color: #ffffff !important;
    }
    .stSlider [data-baseweb="slider"] > div > div {
        background: linear-gradient(90deg, #f093fb, #4facfe) !important;
    }
    .stSlider label {
        color: rgba(255,255,255,0.8) !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        background-color: #1a1a2e !important;
        border: 1px solid #333333 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    
    /* Text Area */
    .stTextArea > div > div > textarea {
        background-color: #1a1a2e !important;
        border: 1px solid #333333 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #4facfe !important;
    }
    
    /* Generate Button */
    .stButton > button {
        background: linear-gradient(135deg, #f093fb, #f5576c, #4facfe) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.9rem !important;
        width: 100% !important;
        font-size: 1rem !important;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(245, 87, 108, 0.4);
    }
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        background-color: #1a1a2e !important;
        border: 1px solid #333333 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
    }
    .stDownloadButton > button:hover {
        background-color: #2a2a4e !important;
        border-color: #4facfe !important;
    }
    
    /* Caption Cards */
    .caption-card {
        background-color: #1a1a2e !important;
        border: 1px solid #333333 !important;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #4facfe;
    }
    .caption-card:hover {
        background-color: #2a2a4e !important;
    }
    
    /* Hashtag Box */
    .hashtag-box {
        background-color: #1a1a2e !important;
        border: 1px solid #333333 !important;
        border-radius: 12px;
        padding: 1rem;
        font-size: 0.85rem;
        line-height: 2;
    }
    .hashtag-box span {
        color: #4facfe !important;
        margin-right: 4px;
    }
    
    /* Favorite Box */
    .favorite-box {
        background-color: #1a1a2e !important;
        border: 1px solid #333333 !important;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        border-left: 4px solid #ff9800;
    }
    
    /* Info/Success/Error Messages */
    .stAlert {
        background-color: #1a1a2e !important;
        border-color: #333333 !important;
    }
    .stAlert p {
        color: #ffffff !important;
    }
    .stSuccess {
        background-color: #1a2e1a !important;
        border-color: #4caf50 !important;
    }
    .stError {
        background-color: #2e1a1a !important;
        border-color: #f44336 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        color: #ffffff !important;
    }
    
    /* Hide branding */
    #MainMenu, footer, header {
        display: none !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.05) !important;
    }
    
    /* Number Input */
    .stNumberInput > div > div > input {
        background-color: #1a1a2e !important;
        border: 1px solid #333333 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem;">
    <h1 style="font-size: 3rem; font-weight: 700; background: linear-gradient(135deg, #f093fb, #f5576c, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">✨ AI Caption Generator</h1>
    <p style="color: rgba(255,255,255,0.5); font-size: 1rem; letter-spacing: 0.3em; text-transform: uppercase; margin-top: 0.5rem;">Instagram Captions · Powered by Groq</p>
    <span style="display: inline-block; background: rgba(79, 172, 254, 0.2); border: 1px solid rgba(79, 172, 254, 0.3); color: #4facfe; padding: 0.2rem 1rem; border-radius: 20px; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase;">⚡ Llama 3.1</span>
</div>
""", unsafe_allow_html=True)

# ============================================
# SETTINGS
# ============================================
st.markdown("---")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    topic = st.selectbox("📚 Topic", VALID_TOPICS)

with col2:
    style = st.selectbox("🎨 Style", VALID_STYLES)

with col3:
    num_captions = st.slider("📝 Count", 3, 8, 5)

col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "🌐 Language",
        ["English", "Spanish", "French", "German", "Hindi", "Urdu", "Arabic"],
        index=0
    )

with col2:
    creativity = st.slider(
        "🎨 Creativity",
        0.0, 1.0, 0.9, 0.1,
        help="Higher = more creative"
    )

# ============================================
# GENERATE BUTTON
# ============================================
if st.button("✨ Generate Captions", type="primary", use_container_width=True):
    with st.spinner("🎨 Crafting your captions..."):
        try:
            client = get_client()
            captions, elapsed = generate_captions(
                topic, style, client,
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
    
    st.markdown(f"""
    <div style="display: inline-block; background: rgba(79, 172, 254, 0.1); border: 1px solid rgba(79, 172, 254, 0.15); color: rgba(255,255,255,0.5); padding: 0.2rem 1rem; border-radius: 20px; font-size: 0.7rem; margin-bottom: 1rem;">
        ⏱ Generated in {elapsed}s
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3 style="color: #ffffff; margin-top: 0.5rem;">📝 Your Captions</h3>', unsafe_allow_html=True)
    
    for i, cap in enumerate(captions, 1):
        char_count = len(cap)
        color = "good" if char_count <= 150 else "ok" if char_count <= 200 else "long"
        
        col1, col2 = st.columns([12, 1])
        with col1:
            st.markdown(f"""
            <div class="caption-card">
                <span style="color: rgba(255,255,255,0.3); font-size: 0.8rem; font-weight: 700; background: rgba(255,255,255,0.05); padding: 0.1rem 0.6rem; border-radius: 20px; margin-right: 0.5rem;">#{i}</span>
                <span style="color: #ffffff; font-size: 1rem; line-height: 1.6;">{cap}</span>
                <span style="font-size: 0.7rem; margin-left: 0.5rem; color: {'#4caf50' if char_count <= 150 else '#ff9800' if char_count <= 200 else '#f44336'} !important;">· {char_count}/150</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("⭐", key=f"fav_{i}"):
                if save_favorite_caption(cap, topic, style):
                    st.success("✅ Saved!")
                    st.rerun()
    
    # Copy and Download
    all_text = "\n".join(f"{i}. {c}" for i, c in enumerate(captions, 1))
    
    st.markdown('<h3 style="color: #ffffff; margin-top: 1.5rem;">📋 Copy & Download</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.text_area("Copy all captions", value=all_text, height=100, label_visibility="collapsed")
    with col2:
        st.download_button(
            label="📥 Download TXT",
            data=all_text,
            file_name=f"captions_{topic}_{style}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col3:
        csv_data = "Caption,Character Count\n" + "\n".join(f'"{c}",{len(c)}' for c in captions)
        st.download_button(
            label="📊 Download CSV",
            data=csv_data,
            file_name=f"captions_{topic}_{style}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Hashtags
    st.markdown('<h3 style="color: #ffffff; margin-top: 1.5rem;">#️⃣ Hashtags</h3>', unsafe_allow_html=True)
    hashtag_html = " ".join(f'<span>{tag}</span>' for tag in hashtags.split())
    st.markdown(f'<div class="hashtag-box">{hashtag_html}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.text_area("Copy hashtags", value=hashtags, height=60, label_visibility="collapsed")
    with col2:
        st.download_button(
            label="📥 Download Hashtags",
            data=hashtags,
            file_name=f"hashtags_{topic}_{style}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ============================================
# FAVORITES
# ============================================
st.markdown("---")
st.markdown('<h3 style="color: #ffffff;">⭐ Your Favorites</h3>', unsafe_allow_html=True)

favorites = get_favorites()

if favorites:
    for idx, fav in enumerate(reversed(favorites)):
        st.markdown(f"""
        <div class="favorite-box">
            <span style="color: rgba(255,255,255,0.4); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em;">📌 {fav['topic'].upper()} · {fav['style'].upper()} · {fav['timestamp'][:16]}</span>
            <div style="color: #ffffff; font-size: 0.9rem; margin-top: 0.2rem;">{fav['caption']}</div>
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
