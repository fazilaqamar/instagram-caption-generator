"""Backend for the AI Caption Generator (Streamlit + Groq)."""

import json
import os
import re
import time
from datetime import datetime

import requests
import streamlit as st

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"
REQUEST_TIMEOUT = 30

VALID_TOPICS = [
    "travel", "food", "fitness", "fashion", "nature", "lifestyle",
    "business", "technology", "music", "art", "friends", "family",
    "love", "motivation", "pets", "photography",
]

VALID_STYLES = [
    "funny", "inspirational", "aesthetic", "romantic", "witty", "casual",
    "professional", "poetic", "sassy", "minimal", "bold", "wholesome",
]


# ---------------------------------------------------------------
# API key / client
# ---------------------------------------------------------------
def get_groq_api_key():
    """Read the key from Streamlit Secrets, falling back to an env var."""
    try:
        key = st.secrets.get("GROQ_API_KEY")
        if key:
            return key
    except Exception:
        pass
    return os.environ.get("GROQ_API_KEY")


def get_client(api_key=None):
    key = api_key or get_groq_api_key()
    if not key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it in Manage app > Settings > Secrets."
        )
    return {"api_key": key}


# ---------------------------------------------------------------
# Caption generation
# ---------------------------------------------------------------
def _clean_caption(text):
    text = text.strip()
    text = re.sub(r"^\s*(?:\d+[\.\)]|[-*•])\s*", "", text)  # "1. " / "- "
    return text.strip().strip('"“”').strip()


def _extract_captions(content, num_captions):
    """Try JSON first, then fall back to line-by-line parsing."""
    captions = []

    match = re.search(r"\[.*\]", content, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(0))
            if isinstance(data, list):
                captions = [_clean_caption(str(c)) for c in data]
        except json.JSONDecodeError:
            pass

    if not captions:
        for line in content.splitlines():
            line = _clean_caption(line)
            if len(line) > 8 and not line.lower().startswith(("here are", "sure")):
                captions.append(line)

    captions = [c for c in captions if c]
    return captions[:num_captions]


def generate_captions(topic, style, client, language="English",
                      num_captions=5, creativity=0.9):
    """Return (captions, elapsed_seconds). Raises RuntimeError on failure."""
    prompt = (
        f"Write {num_captions} Instagram captions about '{topic}' in a "
        f"'{style}' style, in {language}. Keep each under 150 characters and "
        f"include fitting emojis. Do not include hashtags. "
        f"Reply ONLY with a JSON array of {num_captions} strings."
    )

    headers = {
        "Authorization": f"Bearer {client['api_key']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a creative social media copywriter."},
            {"role": "user", "content": prompt},
        ],
        "temperature": float(creativity),
        "max_tokens": 1024,
    }

    start = time.time()
    try:
        response = requests.post(
            GROQ_URL, headers=headers, json=payload, timeout=REQUEST_TIMEOUT
        )
        if response.status_code != 200:
            raise RuntimeError(f"HTTP {response.status_code}: {response.text[:300]}")
        content = response.json()["choices"][0]["message"]["content"]
    except requests.Timeout as e:
        raise RuntimeError("Groq request timed out. Try again.") from e
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"Groq API failed: {e}") from e

    captions = _extract_captions(content, num_captions)
    if not captions:
        raise RuntimeError("The model returned no usable captions. Try again.")

    return captions, round(time.time() - start, 2)


# ---------------------------------------------------------------
# Hashtags
# ---------------------------------------------------------------
_STYLE_TAGS = {
    "funny": ["#funny", "#humor", "#lol"],
    "inspirational": ["#inspiration", "#mindset", "#positivevibes"],
    "aesthetic": ["#aesthetic", "#vibes", "#moodboard"],
    "romantic": ["#romantic", "#lovestory", "#couplegoals"],
    "witty": ["#witty", "#clever", "#wordplay"],
    "casual": ["#casual", "#everyday", "#chill"],
    "professional": ["#professional", "#career", "#growth"],
    "poetic": ["#poetry", "#words", "#writersofinstagram"],
    "sassy": ["#sassy", "#attitude", "#unapologetic"],
    "minimal": ["#minimal", "#simple", "#lessismore"],
    "bold": ["#bold", "#confidence", "#fearless"],
    "wholesome": ["#wholesome", "#kindness", "#goodvibes"],
}

_GENERIC_TAGS = ["#instagood", "#instadaily", "#photooftheday", "#explore", "#trending"]


def make_hashtags(topic, style):
    topic_clean = re.sub(r"[^a-z0-9]", "", topic.lower())
    tags = [
        f"#{topic_clean}", f"#{topic_clean}lover", f"#{topic_clean}life",
        f"#{topic_clean}gram",
    ]
    tags += _STYLE_TAGS.get(style.lower(), [f"#{style.lower()}"])
    tags += _GENERIC_TAGS
    return " ".join(dict.fromkeys(tags))


# ---------------------------------------------------------------
# Favorites (stored per user session)
# ---------------------------------------------------------------
def _fav_list():
    if "favorites" not in st.session_state:
        st.session_state["favorites"] = []
    return st.session_state["favorites"]


def save_favorite_caption(caption, topic, style):
    favs = _fav_list()
    if any(f["caption"] == caption for f in favs):
        return False
    favs.append({
        "caption": caption,
        "topic": topic,
        "style": style,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    return True


def get_favorites():
    return list(_fav_list())


def delete_favorite(index):
    favs = _fav_list()
    if 0 <= index < len(favs):
        favs.pop(index)
        return True
    return False


def clear_all_favorites():
    _fav_list().clear()
    return True
