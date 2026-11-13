import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset paths
INPUT_FILE = BASE_DIR / "data" / "all_books_with_images.csv"
OUTPUT_FILE = BASE_DIR / "data" / "all_books_categorized.csv"


# Define category keywords
CATEGORY_KEYWORDS = {
    "Comics & Graphic Novels": [
        "comic", "comics", "graphic novel", "manga"
    ],

    "Gaming": [
        "gaming", "video game", "game design", "gamer"
    ],

    "Technology & Coding": [
        "python", "programming", "coding", "software",
        "computer", "technology", "javascript", "database"
    ],

    "Motivation & Self-Development": [
        "motivation", "self-help", "self help",
        "personal development", "success", "inspiration",
        "dream job", "confidence", "leadership"
    ],

    "History & Biography": [
        "history", "historical", "biography", "memoir",
        "autobiography", "life of", "war"
    ],

    "Science & Nature": [
        "science", "physics", "chemistry", "biology",
        "nature", "universe", "astronomy", "animal"
    ],

    "Business & Economics": [
        "business", "economics", "finance", "marketing",
        "entrepreneur", "investment", "management"
    ],

    "Poetry": [
        "poetry", "poems", "sonnets", "poet"
    ],

    "Fiction & Literature": [
        "novel", "fiction", "shakespeare", "literature",
        "romance", "mystery", "thriller"
    ]
}


# Classify a book using its title
def classify_book(title):

    title = str(title).lower()

    for category, keywords in CATEGORY_KEYWORDS.items():

        for keyword in keywords:

            if keyword in title:
                return category

    return "Other / Unclassified"


# Main function
def main():

    print("Loading BookNest dataset...")

    df = pd.read_csv(INPUT_FILE)

    print("Total books:", len(df))

    # Create a new Category column
    df["Category"] = df["Title"].apply(classify_book)

    # Save a new dataset
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nCategory classification completed!")

    print("\nCategory summary:")

    print(
        df["Category"]
        .value_counts()
        .to_string()
    )

    print("\nTotal books:", len(df))

    print("Saved dataset:", OUTPUT_FILE)


if __name__ == "__main__":
    main()