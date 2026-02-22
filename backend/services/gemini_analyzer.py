from google import genai
from config import settings
import json
import re

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def find_top_ai_phrases(ai_percentage: float, text: str):
    prompt = f"""You are a text analysis expert. Analyze the following text and identify the top 3 most AI-generated sounding phrases.

IMPORTANT: Return ONLY a valid JSON array with exactly 3 phrases. No other text, no explanations, no markdown markers.

Example format:
["phrase one here", "phrase two here", "phrase three here"]

AI Detection Score: {ai_percentage*100:.2f}%

TEXT TO ANALYZE:
{text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    raw_text = response.text.strip()

    print("\nGemini Raw Response:")
    print(raw_text)

    # Try to extract JSON

    try:
        # First try direct parsing
        phrases = json.loads(raw_text)
    except json.JSONDecodeError:
        print("Direct JSON parsing failed. Attempting to extract JSON...")
        
        # Try to find JSON array in the response
        json_match = re.search(r'\[.*\]', raw_text, re.DOTALL)
        if json_match:
            try:
                phrases = json.loads(json_match.group())
            except json.JSONDecodeError:
                print("Could not extract valid JSON from response.")
                return None
        else:
            print("No JSON array found in response.")
            return None

    if isinstance(phrases, list) and len(phrases) > 0:
        print("\nTop AI-like Phrases:")
        for i, phrase in enumerate(phrases[:3], 1):
            print(f"{i}. {phrase}")
        return phrases
    
    return None
    
    
if __name__ == "__main__":
    test_text = """
    Artificial intelligence is transforming industries across the globe.
    It leverages advanced machine learning algorithms to optimize workflows.
    I love pizza and going to the beach on sunny days.
    I am a human and I enjoy reading books and spending time with friends.
    I walked my dog in the park yesterday and we had a great time playing fetch.
    Those characteristic long ears aren't just adorable;
    """

    result = find_top_ai_phrases(0.85, test_text)

    print("\nFinal Parsed Result:")
    print(result)