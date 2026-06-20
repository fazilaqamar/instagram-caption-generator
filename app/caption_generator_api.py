"""
Caption Generator API - Backend Logic
Handles all API calls and data processing
"""

import os
import streamlit as st
import requests
import json
import re
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================
# API KEY MANAGEMENT
# ============================================

def get_groq_api_key():
    """Get API key from Streamlit Secrets or .env file"""
    try:
        # For Streamlit Cloud
        return st.secrets.get("GROQ_API_KEY")
    except (FileNotFoundError, AttributeError):
        # For local development
        return os.getenv("GROQ_API_KEY")

# Get API key
GROQ_API_KEY = get_groq_api_key()

# If no API key found, use default
if not GROQ_API_KEY:
    GROQ_API_KEY = "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"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ============================================
# CONSTANTS
# ============================================

VALID_TOPICS = [
    "cars", "travel", "fashion", "fitness",
    "food", "nature", "tech", "beauty",
    "pets", "music", "art", "photography",
    "business", "entrepreneur", "lifestyle", "wellness"
]

VALID_STYLES = [
    "funny", "luxury", "motivational",
    "aesthetic", "bold", "emotional",
    "savage", "relatable", "poetic",
    "witty", "inspirational", "vibes"
]

# ============================================
# API FUNCTIONS
# ============================================

def get_client(api_key=None):
    """Initialize Groq client"""
    if api_key:
        return {"api_key": api_key}
    return {"api_key": GROQ_API_KEY}

def generate_captions(topic, style, client, language="English", num_captions=5, creativity=0.9):
    """Generate captions using Groq API"""
    
    # Language instruction
    lang_instruction = f"Write in {language}." if language != "English" else ""
    
    prompt = f"""You are a professional social media copywriter.

Generate exactly {num_captions} Instagram captions about {topic} in {style} style. {lang_instruction}

CRITICAL RULES:
- NO INTRODUCTORY LINES (no "Here are...", "Check out...", "Some captions...", "Here are 5...")
- START DIRECTLY with caption 1
- Each caption must be 10-25 words
- Use 1-3 emojis naturally
- Make them unique and engaging
- NO repetitive phrases
- NO hashtags in the captions

Format EXACTLY like this:
1. [Your first caption]
2. [Your second caption]
3. [Your third caption]
4. [Your fourth caption]
5. [Your fifth caption]

Now generate {num_captions} {style} captions about {topic}:
"""

    headers = {
        "Authorization": f"Bearer {client['api_key']}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a professional Instagram copywriter. Generate ONLY captions, no introductions. Start directly with number 1."},
            {"role": "user", "content": prompt}
        ],
        "temperature": creativity,
        "max_tokens": 400
    }
    
    start_time = time.time()
    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=data)
        elapsed = round(time.time() - start_time, 2)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Extract captions
            captions = []
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Match numbered lines
                match = re.match(r'^\s*(\d+)[.)]\s*(.+)', line)
                if match:
                    caption = match.group(2).strip()
                    # Skip if it looks like an introduction
                    if not any([
                        caption.lower().startswith('here are'),
                        caption.lower().startswith('check out'),
                        caption.lower().startswith('some'),
                        caption.lower().startswith('these are'),
                        caption.lower().startswith('here is'),
                        'caption' in caption.lower()[:30],
                        'captions' in caption.lower()[:30],
                        ':' in caption and len(caption) < 40
                    ]):
                        captions.append(caption)
                elif line and len(captions) < num_captions:
                    # If not numbered, try to extract
                    if not any([
                        line.lower().startswith('here are'),
                        line.lower().startswith('check out'),
                        line.lower().startswith('some'),
                        'caption' in line.lower()[:30],
                        'captions' in line.lower()[:30],
                        len(line) < 10
                    ]):
                        captions.append(line)
            
            # Filter out any remaining introductions
            filtered_captions = []
            for cap in captions:
                if not any([
                    cap.lower().startswith('here are'),
                    cap.lower().startswith('check out'),
                    cap.lower().startswith('some'),
                    cap.lower().startswith('these are'),
                    cap.lower().startswith('here is'),
                    'caption' in cap.lower()[:30] and len(cap) < 50,
                    'captions' in cap.lower()[:30] and len(cap) < 50,
                    len(cap) < 10
                ]):
                    filtered_captions.append(cap)
            
            captions = filtered_captions[:num_captions]
            
            # If we don't have enough captions, try harder to extract
            if len(captions) < num_captions:
                all_lines = content.split('\n')
                for line in all_lines:
                    line = line.strip()
                    if not line:
                        continue
                    if re.match(r'^\s*\d+[.)]\s*', line):
                        clean = re.sub(r'^\s*\d+[.)]\s*', '', line)
                        if clean and len(clean) > 10:
                            if not any([
                                clean.lower().startswith('here are'),
                                clean.lower().startswith('check out'),
                                'caption' in clean.lower()[:30],
                                'captions' in clean.lower()[:30],
                            ]):
                                captions.append(clean)
            
            # Ensure we have exactly num_captions
            captions = captions[:num_captions]
            
            # If still not enough, use fallback
            while len(captions) < num_captions:
                captions.append(f"✨ {style} {topic} caption {len(captions)+1}")
            
            return captions, elapsed
        else:
            print(f"API Error: {response.status_code}")
            print(response.text)
            return [], 0
            
    except Exception as e:
        print(f"Error: {e}")
        return [], 0

# ============================================
# FAVORITES FUNCTIONS
# ============================================

def save_favorite_caption(caption, topic, style):
    """Save a favorite caption to favorites.json"""
    try:
        favorites_file = "data/favorites.json"
        os.makedirs("data", exist_ok=True)
        
        try:
            with open(favorites_file, 'r') as f:
                favorites = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            favorites = []
        
        favorite = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "style": style,
            "caption": caption
        }
        favorites.append(favorite)
        
        with open(favorites_file, 'w') as f:
            json.dump(favorites, f, indent=2)
        return True
        
    except Exception as e:
        print(f"Error saving favorite: {e}")
        return False

def get_favorites():
    """Get all favorite captions"""
    try:
        with open("data/favorites.json", 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def delete_favorite(index):
    """Delete a favorite by index"""
    try:
        favorites = get_favorites()
        if 0 <= index < len(favorites):
            del favorites[index]
            with open("data/favorites.json", 'w') as f:
                json.dump(favorites, f, indent=2)
            return True
    except Exception as e:
        print(f"Error deleting favorite: {e}")
    return False

def clear_all_favorites():
    """Clear all favorites"""
    try:
        with open("data/favorites.json", 'w') as f:
            json.dump([], f)
        return True
    except Exception as e:
        print(f"Error clearing favorites: {e}")
        return False