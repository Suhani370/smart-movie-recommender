import pickle
import numpy as np

# Load compact recommendation model
movies = pickle.load(open("model/movie_list.pkl", "rb"))
recommendation_model = pickle.load(
    open("model/top_recommendations.pkl", "rb")
)

TOP_K = 5


def recommend_indices(index):
    data = recommendation_model[index]

    indices = data["indices"]
    scores = data["scores"]

    return [
        int(i)
        for i, _ in zip(indices[:TOP_K], scores[:TOP_K])
    ]


def recommendation_scores(index):
    data = recommendation_model[index]

    scores = data["scores"]

    return [
        float(score)
        for score in scores[:TOP_K]
    ]


# ---------- 1. Recommendation Coverage ----------
sample_size = min(100, len(movies))

sample_indices = np.linspace(
    0,
    len(movies) - 1,
    sample_size,
    dtype=int
)

recommended_movies = set()

for index in sample_indices:
    recommended_movies.update(recommend_indices(index))

coverage = len(recommended_movies) / len(movies)


# ---------- 2. Average Similarity ----------
scores = []

for index in sample_indices:
    scores.extend(recommendation_scores(index))

average_similarity = np.mean(scores)


# ---------- 3. Recommendation Diversity ----------
diversity_scores = []

for index in sample_indices:
    rec_indices = recommend_indices(index)
    rec_scores = recommendation_scores(index)

    if len(rec_indices) < 2:
        continue

    pairwise_distances = []

    for i in range(len(rec_indices)):
        for j in range(i + 1, len(rec_indices)):
            # Approximate pairwise diversity using recommendation scores.
            similarity_score = min(
                rec_scores[i],
                rec_scores[j]
            )

            pairwise_distances.append(
                1 - similarity_score
            )

    if pairwise_distances:
        diversity_scores.append(
            np.mean(pairwise_distances)
        )

diversity = np.mean(diversity_scores)


# ---------- Report ----------
print("=" * 50)
print("SMART MOVIE RECOMMENDER - MODEL EVALUATION")
print("=" * 50)

print(f"Movies in catalog       : {len(movies)}")
print(f"Movies sampled          : {sample_size}")
print(f"Top-K                   : {TOP_K}")
print(f"Recommendation coverage : {coverage * 100:.2f}%")
print(f"Average similarity      : {average_similarity * 100:.2f}%")
print(f"Recommendation diversity: {diversity * 100:.2f}%")

print("=" * 50)
print("Evaluation completed successfully.")
print("Note: No user relevance labels are available in this dataset.")
print("Therefore Precision@K/Recall@K are not claimed.")
