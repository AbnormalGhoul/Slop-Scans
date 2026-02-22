import requests

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}


def scrape_url(url: str) -> str:
    try:
        session = requests.Session()
        response = session.get(url, headers=DEFAULT_HEADERS, timeout=15, allow_redirects=True)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        if isinstance(e, requests.HTTPError) and e.response is not None:
            print(f"Status code: {e.response.status_code}")
            if e.response.status_code == 403:
                print("403 often means the site blocks non-browser requests.")
        return ""
    

if __name__ == "__main__":
    url = input("Enter the URL to scrape: ")
    html_content = scrape_url(url)
    with open("scraped_content.html", "w", encoding="utf-8") as file:
        file.write(html_content)