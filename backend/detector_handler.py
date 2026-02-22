from scrapper.scrape_request import *
from scrapper.img_metadata import *
from scrapper.text_cleanup import *

from services.text_detector import text_detector
from services.image_detector import image_detector
from config import settings

import glob


def run_detector(url: str)->float:
    print(f"Running detection for URL: {url}")
    
    # Step 1: Scrape the page
    html_content = scrape_url(url)
    text_content = extract_text_from_html(html_content)
    with open("data/scraped_text.txt", "w", encoding="utf-8") as file:
        file.write(text_content)
    image_urls = extract_image_urls_from_html(html_content)
    with open("data/scraped_image_urls.txt", "w", encoding="utf-8") as file:
        for url in image_urls:
            file.write(url + "\n")
    
        print("\nRunning local detection tests...\n")

    # Step 2: Run detection models
    text_path = "data/transcription.txt"
    
    remove_double_quotes_from_file(text_path)  # Clean up text file before test

    if os.path.exists(text_path):
        with open(text_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        text_result = text_detector.predict(text_content)

        print("TEXT RESULT:")
        print(text_result)
        print()
    else:
        text_result = {"ai_probability": 0.0}  # No text found, set AI probability to 0
        print(f"Text file not found at {text_path}")

    # Image Test
    image_extensions = ["png", "jpg", "jpeg", "webp"]
    image_files = []

    for ext in image_extensions:
        image_files.extend(glob.glob(f"data/*.{ext}"))

    if image_files:
        image_path = image_files[0]  # take first match
        print(f"Using image: {image_path}")

        with open(image_path, "rb") as f:
            image_bytes = f.read()

        image_result = image_detector.predict_from_bytes(image_bytes)

        print("IMAGE RESULT:")
        print(image_result)
        print()
        
        delete_image(image_path)  # Clean up after test
    else: 
        image_result = {"ai_probability": 0.0}  # No image found, set AI probability to 0
    print("Detection completed.")

    return max(text_result['ai_probability'], image_result['ai_probability'])


if __name__ == "__main__":
    input_url = input("Enter the URL to analyze: ")
    if input_url:
        score = run_detector(input_url)
        print(f"Final AI Detection Score: {score:.2f}")
    else:
        print("No URL provided. Exiting.")