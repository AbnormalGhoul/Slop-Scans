import requests
import os
from pathlib import Path
from dotenv import load_dotenv


def save_image_from_url(url, file_name):
    try: 
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
    
        tmp_dir = Path("backend/data")
        tmp_dir.mkdir(parents=True, exist_ok=True)

        with open(tmp_dir / file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
            print(f"Image saved successfully from {url}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {url}: {e}")
            

def delete_image(file_name):
    try:
        os.remove(Path("backend/data") / file_name)
        print(f"Image {file_name} deleted successfully")
    except OSError as e:
        print(f"Error deleting image {file_name}: {e}")


def get_metadata_from_images(file_name):
    load_dotenv()
    EXIFTOOL_KEY = os.getenv("EXIFTOOL_API_KEY")
    if not EXIFTOOL_KEY:
        print("Error: EXIFTOOL_API_KEY not found in environment variables")
        return
    
    path = Path("backend/data/images") / file_name
    if not path.is_file():
        print(f"Error: Image file '{file_name}' not found in 'backend/data'")
        return

    with open(path, "rb") as f:
        response = requests.post(
            "https://exiftools.com/api/v1/extract",
            headers={"X-API-Key": EXIFTOOL_KEY},
            files={"file": f}
        )

        result = response.json()

        if not result.get("success"):
            print(f"Error: {result.get('error')}")
            return
        
        metadata = result.get("metadata", {})

        print(f"\n{'='*60}")
        print(f"Image: {file_name}")
        print(f"{'='*60}")

        for section, values in metadata.items():
            if isinstance(values, dict):
                print(f"\n--- {section} ---")
                for key, value in values.items():
                    print(f"{key:40}: {value}")
            else:
                print(f"{section:40}: {values}")

        return metadata


def main():
    image_urls = []
    try:    
        with open('backend/data/scraped_image_url.txt', 'r') as file:
            image_urls = file.read().splitlines()
    except FileNotFoundError:
        print("Error: 'scraped_image_urls.txt' not found")

    if image_urls:
        for url in image_urls:
            file_name = url.split("/")[-1].split("?")[0]
            save_image_from_url(url, file_name)

            file_path = Path("backend/data") / file_name
            if file_path.suffix.lower() == ".svg":
                print(f"Skipping SVG (PIL does not support SVG): {file_name}")
                delete_image(file_name)
            else:
                get_metadata_from_images(file_name)
                delete_image(file_name)

    p = Path('backend/data/images')
    files = [entry.name for entry in p.iterdir() if entry.is_file()]
    if files:
        for file in files:
            file_name = file
            file_path = Path("backend/data/images") / file_name
            if file_path.suffix.lower() == ".svg":
                print(f"Skipping SVG (PIL does not support SVG): {file_name}")
            else:
                # read_png_chunks(file_name)
                get_metadata_from_images(file_name)


if __name__ == "__main__":
    main()

