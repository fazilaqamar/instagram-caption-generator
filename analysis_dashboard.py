import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime

st.set_page_config(
    page_title="Caption Generator Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Caption Generator Analytics Dashboard")
st.markdown("Analyze your AI caption generation patterns!")

# Load data
try:
    with open('caption_data.json', 'r') as f:
        data = json.load(f)
    
    if data and len(data) > 0:
        df = pd.DataFrame(data)
        st.success(f"✅ Found {len(df)} records!")
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Create three columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Generations", len(df))
        with col2:
            if len(df) > 0:
                st.metric("Avg Response Time", f"{df['response_time'].mean():.2f}s")
            else:
                st.metric("Avg Response Time", "0.00s")
        with col3:
            if len(df) > 0:
                st.metric("Most Popular Topic", df['topic'].mode().iloc[0])
            else:
                st.metric("Most Popular Topic", "N/A")
        
        if len(df) > 0:
            # Row 1: Time series and topic distribution
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Generations Over Time")
                fig, ax = plt.subplots(figsize=(10, 4))
                df['date'] = df['timestamp'].dt.date
                daily_counts = df.groupby('date').size()
                daily_counts.plot(kind='line', ax=ax, color='#764ba2')
                ax.set_xlabel("Date")
                ax.set_ylabel("Number of Generations")
                st.pyplot(fig)
            
            with col2:
                st.subheader("📊 Topic Distribution")
                fig, ax = plt.subplots(figsize=(8, 4))
                df['topic'].value_counts().plot(kind='bar', ax=ax, color='#667eea')
                ax.set_xlabel("Topic")
                ax.set_ylabel("Count")
                plt.xticks(rotation=45)
                st.pyplot(fig)
            
            # Row 2: Style distribution and response times
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎨 Style Distribution")
                fig, ax = plt.subplots(figsize=(8, 4))
                df['style'].value_counts().plot(kind='bar', ax=ax, color='#e74c3c')
                ax.set_xlabel("Style")
                ax.set_ylabel("Count")
                plt.xticks(rotation=45)
                st.pyplot(fig)
            
            with col2:
                st.subheader("⏱️ Average Response Time by Topic")
                fig, ax = plt.subplots(figsize=(8, 4))
                df.groupby('topic')['response_time'].mean().plot(kind='bar', ax=ax, color='#2ecc71')
                ax.set_xlabel("Topic")
                ax.set_ylabel("Response Time (seconds)")
                plt.xticks(rotation=45)
                st.pyplot(fig)
            
            # Raw data table
            st.subheader("📋 Detailed Data")
            st.dataframe(df[['timestamp', 'topic', 'style', 'num_captions', 'response_time']])
            
            # Export functionality
            st.sidebar.header("Export Data")
            if st.sidebar.button("Export to Excel"):
                df.to_excel("caption_data_export.xlsx", index=False)
                st.sidebar.success("✅ Data exported to caption_data_export.xlsx")
        else:
            st.warning("No data available with current filters.")
    else:
        st.info("📭 No data available. Start generating captions to see analytics!")
        
except FileNotFoundError:
    st.info("📭 No data file found. Start using the caption generator to collect data!")
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")