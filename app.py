import pickle
import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Movie Recommender",
    page_icon="??",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
movies = pickle.load(open("model/movie_list.pkl", "rb"))
compact_model = pickle.load(open("model/top_recommendations.pkl", "rb"))

# ---------------- TMDB POSTER ----------------
@st.cache_data(ttl=3600)
def fetch_poster(movie_id):
    api_key = st.secrets.get("TMDB_API_KEY", "")
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
            return "https://image.tmdb.org/t/p/w500" + poster_path

    except requests.RequestException:
        pass

    return None


# ---------------- RECOMMENDATION ENGINE ----------------
def get_shared_features(selected_tags, recommended_tags):
    selected_words = set(selected_tags.lower().split())
    recommended_words = set(recommended_tags.lower().split())

    shared = selected_words.intersection(recommended_words)

    ignored = {
        "the", "and", "of", "a", "in", "on", "to",
        "with", "from", "his", "her", "movie", "film"
    }

    shared = [
        word for word in shared
        if len(word) > 3 and word not in ignored
    ]

    return shared[:4]


def recommend(movie, top_n=5, genre_filter="All", min_similarity=0.0):
    movie_index = movies[movies["title"] == movie].index[0]

    recommendations = []

    for idx, score in zip(
        compact_model[movie_index]["indices"],
        compact_model[movie_index]["scores"]
    ):
        idx = int(idx)
        score = float(score)

        if score < min_similarity:
            continue

        if genre_filter != "All":
            if genre_filter.lower() not in str(movies.iloc[idx]["tags"]).lower():
                continue

        recommendations.append({
            "title": movies.iloc[idx]["title"],
            "movie_id": movies.iloc[idx]["movie_id"],
            "score": score,
            "poster": fetch_poster(movies.iloc[idx]["movie_id"]),
            "explanation": get_shared_features(
                movies.iloc[movie_index]["tags"],
                movies.iloc[idx]["tags"]
            )
        })

        if len(recommendations) >= top_n:
            break

    return recommendations


    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommendations = []

    for i, score in distances[1:]:
        if score < min_similarity:
            continue

        title = movies.iloc[i]["title"]
        movie_id = movies.iloc[i]["movie_id"]
        recommended_tags = str(movies.iloc[i]["tags"])

        # Genre filtering using movie metadata tags
        if genre_filter != "All":
            if genre_filter.lower() not in recommended_tags.lower():
                continue

        shared_features = get_shared_features(
            selected_tags,
            recommended_tags
        )

        if shared_features:
            explanation = "Similar themes: " + ", ".join(shared_features)
        else:
            explanation = "Recommended because of overall content similarity."

        recommendations.append({
            "title": title,
            "movie_id": movie_id,
            "score": float(score),
            "poster": fetch_poster(movie_id),
            "explanation": explanation
        })

        if len(recommendations) == top_n:
            break

    return recommendations

# ---------------- HEADER ----------------
st.title("?? Smart Movie Recommender")
st.markdown(
    "### Discover movies similar to your favorite one"
)

st.caption(
    "Content-based recommendation using movie metadata and cosine similarity."
)

st.divider()

# ---------------- INPUT ----------------
movie_list = movies["title"].sort_values().values

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
    "? Get Recommendations",
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

    st.subheader(f"Recommendations for **{selected_movie}**")

    if not recommendations:
        st.warning(
            "No movies matched the selected filters. "
            "Try another genre or lower the minimum similarity."
        )
    else:
        st.write(
            "Movies are ranked according to their content similarity score."
        )

        cols = st.columns(5)

        for col, item in zip(cols, recommendations):

            with col:

                if item["poster"]:
                    st.image(
                        item["poster"],
                        use_container_width=True
                    )
                else:
                    st.info("Poster unavailable")

                st.markdown(f"**{item['title']}**")

                score = item["score"] * 100

                st.progress(
                    min(max(item["score"], 0.0), 1.0)
                )

                st.caption(
                    f"Similarity: {score:.2f}%"
                )

                st.caption(
                    f"?? {item['explanation']}"
                )


# ---------------- FOOTER ----------------
st.divider()

st.caption(
    "Movie Recommender System • Built with Python, Scikit-learn and Streamlit"
)




