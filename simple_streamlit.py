# Add to session state initialization
if 'history' not in st.session_state:
    st.session_state.history = []

# After generating captions, add to history
if 'history' not in st.session_state:
    st.session_state.history = []
    
# When you generate captions, add to history
if captions:
    st.session_state.history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "topic": topic,
        "style": style,
        "captions": captions,
        "hashtags": hashtags
    })