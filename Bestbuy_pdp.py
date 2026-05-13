import os
from pathlib import Path

from curl_cffi import requests

# url = "https://www.bestbuy.com/product/dell-15-6-2k-touchscreen-laptop-intel-core-i5-1334u-2023-8gb-memory-512-gb-storage-carbon-black/J3K4L6QW5Y/sku/6668953"
output_file = Path(__file__).with_name("Bestbuy_PDP.html")

proxy_url = os.getenv("PROXY_URL")
proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None

def fetch_bestbuy_response(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    last_error = None
    response = None
    for method in ("get", "post"):
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                proxies=proxies,
                impersonate="chrome124",
                timeout=60,
            )
            response.raise_for_status()
            break
        except Exception as exc:
            last_error = exc

    if response is None:
        raise RuntimeError(f"Failed to fetch URL with GET/POST attempts: {last_error}")

    print("Status:", response.status_code)
    print("Final URL:", response.url)
    print("Content-Type:", response.headers.get("content-type"))
    print("Response length:", len(response.text))

    output_file.write_text(response.text, encoding="utf-8")
    print("Saved HTML to:", output_file)
    return response.text
