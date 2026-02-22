from PIL import Image
from PIL.ExifTags import TAGS
import requests
import sys
import os
from pathlib import Path


def save_image_from_url(url, file_name):
    try: 
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
    
        tmp_dir = Path("scrapper/tmp")
        tmp_dir.mkdir(parents=True, exist_ok=True)

        with open(tmp_dir / file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
            print(f"Image saved successfully from {url}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {url}: {e}")
            

def delete_image(file_name):
    try:
        os.remove(Path("scrapper/tmp") / file_name)
        print(f"Image {file_name} deleted successfully")
    except OSError as e:
        print(f"Error deleting image {file_name}: {e}")


def get_metadata_from_images(file_name):
        try:
            image = Image.open(f"scrapper/tmp/{file_name}")
            image.verify()
            
            # Check if image is truly opened
            if image.fp is None:
                print(f"Error: Image file path is none")
            
            if image.close:
                print(f"Error: Image file is closed")
            
            # Verify image has valid format
            if not image.format:
                print(f"Error: Image has invalid format: {file_name}")
            
            print(f"\n{'='*60}")
            print(f"Image: {file_name}")
            print(f"{'='*60}")
            
            exif_data = image.getexif()
            if exif_data:
                print(f"\n--- EXIF Data ({len(exif_data)} tags) ---")
                for tagid in exif_data:
                    tagname = TAGS.get(tagid, tagid)
                    value = exif_data.get(tagid)
                    
                    if isinstance(value, bytes):
                        value = value.decode()
                    print(f"{tagname:25}: {value}")
            else:
                print("\n--- EXIF Data ---")
                print("No EXIF data found")
            
            image.close()
                
        except Image.UnidentifiedImageError:
            print(f"Unidentified image file: {file_name}")
        except AssertionError:
            print(f"Error: Image file corrupted or cannot be read: {file_name}")            

def main():
    image_urls = []
    try:    
        with open('scraped_image_url.txt', 'r') as file:
            image_urls = file.read().splitlines()
    except FileNotFoundError:
        print("Error: 'scraped_image_urls.txt' not found")

    if image_urls:
        for url in image_urls:
            file_name = url.split("/")[-1].split("?")[0]
            save_image_from_url(url, file_name)

            file_path = Path("scrapper/tmp") / file_name
            if file_path.suffix.lower() == ".svg":
                print(f"Skipping SVG (PIL does not support SVG): {file_name}")
                delete_image(file_name)
            else:
                get_metadata_from_images(file_name)
                delete_image(file_name)

    p = Path('scrapper/tmp')
    files = [entry.name for entry in p.iterdir() if entry.is_file()]
    if files:
        for file in files:
            file_name = file
            file_path = Path("scrapper/tmp") / file_name
            if file_path.suffix.lower() == ".svg":
                print(f"Skipping SVG (PIL does not support SVG): {file_name}")
            else:
                get_metadata_from_images(file_name)


if __name__ == "__main__":
    main()
