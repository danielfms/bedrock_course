import boto3
import json
import base64

from similarity import cosineSimilarity

client = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')

images = [
    "1.png",
    "2.png",
    "3.png"
]

def getImageEmbedding(imagePath: str):
    with open(imagePath, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    response = client.invoke_model(
        body=json.dumps(
            {
                "inputImage": base64_image
            }
        ),
        modelId="amazon.titan-embed-image-v1",
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = json.loads(response.get('body').read())
    return response_body.get('embedding')


imagesWithEmbeddings = []
for image in images:
    imagesWithEmbeddings.append({
        "image": image,
        "embedding": getImageEmbedding(image)
    })

test_image = "image.png"
test_image_embedding = getImageEmbedding(test_image)

similarities = []
for image in imagesWithEmbeddings:
    similarities.append({
        "image": image['image'],
        "similarity": cosineSimilarity(image['embedding'], test_image_embedding)
    })

# Get the more related image to test_image
print(f"Similarities for image: '{test_image}' with:")
similarities.sort(key=lambda x: x['similarity'], reverse=True)
for similarity in similarities:
    print(f" '{similarity['image']}': {similarity['similarity']:.2f}")