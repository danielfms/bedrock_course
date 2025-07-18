import boto3
import json

from similarity import cosineSimilarity
client = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')

facts = [
    "The first computer was invented in the 1940s.",
    "John F. Kennedy was the 35th President of the United States.",
    "The first moon landing was in 1969.",
    "The capital of France is Paris.",
    "Earth is the third planet from the Sun.",
]

newFact = "I like to play computer games."
question = "Who is the president of the United States?"


def getEmbedding(text: str):
    response = client.invoke_model(
        body=json.dumps(
            {
                "inputText": text
            }
        ),
        modelId="amazon.titan-embed-text-v1",
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response.get('body').read())
    return response_body.get('embedding')

factsWithEmbeddings = []

for fact in facts:
    factsWithEmbeddings.append({
        "text": fact,
        "embedding": getEmbedding(fact)
    })

newFactEmbedding = getEmbedding(newFact)

similarities = []

for fact in factsWithEmbeddings:
    similarities.append({
        "text": fact['text'],
        "similarity": cosineSimilarity(fact['embedding'], newFactEmbedding)
    })

# Get the more related fact to newFact
print(f"Similarities for fact: '{newFact}' with:")
similarities.sort(key=lambda x: x['similarity'], reverse=True)
for similarity in similarities:
    print(f" '{similarity['text']}': {similarity['similarity']:.2f}")


