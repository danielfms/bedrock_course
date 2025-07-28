from aws_cdk import (
    Duration,
    Stack,
    aws_lambda,
    aws_apigateway,
    aws_iam
)
from constructs import Construct

class RagApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        rag_lambda = aws_lambda.Function(
            self,
            "Py-RagLambda",
            runtime=aws_lambda.Runtime.PYTHON_3_13,
            code=aws_lambda.Code.from_asset("services"),
            handler="rag.handler",
            timeout=Duration.seconds(30)
        )

        rag_lambda.add_to_role_policy(aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                "bedrock:RetrieveAndGenerate",
                "bedrock:Retrieve",
                "bedrock:InvokeModel",
                "bedrock:InvokeAgent"
            ])
        )

        rag_api = aws_apigateway.RestApi(self,"Py-RagApi")
        rag_resource = rag_api.root.add_resource("rag")
        lambda_integration = aws_apigateway.LambdaIntegration(rag_lambda)
        rag_resource.add_method("POST", lambda_integration)




