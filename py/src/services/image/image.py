import boto3
import json
import base64
import random
from time import time

AWS_REGION = 'us-west-2'
S3_BUCKET = 'image-bucket-dfms'

bedrock_client = boto3.client(service_name="bedrock-runtime", region_name=AWS_REGION)
s3_client = boto3.client("s3")

seed = random.randint(0, 858993460)

def handler(event, context):
    body = json.loads(event["body"])
    description = body.get("description")
    if description:
        model_config = get_model_config(description)
        response = bedrock_client.invoke_model(
            modelId="amazon.titan-image-generator-v1",
            body=model_config,
            contentType="application/json",
            accept="application/json"
        )
        response_body = json.loads(response.get("body").read())
        base64_image = response_body.get("images")[0]
        signed_url = save_image_to_s3(base64_image)
        return {
            "statusCode": 200,
            "body": json.dumps({"url": signed_url})
        }
    

def save_image_to_s3(base64_image):
    image_file = base64.b64decode(base64_image)
    timestamp = int(time())
    image_name = str(timestamp) + ".png"

    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=image_name,
        Body=image_file,
    )
    signed_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET, 'Key': image_name},
        ExpiresIn=3600
    )
    return signed_url


def get_model_config(description):
    return json.dumps({
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": description
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "height": 512,
            "width": 512,
            "quality": "standard",
            "seed": seed
        }
    })