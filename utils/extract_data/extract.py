import time
import logging
import requests
import datetime
from typing import List, Dict
from bs4 import BeautifulSoup


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    )
}

BASE_URL = "https://fashion-studio.dicoding.dev/"
MAX_PAGES_LIMIT = 50

def scrape_page(url: str) -> List[Dict[str, str]]:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Fetching failure {url}: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for product in soup.find_all("div", class_="collection-card"):
        try:
            title = product.find("h3", class_="product-title")
            title = title.text.strip() if title else "Unknown Product"

            price = product.find("span", class_="price")
            price = price.text.strip().replace("$", "") if price else "N/A"

            rating_elem = product.find("p", string=lambda text: text and "Rating" in text)
            rating = rating_elem.text.replace("Rating:", "").replace("⭐", "").strip() if rating_elem else "Invalid"

            colors_elem = product.find("p", string=lambda text: text and "Colors" in text)
            colors = colors_elem.text.replace("Colors:", "").strip().split()[0] if colors_elem else "N/A"

            size_elem = product.find("p", string=lambda text: text and "Size" in text)
            size = size_elem.text.replace("Size:", "").strip() if size_elem else "N/A"

            gender_elem = product.find("p", string=lambda text: text and "Gender" in text)
            gender = gender_elem.text.replace("Gender:", "").strip() if gender_elem else "N/A"

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            products.append({
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Colors": colors,
                "Size": size,
                "Gender": gender,
                "Timestamp": timestamp
            })
        except Exception as e:
            logging.warning(f"Failed to extract the product: {e}")

    return products

def generate_urls(max_pages: int = MAX_PAGES_LIMIT) -> List[str]:
    urls = [BASE_URL]
    urls.extend([f"{BASE_URL}page{page}" for page in range(2, max_pages + 1)])
    return urls

def scrape_main(max_pages: int = MAX_PAGES_LIMIT) -> List[Dict[str, str]]:
    start_time = time.time()
    urls = generate_urls(max_pages)
    all_products = []

    for url in urls:
        logging.info(f"Scraping URL: {url}")
        page_products = scrape_page(url)
        if page_products:
            all_products.extend(page_products)
            logging.info(f"Successful scraping {len(page_products)} product data from {url}")
        time.sleep(1)

    execution_time = time.time() - start_time
    print(f"\nTotal scraping time: {execution_time:.2f} seconds")
    print(f"Total data scraping: {len(all_products)}\n")
    return all_products