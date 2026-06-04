# ============================================================
#  caption_generator_api.py  —  Claude API backend
#  Used by both: streamlit_app.py  AND  CLI runner
# ============================================================

# pip install anthropic
# export ANTHROPIC_API_KEY=sk-ant-...

import anthropic, re, time, os

VALID_TOPICS = ["cars","travel","fashion","fitness","food","nature","tech","beauty"]
VALID_STYLES = ["funny","luxury","motivational","aesthetic","bold","emotional"]

HASHTAG_BANK = {
    "cars":    ["#carsofinstagram","#dreamcar","#luxurycars","#automotive","#carlover"],
    "travel":  ["#travelgram","#wanderlust","#exploremore","#vacationmode","#travelphotography"],
    "fashion": ["#fashionstyle","#ootd","#outfitcheck","#styleinspo","#fashionista"],
    "fitness": ["#fitcheck","#gymrat","#gains","#workout","#fitnessmotivation"],
    "food":    ["#foodie","#instafood","#eatingfortheinsta","#foodporn","#nomnomnom"],
    "nature":  ["#earthpix","#naturephotography","#outdoors","#optoutside","#natgeo"],
    "tech":    ["#techbro","#gadgets","#innovation","#techlife","#futureishere"],
    "beauty":  ["#glowup","#skincare","#makeuptok","#beautytips","#selfcare"],
}
STYLE_TAGS = {
    "funny":"#lol","luxury":"#luxury","motivational":"#mindset",
    "aesthetic":"#aesthetic","bold":"#bold","emotional":"#feelings",
}
STYLE_GUIDE = {
    "funny":        "GenZ humor — POV format, self-aware, relatable fails, dry wit. Like: 'POV: washed the car, it rained.' or 'My car has more issues than me.'",
    "luxury":       "Minimal, confident, aspirational. Short power statements. Like: 'Not for everyone. That\\'s the point.' or 'Silence is the loudest flex.'",
    "motivational": "Punchy, action-oriented, no fluff. Like: 'Start before you\\'re ready.' or 'No excuses. Just miles.'",
    "aesthetic":    "Dreamy, sensory, poetic but short. Like: 'Windows down, mind clear.' or 'Chasing golden hour forever.'",
    "bold":         "Unapologetic, statement-making, zero softness. Like: 'We don\\'t follow trends. We set them.' or 'Boring is a choice. Not ours.'",
    "emotional":    "Honest, vulnerable, hits in the feels. Like: 'Some moments you just want to freeze.' or 'Not every ride is just a ride.'",
}
EMOJI_OK = {"funny","aesthetic","emotional"}


def get_client(api_key: str = None):
    key = api_key or os.environ.get("ANTHROPIC_API_KEY","")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY not set")
    return anthropic.Anthropic(api_key=key)


def generate_captions(topic: str, style: str, client) -> tuple[list[str], float]:
    style_desc  = STYLE_GUIDE.get(style, "")
    emoji_rule  = "Emojis okay (max 1 per caption)." if style in EMOJI_OK else "No emojis."

    system = (
        "You are an expert GenZ Instagram caption writer. "
        "You write viral, punchy, human captions people actually save and share. "
        "Respond with ONLY a numbered list — no intro, no explanation, nothing else."
    )
    user = (
        f"Write EXACTLY 5 Instagram captions.\n\n"
        f"Topic: {topic}\nStyle: {style}\n\n"
        f"Style guide: {style_desc}\n\n"
        f"Rules:\n"
        f"- 4 to 8 words per caption\n"
        f"- Complete thought, never cut off\n"
        f"- No hashtags\n"
        f"- {emoji_rule}\n"
        f"- No photo suggestions, no explanations\n"
        f"- Numbered list ONLY\n\n"
        f"1.\n2.\n3.\n4.\n5."
    )

    start = time.perf_counter()
    msg   = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        system=system,
        messages=[{"role":"user","content":user}],
    )
    elapsed = round(time.perf_counter() - start, 2)

    raw      = msg.content[0].text
    captions = _clean(raw, style)
    return captions, elapsed


def _clean(text: str, style: str) -> list[str]:
    intro_re = re.compile(
        r"^(sure|here|of course|absolutely|below|great|these are|"
        r"here are|here's|i've|i have|following|let me|as requested)",
        re.IGNORECASE,
    )
    captions = []
    for line in text.strip().split("\n"):
        line  = line.strip()
        match = re.match(r"^\*{0,2}\s*\d+[.)]\s*\*{0,2}\s*(.+)", line)
        if not match:
            continue
        cap = match.group(1).strip("*\"' ")
        if intro_re.match(cap):
            continue
        cap = re.sub(r"#\w+", "", cap)
        cap = re.sub(r"\*+\w*", "", cap)
        for m in ['" *','." ',"(Note","Note:","*Your","Accompanied"]:
            if m in cap:
                cap = cap.split(m)[0]
        cap = cap.rstrip("–—…\"'").strip()
        mid = {","," and"," but"," or"," the"," a"," an"}
        if not cap or len(cap.split()) < 3:
            continue
        if any(cap.lower().endswith(e) for e in mid):
            continue
        captions.append(cap)
    return captions[:5]


def make_hashtags(topic: str, style: str) -> str:
    tags      = HASHTAG_BANK.get(topic.lower().strip(), [])
    default   = ["#viral","#instagram","#trending","#contentcreator","#fyp"]
    style_tag = STYLE_TAGS.get(style, "#" + style.lower())
    return " ".join(tags + default + [style_tag])
