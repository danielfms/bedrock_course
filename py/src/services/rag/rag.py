import boto3
import json

AWS_REGION = 'us-west-2'

client = boto3.client(service_name="bedrock-agent-runtime", region_name=AWS_REGION)

def handler(event, context):
    body = json.loads(event["body"])
    question = body.get("question")
    if question:
        response = client.retrieve_and_generate(
            input={"text": question},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": "SYLIAYTMEC",
                    "modelArn": "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0"
                }
            }
        )
        answer = response.get("output").get("text")
        return {
            "statusCode": 200,
            "body": json.dumps({"answer": answer})
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "question needed"})
        }