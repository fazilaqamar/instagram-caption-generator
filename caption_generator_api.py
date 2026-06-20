import streamlit as st
import requests
import json
import re
import time
from datetime import datetime

# ============================================
# API KEY MANAGEMENT
# ============================================

def get_groq_api_key():
    try:
        return st.secrets.get("GROQ_API_KEY")
    except:
        return ""

GROQ_API_KEY = get_groq_api_key()
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
    if api_key:
        return {"api_key": api_key}
    return {"api_key": GROQ_API_KEY}

def generate_captions(topic, style, client, language="English", num_captions=5, creativity=0.9):
    lang_instruction = f"Write in {language}." if language != "English" else ""
    
    prompt = f"""Generate exactly {num_captions} Instagram captions about {topic} in {style} style. {lang_instruction}

Rules:
- NO introductions
- Start with 1.
- Each caption: 10-25 words
- Use 1-3 emojis
- Make them unique

Format:
1. [caption]
2. [caption]
3. [caption]
4. [caption]
5. [caption]"""

    headers = {
        "Authorization": f"Bearer {client['api_key']}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "Generate ONLY captions. Start directly with number 1. No introductions."},
            {"role": "user", "content": prompt}
        ],
        "temperature": creativity,
        "max_tokens": 400
    }
    
    start = time.time()
    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=data)
        elapsed = round(time.time() - start, 2)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            captions = []
            for line in content.split('\n'):
                line = line.strip()
                match = re.match(r'^\s*(\d+)[.)]\s*(.+)', line)
                if match:
                    caption = match.group(2).strip()
                    if not caption.lower().startswith(('here are', 'check out', 'some')):
                        captions.append(caption)
            
            while len(captions) < num_captions:
                captions.append(f"✨ {style} {topic} caption {len(captions)+1}")
            
            return captions[:num_captions], elapsed
        else:
            return [], 0
            
    except Exception as e:
        return [], 0

def make_hashtags(topic, style):
    hashtag_map = {
        "cars": ["#carsofinstagram", "#dreamcar", "#automotive", "#carlover"],
        "travel": ["#travelgram", "#wanderlust", "#exploremore", "#vacationmode"],
        "fashion": ["#fashionstyle", "#ootd", "#outfitcheck", "#styleinspo"],
        "fitness": ["#fitcheck", "#gymrat", "#gains", "#workout"],
        "food": ["#foodie", "#instafood", "#foodporn", "#nomnomnom"],
        "nature": ["#earthpix", "#naturephotography", "#outdoors", "#natgeo"],
        "tech": ["#techbro", "#gadgets", "#innovation", "#techlife"],
        "beauty": ["#glowup", "#skincare", "#makeuptok", "#beautytips"],
        "pets": ["#petlover", "#dogsofinstagram", "#catsofinstagram", "#furryfriends"],
        "music": ["#musiclover", "#songwriter", "#musician", "#livemusic"],
        "art": ["#artwork", "#artist", "#creative", "#artgram"],
        "photography": ["#photographer", "#photooftheday", "#capturethemoment", "#lens"],
        "business": ["#entrepreneur", "#businessowner", "#success", "#startup"],
        "entrepreneur": ["#entrepreneurlife", "#hustle", "#successmindset", "#businessgrowth"],
        "lifestyle": ["#lifestyle", "#lifestyleblogger", "#dailyvibes", "#mindfulness"],
        "wellness": ["#wellness", "#selfcare", "#healthyliving", "#mindfulness"]
    }
    
    style_tags = {
        "funny": "#lol", "luxury": "#luxury", "motivational": "#mindset",
        "aesthetic": "#aesthetic", "bold": "#bold", "emotional": "#feelings",
        "savage": "#savage", "relatable": "#relatable", "poetic": "#poetry",
        "witty": "#witty", "inspirational": "#inspire", "vibes": "#vibes"
    }
    
    tags = hashtag_map.get(topic, ["#instagram", "#viral"])
    style_tag = style_tags.get(style, "#content")
    default = ["#viral", "#instagram", "#trending", "#fyp"]
    
    all_tags = tags + [style_tag] + default
    return " ".join(list(dict.fromkeys(all_tags))[:12])

# ============================================
# FAVORITES FUNCTIONS
# ============================================

def save_favorite_caption(caption, topic, style):
    import os
    try:
        favorites_file = "data/favorites.json"
        os.makedirs("data", exist_ok=True)
        try:
            with open(favorites_file, 'r') as f:
                favorites = json.load(f)
        except:
            favorites = []
        favorites.append({
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "style": style,
            "caption": caption
        })
        with open(favorites_file, 'w') as f:
            json.dump(favorites, f, indent=2)
        return True
    except:
        return False

def get_favorites():
    try:
        with open("data/favorites.json", 'r') as f:
            return json.load(f)
    except:
        return []

def delete_favorite(index):
    try:
        favorites = get_favorites()
        if 0 <= index < len(favorites):
            del favorites[index]
            with open("data/favorites.json", 'w') as f:
                json.dump(favorites, f, indent=2)
            return True
    except:
        return False

def clear_all_favorites():
    try:
        with open("data/favorites.json", 'w') as f:
            json.dump([], f)
        return True
    except:
        return False
