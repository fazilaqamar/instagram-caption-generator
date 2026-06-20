"""
Instagram Caption Generator - Main Application
Streamlit UI with all features
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================
# PAGE CONFIGURATION - MUST BE FIRST!
# ============================================

st.set_page_config(
    page_title="Instagram Caption Generator Pro",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# IMPORT BACKEND FUNCTIONS
# ============================================

from caption_generator_api import (
    VALID_TOPICS,
    VALID_STYLES,
    get_client,
    generate_captions,
    make_hashtags,
    save_favorite_caption,
    get_favorites,
    delete_favorite,
    clear_all_favorites
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
    <style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .caption-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.2rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #764ba2;
        transition: all 0.3s ease;
    }
    .caption-box:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .hashtag-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
        font-size: 0.9rem;
        word-wrap: break-word;
    }
    .favorite-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ff9800;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 0.5rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================

if 'history' not in st.session_state:
    st.session_state.history = []
if 'captions' not in st.session_state:
    st.session_state.captions = []
if 'hashtags' not in st.session_state:
    st.session_state.hashtags = ""
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = None
if 'current_style' not in st.session_state:
    st.session_state.current_style = None
if 'generated_time' not in st.session_state:
    st.session_state.generated_time = 0

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # API Key
    api_key = st.text_input("🔑 Groq API Key (optional)", type="password", 
                           placeholder="Leave blank to use default")
    
    # Language selection
    language = st.selectbox(
        "🌐 Language",
        options=["English", "Spanish", "French", "German", "Hindi", "Urdu", "Arabic"],
        index=0
    )
    
    # Number of captions
    num_captions = st.slider(
        "📝 Number of Captions",
        min_value=3,
        max_value=8,
        value=5,
        step=1
    )
    
    # Creativity level
    creativity = st.slider(
        "🎨 Creativity Level",
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        step=0.1,
        help="Higher = more creative but less predictable"
    )
    
    st.divider()
    
    # Stats
    st.markdown("### 📊 Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Topics", len(VALID_TOPICS))
    with col2:
        st.metric("Styles", len(VALID_STYLES))
    
    favorites = get_favorites()
    st.metric("⭐ Favorites", len(favorites))
    
    st.divider()
    st.caption("Made with ❤️ using Groq AI")

# ============================================
# MAIN TITLE
# ============================================

st.markdown('<h1 class="main-title">🎨 Instagram Caption Generator Pro</h1>', unsafe_allow_html=True)
st.markdown("Generate creative, viral-worthy Instagram captions with AI!")

# ============================================
# TABS
# ============================================

tab1, tab2, tab3 = st.tabs(["✨ Generate", "⭐ Favorites", "📜 History"])

# ============================================
# TAB 1: GENERATE
# ============================================

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.selectbox("📚 Select Topic", options=VALID_TOPICS, index=0)
    
    with col2:
        style = st.selectbox("🎨 Select Style", options=VALID_STYLES, index=0)
    
    if st.button("✨ Generate Viral Captions", type="primary"):
        with st.spinner("🎨 Cooking up some fire captions..."):
            try:
                client = get_client(api_key if api_key else None)
                captions, elapsed = generate_captions(
                    topic, style, client,
                    language=language,
                    num_captions=num_captions,
                    creativity=creativity
                )
                
                if captions:
                    hashtags_text = make_hashtags(topic, style)
                    
                    # STORE IN SESSION STATE
                    st.session_state.captions = captions
                    st.session_state.hashtags = hashtags_text
                    st.session_state.current_topic = topic
                    st.session_state.current_style = style
                    st.session_state.generated_time = elapsed
                    
                    st.session_state.history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "topic": topic,
                        "style": style,
                        "captions": captions,
                        "hashtags": hashtags_text
                    })
                    
                    st.success(f"🔥 Generated {len(captions)} fire captions in {elapsed}s!")
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # ============================================
    # DISPLAY SAVED CAPTIONS FROM SESSION STATE
    # ============================================
    
    if st.session_state.captions:
        st.markdown("---")
        st.markdown("### 📝 Your Viral Captions")
        
        for i, caption in enumerate(st.session_state.captions, 1):
            char_count = len(caption)
            col1, col2 = st.columns([10, 1])
            
            with col1:
                color = "green" if char_count <= 150 else "orange" if char_count <= 200 else "red"
                st.markdown(f"""
                    <div class="caption-box">
                        <strong>{i}.</strong> {caption}
                        <br>
                        <small style="color: {color}">
                            📝 {char_count}/150 characters
                        </small>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("⭐", key=f"fav_{i}_{datetime.now().timestamp()}"):
                    if save_favorite_caption(caption, st.session_state.current_topic, st.session_state.current_style):
                        st.success("✅ Saved to favorites!")
                        st.rerun()
        
        # Display hashtags
        if st.session_state.hashtags:
            st.markdown("### 📌 Suggested Hashtags")
            st.markdown(f'<div class="hashtag-box">{st.session_state.hashtags}</div>', unsafe_allow_html=True)
        
        # Download options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            txt_data = "\n".join([f"{i}. {cap}" for i, cap in enumerate(st.session_state.captions, 1)])
            txt_data += f"\n\n{st.session_state.hashtags}"
            st.download_button(
                label="📥 Download TXT",
                data=txt_data,
                file_name=f"captions_{st.session_state.current_topic}_{st.session_state.current_style}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        with col2:
            df = pd.DataFrame({
                'Caption': st.session_state.captions,
                'Topic': [st.session_state.current_topic] * len(st.session_state.captions),
                'Style': [st.session_state.current_style] * len(st.session_state.captions),
                'Character_Count': [len(c) for c in st.session_state.captions]
            })
            csv = df.to_csv(index=False)
            st.download_button(
                label="📊 Download CSV",
                data=csv,
                file_name=f"captions_{st.session_state.current_topic}_{st.session_state.current_style}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col3:
            full_text = "\n".join([f"{i}. {cap}" for i, cap in enumerate(st.session_state.captions, 1)])
            full_text += f"\n\n{st.session_state.hashtags}"
            st.text_area("📋 Copy All", full_text, height=120, key="copy_text")

# ============================================
# TAB 2: FAVORITES
# ============================================

with tab2:
    st.subheader("⭐ Your Favorite Captions")
    
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🗑️ Clear All"):
            if clear_all_favorites():
                st.success("All favorites cleared!")
                st.rerun()
    
    favorites = get_favorites()
    
    if favorites:
        st.success(f"✅ You have {len(favorites)} favorite captions!")
        
        for idx, fav in enumerate(reversed(favorites)):
            with st.container():
                st.markdown(f"""
                    <div class="favorite-box">
                        <strong>📌 {fav['topic'].upper()} - {fav['style'].upper()}</strong>
                        <br>
                        <small>📅 {fav['timestamp'][:16]}</small>
                    </div>
                """, unsafe_allow_html=True)
                
                st.write(f"💬 {fav['caption']}")
                
                if st.button(f"🗑️ Delete", key=f"del_{idx}"):
                    if delete_favorite(len(favorites) - 1 - idx):
                        st.success("Deleted!")
                        st.rerun()
                st.divider()
    else:
        st.info("💡 No favorites yet. Click ⭐ on any caption to save it!")

# ============================================
# TAB 3: HISTORY
# ============================================

with tab3:
    st.subheader("📜 Generation History")
    
    if st.session_state.history:
        st.info(f"📊 Showing {len(st.session_state.history)} generations")
        
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"🕐 {item['timestamp']} - {item['topic'].upper()} ({item['style']})"):
                for i, cap in enumerate(item['captions'], 1):
                    st.write(f"{i}. {cap}")
                st.write(f"**Hashtags:** {item['hashtags']}")
    else:
        st.info("📭 No history yet. Generate some captions!")

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Made with ❤️ using Groq AI • 
    <a href="https://console.groq.com/" target="_blank">Get your API key</a>
</div>
""", unsafe_allow_html=True)