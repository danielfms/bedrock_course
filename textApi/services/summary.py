import boto3
import json

AWS_REGION = "us-west-2"
client = boto3.client(service_name="bedrock-runtime", region_name=AWS_REGION)
model_id = "us.amazon.nova-lite-v1:0"


def handler(event, context):
    body = json.loads(event["body"])
    text = body.get("text")
    points = event["queryStringParameters"]["points"]
    if text and points:
        response = client.converse(
            modelId=model_id,
            messages=get_conversation(text, points),
            inferenceConfig={"maxTokens": 512, "temperature": 0, "topP": 1}
        )
        result = response["output"]["message"]["content"][0]["text"]
        return {
            "statusCode": 200,
            "body": json.dumps({
                "summary": result
            })
        }
    return {
        "statusCode": 400,
        "body": json.dumps({
            "error": "text and points required"
        })
    }

def get_conversation(text: str, points: str):
    user_message = f"""Text: {text} \n
        From the text above, summarize the story in {points} points.\n
    """
    return [{
        "role": "user",
        "content": [{"text": user_message}],
    }]
