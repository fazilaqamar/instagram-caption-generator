"""
Project Runner - Start all apps at once
"""

import subprocess
import time
import webbrowser

def run_apps():
    print("🚀 Starting all applications...")
    
    # Run main app
    print("1️⃣ Starting Caption Generator...")
    subprocess.Popen(['streamlit', 'run', 'working_app.py'])
    time.sleep(3)
    
    # Run analytics dashboard
    print("2️⃣ Starting Analytics Dashboard...")
    subprocess.Popen(['streamlit', 'run', 'analysis_dashboard.py'])
    time.sleep(3)
    
    # Run portfolio
    print("3️⃣ Starting Portfolio...")
    subprocess.Popen(['streamlit', 'run', 'portfolio_showcase.py'])
    
    print("\n✅ All apps started!")
    print("📊 Main App: http://localhost:8501")
    print("📊 Analytics: http://localhost:8502")
    print("📊 Portfolio: http://localhost:8503")

if __name__ == "__main__":
    run_apps()