import pickle
import numpy as np

# Load trained model
movies = pickle.load(open("model/movie_list.pkl", "rb"))
similarity = pickle.load(open("model/similarity.pkl", "rb"))

TOP_K = 5

def recommend_indices(index):
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    return [i for i, score in distances[1:TOP_K + 1]]


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
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    top_scores = [
        float(score)
        for _, score in distances[1:TOP_K + 1]
    ]

    scores.extend(top_scores)

average_similarity = np.mean(scores)


# ---------- 3. Recommendation Diversity ----------
diversity_scores = []

for index in sample_indices:
    rec_indices = recommend_indices(index)

    if len(rec_indices) < 2:
        continue

    pairwise_distances = []

    for i in range(len(rec_indices)):
        for j in range(i + 1, len(rec_indices)):
            similarity_score = similarity[
                rec_indices[i],
                rec_indices[j]
            ]

            pairwise_distances.append(
                1 - float(similarity_score)
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
