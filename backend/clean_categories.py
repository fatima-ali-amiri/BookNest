import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output files
INPUT_FILE = BASE_DIR / "data" / "all_books_categorized.csv"

OUTPUT_FILE = BASE_DIR / "data" / "all_books_cleaned.csv"


# Convert original category names into cleaner display names
CATEGORY_MAPPING = {

    "Default": "Other / Miscellaneous",

    "Add a comment": "Other / Miscellaneous",

    "Sequential Art": "Comics & Graphic Novels",

    "Sports and Games": "Sports & Games",

    "Self Help": "Motivation & Self-Development",

    "Business": "Business & Economics",

    "Autobiography": "Biography & Memoir",

    "Biography": "Biography & Memoir",

    "Childrens": "Children's Books",

    "Womens Fiction": "Women's Fiction",

    "Science Fiction": "Science Fiction",

    "Historical Fiction": "Historical Fiction",

    "Young Adult": "Young Adult",

    "Nonfiction": "Nonfiction",

    "Fiction": "Fiction & Literature",

    "Novels": "Fiction & Literature",

    "Adult Fiction": "Fiction & Literature",

    "Christian Fiction": "Fiction & Literature",

    "Poetry": "Poetry",

    "Science": "Science & Nature",

    "History": "History",

    "Food and Drink": "Food & Drink",

    "Travel": "Travel",

    "Mystery": "Mystery",

    "Romance": "Romance",

    "Fantasy": "Fantasy",

    "Thriller": "Thriller",

    "Horror": "Horror",

    "Philosophy": "Philosophy",

    "Psychology": "Psychology",

    "Religion": "Religion",

    "Spirituality": "Spirituality",

    "Music": "Music",

    "Art": "Art",

    "Humor": "Humor",

    "Health": "Health",

    "Politics": "Politics",

    "Crime": "Crime",

    "Cultural": "Culture",

    "Contemporary": "Contemporary",

    "New Adult": "New Adult",

    "Christian": "Religion & Spirituality",

    "Historical": "Historical Fiction",

    "Short Stories": "Short Stories",

    "Suspense": "Suspense",

    "Academic": "Academic",

    "Paranormal": "Paranormal",

    "Parenting": "Parenting",

    "Erotica": "Other / Miscellaneous"
}


def main():

    print("Loading categorized books...")

    df = pd.read_csv(INPUT_FILE)

    print("Total books:", len(df))

    # Preserve the original collected categories
    df["Source_Category"] = df["Category"].fillna(
        "Unknown"
    ).astype(str).str.strip()

    # Create clean category names
    df["Category"] = df["Source_Category"].map(
        CATEGORY_MAPPING
    ).fillna(df["Source_Category"])

    # Save cleaned dataset separately
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nCategory cleaning completed!")

    print("\nClean category summary:")

    print(
        df["Category"]
        .value_counts()
        .to_string()
    )

    print("\nTotal books:", len(df))

    print(
        "Unique clean categories:",
        df["Category"].nunique()
    )

    print(
        "Books with original categories:",
        df["Source_Category"].notna().sum()
    )

    print("\nSaved file:", OUTPUT_FILE)


if __name__ == "__main__":
    main()