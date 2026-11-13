import pandas as pd
import requests
import time

from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Original dataset
df = pd.read_csv("data/all_books_dataset.csv")

# Website
BASE_URL = "https://books.toscrape.com/"

# Store image URLs using book titles
image_data = {}

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("Starting book cover collection...")

# Visit all 50 catalogue pages
for page in range(1, 51):

    page_url = f"{BASE_URL}catalogue/page-{page}.html"

    try:
        response = requests.get(
            page_url,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        books = soup.select("article.product_pod")

        for book in books:

            image = book.select_one("img.thumbnail")

            if image:

                title = image.get("alt", "").strip()

                image_path = image.get("src", "")

                image_url = urljoin(
                    page_url,
                    image_path
                )

                image_data[title] = image_url

        print(f"Page {page}: {len(books)} books collected")

        time.sleep(0.4)

    except requests.RequestException as error:

        print(f"Error on page {page}: {error}")

# Match images with original dataset
df["Image_URL"] = df["Title"].map(image_data)

# Save as a NEW file
output_file = "data/all_books_with_images.csv"

df.to_csv(output_file, index=False)

print("\nCollection completed!")
print("Total books:", len(df))
print("Images found:", df["Image_URL"].notna().sum())
print("Images missing:", df["Image_URL"].isna().sum())
print("Saved to:", output_file)