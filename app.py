import pickle

import requests
import streamlit as st


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Smart Movie Recommender",
    page_icon="Movie",
    layout="wide"
)


# ---------------- LOAD MODEL ----------------

movies = pickle.load(
    open("model/movie_list.pkl", "rb")
)

compact_model = pickle.load(
    open("model/top_recommendations.pkl", "rb")
)


# ---------------- TMDB POSTER ----------------

@st.cache_data(ttl=3600)
def fetch_poster(movie_id):

    api_key = st.secrets.get("TMDB_API_KEY", "")

    if not api_key:
        return None

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    try:

        response = requests.get(
            url,
            params={
                "api_key": api_key,
                "language": "en-US"
            },
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return (
                "https://image.tmdb.org/t/p/w500"
                + poster_path
            )

    except requests.RequestException:
        pass

    return None


# ---------------- EXPLANATION ENGINE ----------------

def get_shared_features(selected_tags, recommended_tags):

    selected_words = set(
        str(selected_tags).lower().split()
    )

    recommended_words = set(
        str(recommended_tags).lower().split()
    )

    shared = selected_words.intersection(
        recommended_words
    )

    ignored = {
        "the",
        "and",
        "of",
        "a",
        "in",
        "on",
        "to",
        "with",
        "from",
        "his",
        "her",
        "movie",
        "film",
        "becomes",
        "between"
    }

    shared = [
        word
        for word in shared
        if len(word) > 3
        and word not in ignored
    ]

    shared = sorted(shared)

    return ", ".join(shared[:4])


# ---------------- RECOMMENDATION ENGINE ----------------

def recommend(
    movie,
    top_n=5,
    genre_filter="All",
    min_similarity=0.0
):

    movie_index = movies[
        movies["title"] == movie
    ].index[0]

    selected_tags = str(
        movies.iloc[movie_index]["tags"]
    )

    recommendations = []

    for idx, score in zip(
        compact_model[movie_index]["indices"],
        compact_model[movie_index]["scores"]
    ):

        idx = int(idx)
        score = float(score)

        # Similarity threshold
        if score < min_similarity:
            continue

        recommended_tags = str(
            movies.iloc[idx]["tags"]
        )

        # Genre filtering
        if genre_filter != "All":

            if (
                genre_filter.lower()
                not in recommended_tags.lower()
            ):
                continue

        # Explainable recommendation
        shared_features = get_shared_features(
            selected_tags,
            recommended_tags
        )

        if shared_features:

            explanation = (
                "Why recommended: "
                + shared_features
            )

        else:

            explanation = (
                "Why recommended: "
                "overall content similarity"
            )

        recommendations.append(
            {
                "title": movies.iloc[idx]["title"],
                "movie_id": movies.iloc[idx]["movie_id"],
                "score": score,
                "poster": fetch_poster(
                    movies.iloc[idx]["movie_id"]
                ),
                "explanation": explanation
            }
        )

        if len(recommendations) >= top_n:
            break

    return recommendations


# ---------------- HEADER ----------------

st.title("Smart Movie Recommender")

st.markdown(
    "### Discover movies similar to your favorite one"
)

st.caption(
    "Content-based recommendation using "
    "movie metadata and cosine similarity."
)

st.divider()


# ---------------- INPUT ----------------

movie_list = movies[
    "title"
].sort_values().values


selected_movie = st.selectbox(
    "Search or select a movie",
    movie_list
)


filter_col1, filter_col2 = st.columns(2)


with filter_col1:

    genre_filter = st.selectbox(
        "Filter by genre",
        [
            "All",
            "Action",
            "Adventure",
            "Animation",
            "Comedy",
            "Crime",
            "Drama",
            "Fantasy",
            "Horror",
            "Romance",
            "ScienceFiction",
            "Thriller"
        ]
    )


with filter_col2:

    min_similarity = st.slider(
        "Minimum similarity",
        min_value=0.0,
        max_value=0.5,
        value=0.0,
        step=0.05,
        format="%.2f"
    )


recommend_button = st.button(
    "Get Recommendations",
    use_container_width=True
)


# ---------------- RESULTS ----------------

if recommend_button:

    recommendations = recommend(
        selected_movie,
        top_n=5,
        genre_filter=genre_filter,
        min_similarity=min_similarity
    )

    st.subheader(
        f"Recommendations for **{selected_movie}**"
    )

    if not recommendations:

        st.warning(
            "No movies matched the selected filters. "
            "Try another genre or lower the minimum similarity."
        )

    else:

        st.write(
            "Movies are ranked according to "
            "their content similarity score."
        )

        cols = st.columns(5)

        for col, item in zip(
            cols,
            recommendations
        ):

            with col:

                # Poster
                if item["poster"]:

                    st.image(
                        item["poster"],
                        use_container_width=True
                    )

                else:

                    st.info(
                        "Poster unavailable"
                    )

                # Movie title
                st.markdown(
                    f"**{item['title']}**"
                )

                # Similarity progress
                st.progress(
                    min(
                        max(
                            item["score"],
                            0.0
                        ),
                        1.0
                    )
                )

                # Similarity percentage
                st.caption(
                    f"Similarity: "
                    f"{item['score'] * 100:.2f}%"
                )

                # Explanation
                st.caption(
                    item["explanation"]
                )


# ---------------- MODEL EVALUATION ----------------

with st.expander("Model Evaluation"):

    st.markdown(
        """
        **Evaluation Summary**

        - Catalog Size: 4,806 movies
        - Average Similarity: 25.63%
        - Recommendation Diversity: 80.86%
        - Recommendation Coverage: 8.68%
        - Top-K: 5

        Precision@K and Recall@K are not reported because
        the available dataset does not contain user relevance
        or preference labels.
        """
    )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "Movie Recommender System • "
    "Built with Python, Scikit-learn and Streamlit"
)