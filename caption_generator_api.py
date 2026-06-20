def generate_captions(topic, style, client, language="English", num_captions=5, creativity=0.9):
    """Generate captions using Groq API"""
    
    lang_instruction = f"Write in {language}." if language != "English" else ""
    
    prompt = f"""You are a professional social media copywriter.

Generate exactly {num_captions} Instagram captions about {topic} in {style} style. {lang_instruction}

CRITICAL RULES:
- NO INTRODUCTORY LINES
- START DIRECTLY with caption 1
- Each caption: 10-25 words
- Use 1-3 emojis naturally
- Make them unique and engaging
- NO repetitive phrases
- NO hashtags in captions

Format EXACTLY like this:
1. [Your first caption]
2. [Your second caption]
3. [Your third caption]
4. [Your fourth caption]
5. [Your fifth caption]

Now generate {num_captions} {style} captions about {topic}:
"""
    # ... rest of the code
