"""
Utility functions for interacting with Google's Gemini API
"""
import google.generativeai as genai
from gemini_config import GEMINI_API_KEY, GEMINI_MODEL, GENERATION_CONFIG, ENHANCE_PROMPT
import os
from typing import Optional

def setup_gemini():
    """Initialize the Gemini API with the API key"""
    if not GEMINI_API_KEY or GEMINI_API_KEY == 'YOUR_API_KEY':
        raise ValueError(
            "Please set up your Gemini API key in gemini_config.py. "
            "Get one from: https://aistudio.google.com/app/apikey"
        )
    
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(GEMINI_MODEL)

def enhance_description(description: str) -> Optional[str]:
    """
    Enhance a post description using Gemini
    
    Args:
        description: The original description to enhance
        
    Returns:
        Enhanced description or None if there was an error
    """
    if not description.strip():
        return ""
    
    try:
        model = setup_gemini()
        
        # Create the full prompt
        full_prompt = f"{ENHANCE_PROMPT}\"" + description + "\""
        
        # Generate the response
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(**GENERATION_CONFIG)
        )
        
        # Extract and return the enhanced text
        enhanced_text = response.text.strip()
        
        # Remove any markdown code blocks if present
        if enhanced_text.startswith('```') and enhanced_text.endswith('```'):
            enhanced_text = enhanced_text[3:-3].strip()
        
        return enhanced_text
        
    except Exception as e:
        print(f"Error enhancing description: {str(e)}")
        return None

def test_enhancement():
    """Test the enhancement function with a sample description"""
    test_desc = """
    Check out our new product! It's really cool and has lots of features.
    Buy now and get 10% off!
    """
    
    print("Original:")
    print(test_desc)
    print("\nEnhanced:")
    enhanced = enhance_description(test_desc)
    print(enhanced)

if __name__ == "__main__":
    test_enhancement()
