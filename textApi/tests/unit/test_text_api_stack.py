import aws_cdk as core
import aws_cdk.assertions as assertions

from text_api.text_api_stack import TextApiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in text_api/text_api_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TextApiStack(app, "text-api")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
