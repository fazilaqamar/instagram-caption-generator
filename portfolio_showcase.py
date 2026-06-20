import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Fazila's AI/ML Portfolio",
    page_icon="🌟",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .skill-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #764ba2;
    }
    .project-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    .achievement-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-title">🌟 Fazila\'s AI/ML Summer Portfolio</h1>', unsafe_allow_html=True)

# Introduction
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## 👋 About Me
    
    I'm a passionate **AI/ML enthusiast** on a journey to become a **Machine Learning Engineer**. 
    This portfolio showcases my summer learning journey in AI, Data Science, and Python programming.
    
    ### 🎯 Summer 2026 Goals:
    - ✅ Strengthen AI/ML Skills
    - ✅ Master Python Programming
    - ✅ Learn Data Analysis & Visualization
    - ✅ Build Portfolio Projects
    - ✅ Start Freelancing Journey
    """)

with col2:
    st.markdown("""
    <div class="achievement-box">
        <h3>📊 Summer Stats</h3>
        <p>🔥 Projects: 3+</p>
        <p>📚 Topics: 16+</p>
        <p>🎨 Styles: 12+</p>
        <p>⚡ API Calls: 100+</p>
    </div>
    """, unsafe_allow_html=True)

# Skills Section
st.markdown("## 🚀 Skills I've Developed")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="skill-box">
        <h4>🐍 Python Programming</h4>
        <ul>
            <li>API Integration</li>
            <li>Data Analysis</li>
            <li>Web Apps (Streamlit)</li>
            <li>Automation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="skill-box">
        <h4>🧠 AI & Machine Learning</h4>
        <ul>
            <li>Prompt Engineering</li>
            <li>LLM Integration</li>
            <li>Model Evaluation</li>
            <li>AI Application Dev</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="skill-box">
        <h4>📊 Data Analysis</h4>
        <ul>
            <li>Pandas</li>
            <li>Matplotlib/Seaborn</li>
            <li>Power BI Basics</li>
            <li>Data Visualization</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Projects Section
st.markdown("## 📁 Featured Projects")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="project-box">
        <h3>📸 AI Caption Generator</h3>
        <p><strong>Tech:</strong> Python, Streamlit, Groq API</p>
        <p><strong>Features:</strong></p>
        <ul>
            <li>16+ Topics</li>
            <li>12+ Styles</li>
            <li>Multi-language</li>
            <li>Analytics Dashboard</li>
        </ul>
        <p><strong>Status:</strong> ✅ Complete</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="project-box">
        <h3>📊 Analytics Dashboard</h3>
        <p><strong>Tech:</strong> Pandas, Matplotlib, Seaborn</p>
        <p><strong>Features:</strong></p>
        <ul>
            <li>Usage Analytics</li>
            <li>Visual Reports</li>
            <li>Data Export</li>
            <li>Performance Metrics</li>
        </ul>
        <p><strong>Status:</strong> ✅ Complete</p>
    </div>
    """, unsafe_allow_html=True)

# Learning Timeline
st.markdown("## 📅 Summer Learning Timeline")

timeline_data = {
    "Week": ["1-2", "3-4", "5-6", "7-8"],
    "Focus": [
        "Python & AI Basics",
        "Data Analysis & Visualization",
        "Git/GitHub & Projects",
        "Freelancing & Portfolio"
    ],
    "Achievements": [
        "Built Caption Generator",
        "Created Dashboards",
        "Git Mastery & Deployment",
        "Started Fiverr/Upwork"
    ]
}

st.table(timeline_data)

# Achievements
st.markdown("## 🏆 Key Achievements")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("✅ Projects", "3+")
with col2:
    st.metric("📚 Skills", "12+")
with col3:
    st.metric("⚡ API Calls", "100+")
with col4:
    st.metric("📊 Lines of Code", "500+")

# Tools & Technologies
st.markdown("## 🛠️ Tools I've Mastered")

tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)

with tech_col1:
    st.markdown("**Languages**")
    st.write("✅ Python")
    st.write("✅ SQL (Basics)")
    
with tech_col2:
    st.markdown("**Libraries**")
    st.write("✅ Pandas")
    st.write("✅ Matplotlib")
    st.write("✅ Streamlit")
    
with tech_col3:
    st.markdown("**AI/ML**")
    st.write("✅ Groq API")
    st.write("✅ Prompt Engineering")
    st.write("✅ LLM Integration")
    
with tech_col4:
    st.markdown("**Tools**")
    st.write("✅ Git/GitHub")
    st.write("✅ VS Code")
    st.write("✅ Power BI")

# Next Steps
st.markdown("## 🚀 Next Steps & Goals")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📈 Immediate Goals
    - [ ] Deploy to Streamlit Cloud
    - [ ] Add more AI features
    - [ ] Build mobile app version
    - [ ] Start freelancing
    
    ### 🔗 Connect With Me
    - [LinkedIn](your-linkedin-url)
    - [GitHub](your-github-url)
    - [Upwork](your-upwork-url)
    """)

with col2:
    st.markdown("""
    ### 💪 Why I'm Ready for Internships
    
    1. **Hands-on Experience**: Built real AI applications
    2. **Full-Stack Skills**: Python + Streamlit + Data Analysis
    3. **Project Portfolio**: 3+ complete projects
    4. **Continuous Learning**: Daily coding and improvement
    5. **Professional Tools**: Git, GitHub, Documentation
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Made with ❤️ as part of my AI/ML Summer Learning Journey<br>
    <small>Last Updated: June 2026</small>
</div>
""", unsafe_allow_html=True)