from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import json
from pathlib import Path
try:
    from .recommendation_model import recommendation_model
except ImportError:
    from recommendation_model import recommendation_model

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "all_books_cleaned.csv"
FAVOURITES_FILE = BASE_DIR / "data" / "favourites.json"


# LOAD BOOK DATA

def load_books():

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    required_columns = [
        "Title",
        "Price",
        "Rating",
        "Availability",
        "Image_URL",
        "Category"
    ]

    for column in required_columns:
        if column not in df.columns:
            df[column] = ""

    df["Title"] = df["Title"].fillna("").astype(str).str.strip()
    df["Price"] = df["Price"].fillna("Not available").astype(str)
    df["Rating"] = df["Rating"].fillna("Not rated").astype(str)
    df["Availability"] = df["Availability"].fillna("Unknown").astype(str)
    df["Image_URL"] = df["Image_URL"].fillna("").astype(str).str.strip()

    df["Category"] = (
        df["Category"]
        .fillna("Other / Miscellaneous")
        .astype(str)
        .str.strip()
    )

    rating_mapping = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    df["Rating_Score"] = (
        df["Rating"].map(rating_mapping).fillna(0)
    )

    price_numbers = df["Price"].str.replace(
        r"[^0-9.]",
        "",
        regex=True
    )

    df["Price_Value"] = pd.to_numeric(
        price_numbers,
        errors="coerce"
    )

    return df


books_data = load_books()


# FAVOURITES FUNCTIONS

def load_favourites():

    if not FAVOURITES_FILE.exists():
        return []

    try:
        with open(FAVOURITES_FILE, "r") as file:
            favourites = json.load(file)

        if not isinstance(favourites, list):
            return []

        valid_ids = set(range(len(books_data)))

        return [
            book_id
            for book_id in favourites
            if type(book_id) is int and book_id in valid_ids
        ]

    except (json.JSONDecodeError, OSError):
        return []


def save_favourites(favourites):

    with open(FAVOURITES_FILE, "w") as file:
        json.dump(favourites, file, indent=4)


# BOOK DETAILS PAGE

@app.route("/book/<int:book_id>")
def book_details(book_id):

    if book_id < 0 or book_id >= len(books_data):
        return "Book not found", 404

    book = books_data.iloc[book_id].drop(
        labels=["Rating_Score", "Price_Value"],
        errors="ignore"
    ).to_dict()

    # Get similar books from ML model
    similar_books = recommendation_model.recommend(
        book_id,
        number=5
    )

    return render_template(
        "book_details.html",
        book=book,
        book_id=book_id,
        similar_books=similar_books
    )


# ADD OR REMOVE FAVOURITE

@app.route("/favourite/<int:book_id>", methods=["POST"])
def toggle_favourite(book_id):

    if book_id < 0 or book_id >= len(books_data):
        return "Book not found", 404

    favourites = load_favourites()

    if book_id in favourites:
        favourites.remove(book_id)
    else:
        favourites.append(book_id)

    save_favourites(favourites)

    return redirect(request.referrer or url_for("home"))


# FAVOURITES PAGE

@app.route("/favourites")
def favourites_page():

    favourites = load_favourites()

    favourite_books = []

    for book_id in favourites:

        book = books_data.iloc[book_id].drop(
            labels=["Rating_Score", "Price_Value"],
            errors="ignore"
        ).to_dict()

        book["Book_ID"] = book_id

        favourite_books.append(book)

    return render_template(
        "favourites.html",
        books=favourite_books
    )


# HOME PAGE

@app.route("/")
def home():

    search_query = request.args.get("q", "").strip()
    selected_category = request.args.get("category", "").strip()

    min_price = request.args.get("min_price", "").strip()
    max_price = request.args.get("max_price", "").strip()
    min_rating = request.args.get("min_rating", "").strip()

    filtered_books = books_data.copy()

    # SEARCH BY TITLE

    if search_query:

        filtered_books = filtered_books[
            filtered_books["Title"].str.contains(
                search_query,
                case=False,
                na=False,
                regex=False
            )
        ]

    # CATEGORY FILTER

    if selected_category:

        filtered_books = filtered_books[
            filtered_books["Category"].str.strip()
            == selected_category
        ]

    # MINIMUM PRICE FILTER

    try:

        if min_price:

            min_value = float(min_price)

            filtered_books = filtered_books[
                filtered_books["Price_Value"].notna()
                & (filtered_books["Price_Value"] >= min_value)
            ]

    except ValueError:
        min_price = ""

    # MAXIMUM PRICE FILTER

    try:

        if max_price:

            max_value = float(max_price)

            filtered_books = filtered_books[
                filtered_books["Price_Value"].notna()
                & (filtered_books["Price_Value"] <= max_value)
            ]

    except ValueError:
        max_price = ""

    # MINIMUM RATING FILTER

    try:

        if min_rating:

            rating_value = int(min_rating)

            if rating_value in [1, 2, 3, 4, 5]:

                filtered_books = filtered_books[
                    filtered_books["Rating_Score"] >= rating_value
                ]

            else:
                min_rating = ""

    except ValueError:
        min_rating = ""

    # RECOMMENDATIONS

    if selected_category:

        recommendation_source = books_data[
            books_data["Category"].str.strip()
            == selected_category
        ].copy()

    else:
        recommendation_source = books_data.copy()

    # ADD BOOK ID BEFORE CONVERTING TO DICTIONARY

    recommendation_source["Book_ID"] = recommendation_source.index

    recommended_books = (
        recommendation_source
        .sort_values(
            by="Rating_Score",
            ascending=False
        )
        .head(5)
        .drop(
            columns=["Rating_Score", "Price_Value"],
            errors="ignore"
        )
        .to_dict(orient="records")
    )

    # BOOK COLLECTION

    filtered_books = filtered_books.copy()

    filtered_books["Book_ID"] = filtered_books.index

    books = (
        filtered_books
        .drop(
            columns=["Rating_Score", "Price_Value"],
            errors="ignore"
        )
        .to_dict(orient="records")
    )

    # CATEGORY LIST

    categories = sorted(
        books_data["Category"].dropna().unique().tolist()
    )

    # CURRENT FAVOURITES

    favourite_ids = load_favourites()

    return render_template(
        "index.html",
        books=books,
        recommended_books=recommended_books,
        search_query=search_query,
        categories=categories,
        selected_category=selected_category,
        total_books=len(books_data),
        result_count=len(books),
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        favourite_ids=favourite_ids
    )


# PERSONALIZED BOOK DISCOVERY

@app.route("/discover", methods=["GET", "POST"])
def discover():

    categories = sorted(
        books_data["Category"].dropna().unique().tolist()
    )

    results = []
    selected_categories = []
    min_rating = 0
    max_price = ""
    ranking = "similarity"
    submitted = False

    if request.method == "POST":

        submitted = True

        selected_categories = request.form.getlist("categories")
        selected_categories = [
            category for category in selected_categories
            if category in categories
        ]

        try:
            min_rating = int(request.form.get("min_rating", 0))
            if min_rating not in [0, 1, 2, 3, 4, 5]:
                min_rating = 0
        except ValueError:
            min_rating = 0

        try:
            max_price = float(request.form.get("max_price", ""))
            if max_price < 0:
                max_price = ""
        except ValueError:
            max_price = ""

        ranking = request.form.get("ranking", "similarity")

        if ranking not in ["similarity", "rating", "value"]:
            ranking = "similarity"

        if selected_categories:
            results = recommendation_model.recommend_by_preferences(
                categories=selected_categories,
                min_rating=min_rating,
                max_price=max_price if max_price != "" else None,
                ranking=ranking,
                number=20
            )

    favourite_ids = load_favourites()

    return render_template(
        "discover.html",
        categories=categories,
        results=results,
        selected_categories=selected_categories,
        min_rating=min_rating,
        max_price=max_price,
        ranking=ranking,
        favourite_ids=favourite_ids,
        submitted=submitted
    )
# RUN APPLICATION

if __name__ == "__main__":

    print("Starting BookNest...")
    print("Total books loaded:", len(books_data))
    print("Total categories:", books_data["Category"].nunique())

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
