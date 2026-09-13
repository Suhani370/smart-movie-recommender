\# 🎬 Smart Movie Recommender



A content-based movie recommendation system built using Python, Scikit-learn and Streamlit.



This project recommends movies based on content similarity using movie metadata such as genres, keywords, cast and other descriptive features.



> \*\*Base Reference:\*\* This project is based on the original CampusX movie recommender project. The original implementation was used as a learning/reference foundation, and additional engineering, optimization, explainability, filtering, evaluation and UI improvements were added in this version.



\---



\## 🚀 Features



\- 🎬 Content-based movie recommendations

\- 🔍 Movie selection through an interactive Streamlit interface

\- 🎯 Top-K recommendation ranking

\- 🎚️ Minimum similarity filtering

\- 🎭 Genre-based filtering

\- 💡 Explanation of why a movie was recommended

\- 📊 Model evaluation metrics

\- ⚡ Optimized recommendation artifact for faster inference

\- 🖼️ TMDB poster integration

\- 📱 Interactive web interface using Streamlit



\---



\## 🧠 How It Works



The recommendation pipeline follows these steps:



```text

Movie Metadata

&#x20;     ↓

Data Cleaning \& Preprocessing

&#x20;     ↓

Feature Combination

&#x20;     ↓

Text Vectorization

&#x20;     ↓

Cosine Similarity

&#x20;     ↓

Top-K Candidate Retrieval

&#x20;     ↓

Filtering \& Ranking

&#x20;     ↓

Streamlit Recommendations

