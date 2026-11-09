
def make_hashtags(topic, style):
    """Create relevant hashtags for the selected topic and style."""

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
        "funny": "#lol",
        "luxury": "#luxury",
        "motivational": "#mindset",
        "aesthetic": "#aesthetic",
        "bold": "#bold",
        "emotional": "#feelings",
        "savage": "#savage",
        "relatable": "#relatable",
        "poetic": "#poetry",
        "witty": "#witty",
        "inspirational": "#inspire",
        "vibes": "#vibes",
    }

    default_tags = [
        "#viral", "#instagram", "#trending",
        "#contentcreator", "#fyp"
    ]

    topic_tags = hashtag_map.get(topic, ["#instagram", "#viral"])
    style_tag = style_tags.get(style, "#content")

    all_tags = topic_tags + [style_tag] + default_tags
    unique_tags = list(dict.fromkeys(all_tags))

    return " ".join(unique_tags[:15])


# ============================================
# FAVORITES
# ============================================

def _favorites_file():
    """Return the favorites JSON path and ensure its directory exists."""
    os.makedirs("data", exist_ok=True)
    return os.path.join("data", "favorites.json")


def get_favorites():
    """Load saved favorite captions."""
    path = _favorites_file()

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def save_favorite_caption(caption, topic, style):
    """Save one caption to data/favorites.json."""
    try:
        favorites = get_favorites()
        favorites.append({
            "timestamp": datetime.now().isoformat(timespec="minutes"),
            "topic": topic,
            "style": style,
            "caption": caption,
        })

        with open(_favorites_file(), "w", encoding="utf-8") as file:
            json.dump(favorites, file, indent=2, ensure_ascii=False)

        return True

    except (OSError, TypeError, ValueError):
        return False


def delete_favorite(index):
    """Delete a favorite using its zero-based index."""
    try:
        favorites = get_favorites()

        if not 0 <= index < len(favorites):
            return False

        del favorites[index]

        with open(_favorites_file(), "w", encoding="utf-8") as file:
            json.dump(favorites, file, indent=2, ensure_ascii=False)

        return True

    except (OSError, TypeError, ValueError):
        return False


def clear_all_favorites():
    """Delete all saved favorites."""
    try:
        with open(_favorites_file(), "w", encoding="utf-8") as file:
            json.dump([], file, indent=2)

        return True

    except OSError:
        return False
