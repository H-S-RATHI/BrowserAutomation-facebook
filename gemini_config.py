"""
Gemini API Configuration

1. Get your API key from: https://aistudio.google.com/app/apikey
2. Replace 'YOUR_API_KEY' with your actual API key
3. Save the file
"""

# Gemini API Configuration
GEMINI_API_KEY = 'AIzaSyByhHWNhRJJar25MgTmNNUxeOcSltAm9Q8'  # Replace with your actual API key

# Model configuration
GEMINI_MODEL = 'gemini-2.0-flash'  # or 'gemini-1.5-flash' for faster responses

# Default generation parameters
GENERATION_CONFIG = {
    'temperature': 0.7,
    'top_p': 0.9,
    'top_k': 40,
    'max_output_tokens': 2048,
}

# System prompt for enhancing descriptions
ENHANCE_PROMPT = """
Rewrite this social media post to sound completely natural and human-written. 
Make it engaging and conversational, just like a real person would write. 
Keep it casual, use natural language, and avoid any AI-sounding phrases. 
Maintain the original meaning but make it sound authentic and spontaneous. 
Add a few relevant emojis if appropriate, but don't overdo it. 
Keep it concise (1-2 short paragraphs max).

Original post:
"""
