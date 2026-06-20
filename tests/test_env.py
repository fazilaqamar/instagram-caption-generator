import os
from groq import Groq

# Set API key from environment
api_key = os.environ.get("GROQ_API_KEY", "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")

try:
    # Initialize with environment variable
    client = Groq(api_key=api_key)
    print("✅ Client created successfully!")
    
    # Test API call
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": "Say 'Hello World'"}
        ],
        max_tokens=10
    )
    print(f"✅ API Response: {response.choices[0].message.content}")
    print("🎉 Everything is working!")
    
except Exception as e:
    print(f"❌ Error: {e}")