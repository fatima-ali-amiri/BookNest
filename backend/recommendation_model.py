import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "all_books_cleaned.csv"


class BookRecommendationModel:

    def __init__(self):

        self.books = pd.read_csv(DATA_FILE)

        self.books["Title"] = (
            self.books["Title"].fillna("").astype(str)
        )

        self.books["Category"] = (
            self.books["Category"].fillna("").astype(str)
        )

        self.books["Rating"] = (
            self.books["Rating"].fillna("Not rated").astype(str)
        )

        # Combine book title and category
        self.books["Features"] = (
            self.books["Title"] + " " +
            self.books["Category"] + " " +
            self.books["Category"]
        )

        # Convert text into numerical vectors
        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.tfidf_matrix = self.vectorizer.fit_transform(
            self.books["Features"]
        )

        # Calculate similarity between books
        self.similarity_matrix = cosine_similarity(
            self.tfidf_matrix
        )

    def recommend(self, book_id, number=5):

        if book_id < 0 or book_id >= len(self.books):
            return []

        similarity_scores = list(
            enumerate(self.similarity_matrix[book_id])
        )

        # Exclude the selected book itself
        similarity_scores = [
            item for item in similarity_scores
            if item[0] != book_id
        ]

        # Sort by similarity
        similarity_scores.sort(
            key=lambda item: item[1],
            reverse=True
        )

        recommendations = []

        for index, score in similarity_scores[:number]:

            book = self.books.iloc[index].to_dict()

            book["Book_ID"] = int(index)
            book["Similarity_Score"] = round(
                float(score), 3
            )

            recommendations.append(book)

        return recommendations

    def recommend_by_preferences(
        self,
        categories=None,
        min_rating=0,
        max_price=None,
        ranking="similarity",
        number=10
    ):

        selected_books = self.books.copy()

        # Create user interest profile
        if categories:
            interest_text = " ".join(categories)
            user_vector = self.vectorizer.transform([interest_text])

            similarity_scores = cosine_similarity(
                user_vector,
                self.tfidf_matrix
            ).flatten()
        else:
            similarity_scores = [0.0] * len(self.books)

        selected_books["Book_ID"] = selected_books.index
        selected_books["Similarity_Score"] = similarity_scores

        # Convert ratings into numbers
        rating_mapping = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }

        selected_books["Rating_Score"] = (
            selected_books["Rating"].map(rating_mapping).fillna(0)
        )

        # Convert prices into numbers
        price_values = pd.to_numeric(
            selected_books["Price"].astype(str).str.replace(
                r"[^0-9.]",
                "",
                regex=True
            ),
            errors="coerce"
        )

        selected_books["Price_Value"] = price_values

        # Filter by selected categories
        if categories:
            selected_books = selected_books[
                selected_books["Category"].isin(categories)
            ]

        # Filter by minimum rating
        if min_rating:
            selected_books = selected_books[
                selected_books["Rating_Score"] >= min_rating
            ]

        # Filter by maximum budget
        if max_price is not None:
            selected_books = selected_books[
                selected_books["Price_Value"].notna()
                & (selected_books["Price_Value"] <= max_price)
            ]

        # Rank recommendations
        if ranking == "rating":
            selected_books = selected_books.sort_values(
                ["Rating_Score", "Similarity_Score"],
                ascending=False
            )

        elif ranking == "value":
            selected_books["Value_Score"] = (
                selected_books["Rating_Score"]
                / selected_books["Price_Value"].replace(0, float("nan"))
            )

            selected_books = selected_books.sort_values(
                ["Value_Score", "Rating_Score"],
                ascending=False
            )

        else:
            selected_books = selected_books.sort_values(
                ["Similarity_Score", "Rating_Score"],
                ascending=False
            )

        # Prepare final recommendations
        recommendations = selected_books.head(number).copy()

        recommendations["Why_Recommended"] = (
            "Matches your selected interests"
        )

        return recommendations.to_dict(orient="records")
# Initialize the recommendation model
recommendation_model = BookRecommendationModel()


if __name__ == "__main__":

    print("BookNest ML Model Loaded!")
    print("Total books:", len(recommendation_model.books))

    print("\nRecommendations for first book:")

    results = recommendation_model.recommend(0, 5)

    for book in results:
        print(
            book["Title"],
            "| Category:", book["Category"],
            "| Similarity:", book["Similarity_Score"]
        )


