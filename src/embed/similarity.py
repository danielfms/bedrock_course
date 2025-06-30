def dotProduct(embedding1: list, embedding2: list):
    return sum([embedding1[i] * embedding2[i] for i in range(len(embedding1))])

def cosineSimilarity(embedding1: list, embedding2: list):
    dotProductValue = dotProduct(embedding1, embedding2)
    magnitude1 = dotProduct(embedding1, embedding1) ** 0.5
    magnitude2 = dotProduct(embedding2, embedding2) ** 0.5
    return dotProductValue / (magnitude1 * magnitude2)