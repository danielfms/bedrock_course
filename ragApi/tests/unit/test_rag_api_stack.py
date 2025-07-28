import aws_cdk as core
import aws_cdk.assertions as assertions

from rag_api.rag_api_stack import RagApiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in rag_api/rag_api_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = RagApiStack(app, "rag-api")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
