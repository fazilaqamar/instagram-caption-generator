import os
import re
import time
from datetime import datetime

import requests
import streamlit as st

# ============================================
# API KEY MANAGEMENT
# ============================================

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"
REQUEST_TIMEOUT = 30


def get_groq_api_key():
    """Read GROQ_API_KEY from Streamlit Secrets (fallback: environment variable)."""
    try:
        key = st.secrets.get("GROQ_API_KEY")
        if key:
            return key
    except Exception:
        pass
    return os.environ.get("GROQ_API_KEY", "")


# ============================================
# CONSTANTS
# ============================================

VALID_TOPICS = [
    "cars", "travel", "fashion", "fitness",
    "food", "nature", "tech", "beauty",
    "pets", "music", "art", "photography",
    "business", "entrepreneur", "lifestyle", "wellness",
]

VALID_STYLES = [
    "funny", "luxury", "motivational",
    "aesthetic", "bold", "emotional",
    "savage", "relatable", "poetic",
    "witty", "inspirational", "vibes",
]

# ============================================
# API FUNCTIONS
# ============================================


def get_client(api_key=None):
    key = api_key or get_groq_api_key()
    if not key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it in Manage app > Settings > Secrets."
        )
    return {"api_key": key}


def _parse_captions(content):
    captions = []
    for line in content.split("\n"):
        line = line.strip()
        match = re.match(r"^\s*(\d+)[.)]\s*(.+)", line)
        if match:
            caption = match.group(2).strip().strip('"“”')
            if caption and not caption.lower().startswith(("here are", "check out", "some")):
                captions.append(caption)
    return captions


def generate_captions(topic, style, client, language="English", num_captions=5, creativity=0.9):
    """Return (captions, elapsed_seconds). Raises RuntimeError / ValueError on failure."""
    lang_instruction = f"Write in {language}." if language != "English" else ""

    numbered_format = "\n".join(f"{i}. [caption]" for i in range(1, num_captions + 1))
    prompt = f"""Generate exactly {num_captions} Instagram captions about {topic} in {style} style. {lang_instruction}

Rules:
- NO introductions
- Start with 1.
- Each caption: 10-25 words
- Use 1-3 emojis
- Make them unique

Format:
{numbered_format}"""

    headers = {
        "Authorization": f"Bearer {client['api_key']}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Generate ONLY captions. Start directly with number 1. No introductions."},
            {"role": "user", "content": prompt},
        ],
        "temperature": float(creativity),
        "max_tokens": 900,
    }

    start = time.time()
    try:
        response = requests.post(GROQ_URL, headers=headers, json=data, timeout=REQUEST_TIMEOUT)
    except requests.Timeout as e:
        raise RuntimeError("Groq request timed out. Please try again.") from e
    except requests.RequestException as e:
        raise RuntimeError(f"Could not reach Groq: {e}") from e

    elapsed = round(time.time() - start, 2)

    if response.status_code != 200:
        raise RuntimeError(f"Groq API error {response.status_code}: {response.text[:300]}")

    try:
        content = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Unexpected response from Groq: {e}") from e

    captions = _parse_captions(content)
    if not captions:
        raise RuntimeError("The model returned no usable captions. Please try again.")

    return captions[:num_captions], elapsed


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
        "wellness": ["#wellness", "#selfcare", "#healthyliving", "#mindfulness"],
    }

    style_tags = {
        "funny": "#lol", "luxury": "#luxury", "motivational": "#mindset",
        "aesthetic": "#aesthetic", "bold": "#bold", "emotional": "#feelings",
        "savage": "#savage", "relatable": "#relatable", "poetic": "#poetry",
        "witty": "#witty", "inspirational": "#inspire", "vibes": "#vibes",
    }

    tags = hashtag_map.get(topic, ["#instagram", "#viral"])
    style_tag = style_tags.get(style, "#content")
    default = ["#viral", "#instagram", "#trending", "#fyp"]

    all_tags = tags + [style_tag] + default
    return " ".join(list(dict.fromkeys(all_tags))[:12])


# ============================================
# FAVORITES FUNCTIONS (per user session)
# ============================================


def _favs():
    if "favorites" not in st.session_state:
        st.session_state["favorites"] = []
    return st.session_state["favorites"]


def save_favorite_caption(caption, topic, style):
    favs = _favs()
    if any(f["caption"] == caption for f in favs):
        return False
    favs.append({
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "style": style,
        "caption": caption,
    })
    return True


def get_favorites():
    return list(_favs())


def delete_favorite(index):
    favs = _favs()
    if 0 <= index < len(favs):
        del favs[index]
        return True
    return False


def clear_all_favorites():
    _favs().clear()
    return True
