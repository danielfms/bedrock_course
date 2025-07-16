from langchain_aws import BedrockLLM as Bedrock
from langchain_core.prompts import ChatPromptTemplate
import boto3

AWS_REGION = "us-west-2"

bedrock = boto3.client(service_name="bedrock-runtime", region_name=AWS_REGION)

model = Bedrock(model_id="amazon.titan-text-express-v1", client=bedrock)

def invoke_model():
    response = model.invoke("What is the highest mountain in the world?")
    print(response)

invoke_model()

def first_chain():
    template = ChatPromptTemplate.from_messages(
        [
            ("system", "Write a short a short description for the userthe product provided by user"),
            ("human", "{product_name}"),
        ]
    )
    chain = template.pipe(model)
    response = chain.invoke({"product_name": "motorcycle"})
    print(response)

first_chain()