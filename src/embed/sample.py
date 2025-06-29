import boto3
import json

client = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')

fact = "The capital of Colombia is Bogota."
animal = "cat"

def get_embedding(text):
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
    return json.loads(response.get('body').read())

factResponse = get_embedding(fact)
animalResponse = get_embedding(animal)

print(factResponse.get('embedding'))
print(animalResponse.get('embedding'))

# Same length for both embeddings independent of input text
print("Fact embedding length:", len(factResponse.get('embedding')))
print("Animal embedding length:", len(animalResponse.get('embedding')))

