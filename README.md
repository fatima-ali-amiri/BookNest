📚 BookNest – Smart Book Discovery System

Discover Books. Explore Categories. Find Your Next Favourite.

BookNest is a web-based Smart Book Discovery System developed as a BS Information Technology academic project. It helps users explore books, search and filter collections, view book details, save favourites, and discover similar books through content-based recommendations.

🌐 Live Demo

- Live Website: https://fat33maali112.pythonanywhere.com/
- GitHub Repository: https://github.com/fatima-ali-amiri/BookNest

✨ Features

- Browse a collection of 1,000 books.
- Search books by title.
- Filter books by category.
- Filter by minimum and maximum price.
- Filter by minimum rating.
- View individual book details.
- Explore top-rated books.
- Discover similar books using content-based recommendations.
- Save favourite books.
- Responsive and user-friendly interface.

🧠 Recommendation System

BookNest uses a content-based recommendation approach.

The system uses:

- TF-IDF: Converts book title and category text into numerical feature vectors.
- Cosine Similarity: Compares feature vectors to identify similar books.
- Category Weighting: Gives additional importance to category information.

The system recommends books based on similarities in their available features. It does not use deep learning or a neural network.

📊 Dataset and Analysis

The project uses book information collected from Books to Scrape.

Dataset Information| Result
Total Books| 1,000
Dataset Shape| 1000 × 4
Missing Values| 0
Duplicate Records| 0
Average Book Price| 38.05

Data processing included cleaning, price conversion, rating processing, and exploratory data analysis.

🛠️ Technologies Used

- Python
- Flask
- BeautifulSoup
- Pandas
- Scikit-learn
- HTML
- CSS
- CSV
- JSON
- Git and GitHub
- PythonAnywhere

🏗️ Project Architecture

                 USER
                   |
                   v
          FRONTEND (HTML/CSS)
                   |
                   v
            FLASK BACKEND
                   |
          -------------------
          |                 |
          v                 v
      BOOK DATA         FAVOURITES
       (CSV)              (JSON)
          |
          v
     SEARCH & FILTERS
          |
          v
   RECOMMENDATION ENGINE
     (TF-IDF + COSINE)
          |
          v
      BOOK RESULTS

📁 Project Structure

BookNest/
│
├── backend/
├── frontend/
├── database/
├── data/
├── docs/
├── models/
├── requirements.txt
└── README.md

⚙️ Installation and Setup

1. Clone the Repository

git clone https://github.com/fatima-ali-amiri/BookNest.git

2. Open the Project

cd BookNest

3. Create a Virtual Environment

python -m venv venv

4. Activate the Environment

Linux / Ubuntu:

source venv/bin/activate

Windows:

venv\Scripts\activate

5. Install Dependencies

pip install -r requirements.txt

6. Run the Application

python backend/app.py

Open the local website:

http://127.0.0.1:5000

🚀 Deployment

The Flask application is deployed using PythonAnywhere.

The source code is maintained on GitHub, while PythonAnywhere hosts the live web application.

Live Website: https://fat33maali112.pythonanywhere.com/

📸 Screenshots

Screenshots of the homepage, book collection, search results, book details, recommendations, and favourites will be added here.

🔮 Future Improvements

- User registration and login.
- Database integration.
- More personalized recommendations.
- Improved search capabilities.
- Admin dashboard.
- Additional book information and metadata.

🎓 Academic Project

Project Name: BookNest – Smart Book Discovery System
Field: Bachelor of Science in Information Technology (BSIT)
Project Focus: Web Scraping, Data Analysis, Machine Learning Techniques, and Web Development.

👩‍💻 Developer

Developed as an academic learning project to explore practical applications of Python, data processing, recommendation techniques, and web development.

---

Thank you for exploring BookNest! 📚
