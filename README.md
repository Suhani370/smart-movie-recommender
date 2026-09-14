# Smart Movie Recommender

A content-based movie recommendation system built with Python, Scikit-learn and Streamlit.

> **Base Reference:** This project is based on the original CampusX movie recommender project. Additional engineering, optimization, explainability, filtering, evaluation and UI improvements were added in this version.

## Live Demo

https://smart-movie-recommender-habuvwz8y9xdjyxfohovjh.streamlit.app/

## GitHub Repository

https://github.com/Suhani370/smart-movie-recommender

## Features

- Content-based movie recommendations
- Interactive Streamlit interface
- Top-K recommendation ranking
- Genre-based filtering
- Minimum similarity filtering
- Similarity scores for recommendations
- Explainable recommendations using shared movie features
- TMDB poster integration
- Model evaluation metrics
- Compact Top-K recommendation artifact

## How It Works

Movie Metadata -> Data Cleaning & Preprocessing -> Feature Combination -> Text Vectorization -> Cosine Similarity -> Top-K Retrieval -> Filtering & Ranking -> Streamlit Recommendations

The system combines relevant movie metadata into a text representation and uses cosine similarity to identify similar movies.

## Model Evaluation

The system was evaluated on 100 sampled movies using Top-K = 5.

| Metric | Result |
|---|---:|
| Movies in catalog | 4,806 |
| Movies sampled | 100 |
| Top-K | 5 |
| Recommendation Coverage | 8.72% |
| Average Similarity | 25.63% |
| Recommendation Diversity | 80.86% |

Precision@K and Recall@K are not reported because the dataset does not contain user relevance labels or interaction data.

## Optimization

The dense similarity matrix is approximately 176 MB and is excluded from GitHub. A compact Top-50 recommendation artifact of approximately 2.1 MB is used for application inference.

The compact artifact stores the highest-ranked candidate indices and similarity scores for each movie, enabling efficient Top-K retrieval without loading the full similarity matrix during app inference.

## Technology Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- TMDB API
- Pickle

## Project Structure

smart-movie-recommender/

|-- app.py
|-- evaluate_model.py
|-- notebook86c26b4f17.ipynb
|-- requirements.txt
|-- README.md
|-- tmdb_5000_movies.csv
|-- tmdb_5000_credits.csv
-- model/
    |-- movie_list.pkl
    -- top_recommendations.pkl

## Installation

`ash
git clone https://github.com/Suhani370/smart-movie-recommender.git
cd smart-movie-recommender
pip install -r requirements.txt
`

## Run the Application

Create .streamlit/secrets.toml with your TMDB API key, then run:

`ash
python -m streamlit run app.py
`

Never commit .streamlit/secrets.toml or expose your TMDB API key publicly.

## Model Evaluation

`ash
python evaluate_model.py
`

## Dataset

TMDB 5000 Movies and TMDB 5000 Credits datasets.

## TMDB Attribution

This product uses the TMDB API but is not endorsed or certified by TMDB.

Movie data and posters are provided by TMDB.

## Acknowledgement

Initial recommendation implementation learned from and based on the CampusX movie recommender project. This version extends the reference with explainable recommendations, filtering, evaluation, compact Top-K retrieval, improved Streamlit UI and TMDB poster integration.

## Author

**Suhani Singh**

GitHub: https://github.com/Suhani370
