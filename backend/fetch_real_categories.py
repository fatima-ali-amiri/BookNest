import pandas as pd
import requests
import time

from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "all_books_with_images.csv"
OUTPUT_FILE = BASE_DIR / "data" / "all_books_categorized.csv"

BASE_URL = "https://books.toscrape.com/"

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0"
})


def get_soup(url):

    response = session.get(url, timeout=20)
    response.raise_for_status()

    return BeautifulSoup(response.text, "html.parser")


def main():

    df = pd.read_csv(INPUT_FILE)

    category_data = {}

    print("Starting real category collection...")
    print("Total books:", len(df))

    for page in range(1, 51):

        catalogue_url = urljoin(
            BASE_URL,
            f"catalogue/page-{page}.html"
        )

        try:
            soup = get_soup(catalogue_url)

            articles = soup.select("article.product_pod")

            for article in articles:

                image = article.select_one("img.thumbnail")
                link = article.select_one("h3 a")

                if not image or not link:
                    continue

                title = image.get("alt", "").strip()

                product_url = urljoin(
                    catalogue_url,
                    link.get("href", "")
                )

                try:

                    product_soup = get_soup(product_url)

                    breadcrumbs = product_soup.select(
                        "ul.breadcrumb li a"
                    )

                    if len(breadcrumbs) >= 3:

                        category = breadcrumbs[-1].get_text(
                            strip=True
                        )

                    else:
                        category = "Unknown"

                    category_data[title] = category

                except requests.RequestException as error:

                    print("Book error:", title, error)
                    category_data[title] = "Unknown"

                time.sleep(0.25)

            print(
                f"Catalogue page {page}/50 completed"
            )

        except requests.RequestException as error:

            print(
                f"Catalogue page {page} error:",
                error
            )

    # Match real categories with our dataset
    df["Category"] = (
        df["Title"]
        .map(category_data)
        .fillna("Unknown")
    )

    # Save a new dataset
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nCategory collection completed!")

    print("\nReal category summary:")

    print(df["Category"].value_counts().to_string())

    print("\nTotal books:", len(df))

    print(
        "Books with categories:",
        (df["Category"] != "Unknown").sum()
    )

    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()