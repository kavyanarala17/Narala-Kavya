from sentence_transformers import SentenceTransformer, util
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')


def calculate_agreement(responses):

    valid = [
        v for v in responses.values()
        if v and v != "Model not available"
    ]

    if len(valid) < 2:
        return {
            "most_common_answer": valid[0] if valid else "No answer",
            "agreement_percentage": 0
        }

    embeddings = model.encode(valid)

    similarities = []

    for i in range(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            sim = util.cos_sim(embeddings[i], embeddings[j]).item()
            similarities.append(sim)

    avg_similarity = np.mean(similarities)

    # convert to %
    agreement = avg_similarity * 100

    # pick best answer (highest average similarity)
    best_idx = np.argmax([
        np.mean([util.cos_sim(embeddings[i], embeddings[j]).item() 
        for j in range(len(embeddings)) if i != j])
        for i in range(len(embeddings))
    ])

    best_answer = valid[best_idx]

    return {
        "most_common_answer": best_answer,
        "agreement_percentage": round(agreement, 2)
    }