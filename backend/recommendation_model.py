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


