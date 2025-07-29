import json
from aws_cdk import (
    Stack,
    aws_iam,
    aws_s3,
    aws_opensearchserverless,
    aws_bedrock,
    RemovalPolicy,
    Duration,
    CfnOutput
)
from constructs import Construct

class KnowledgeBaseStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Bucket for data source
        data_bucket = aws_s3.Bucket(
            self,
            "KnowledgeBaseDataBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # 2. OpenSearch Serverless Collection for vector store
        vector_collection = aws_opensearchserverless.CfnCollection(
            self,
            "VectorCollection",
            name="knowledge-base-vectors",
            type="VECTORSEARCH",
            description="Vector collection for knowledge base embeddings"
        )

        # 3. OpenSearch Serverless Access Policy
        access_policy = aws_opensearchserverless.CfnAccessPolicy(
            self,
            "AccessPolicy",
            name="knowledge-base-access-policy",
            type="data",
            policy=json.dumps([
                {
                    "Rules": [
                        {
                            "Resource": [
                                f"collection/{vector_collection.name}"
                            ],
                            "Permission": [
                                "aoss:*"
                            ],
                            "ResourceType": "collection"
                        }
                    ],
                    "Principal": [
                        "arn:aws:iam::*:role/KnowledgeBaseRole"
                    ]
                }
            ])
        )

        # 4. IAM Role for Bedrock Knowledge Base
        knowledge_base_role = aws_iam.Role(
            self,
            "KnowledgeBaseRole",
            assumed_by=aws_iam.ServicePrincipal("bedrock.amazonaws.com"),
            inline_policies={
                "KnowledgeBasePolicy": aws_iam.PolicyDocument(
                    statements=[
                        aws_iam.PolicyStatement(
                            effect=aws_iam.Effect.ALLOW,
                            actions=["s3:GetObject", "s3:ListBucket"],
                            resources=[
                                data_bucket.bucket_arn,
                                f"{data_bucket.bucket_arn}/*"
                            ]
                        ),
                        aws_iam.PolicyStatement(
                            effect=aws_iam.Effect.ALLOW,
                            actions=["aoss:APIAccessAll"],
                            resources=["*"]
                        ),
                        aws_iam.PolicyStatement(
                            effect=aws_iam.Effect.ALLOW,
                            actions=["kms:Decrypt", "kms:Encrypt", "kms:GenerateDataKey"],
                            resources=["*"]
                        )
                    ]
                )
            }
        )

        # 5. Bedrock Knowledge Base
        knowledge_base = aws_bedrock.CfnKnowledgeBase(
            self,
            "KnowledgeBase",
            knowledge_base_configuration={
                "type": "VECTOR",
                "vectorKnowledgeBaseConfiguration": {
                    "embeddingModelArn": "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
                }
            },
            name="my-knowledge-base",
            description="Knowledge base for RAG applications",
            role_arn=knowledge_base_role.role_arn
        )

        # 6. Bedrock Data Source
        data_source = aws_bedrock.CfnDataSource(
            self,
            "DataSource",
            knowledge_base_id=knowledge_base.attr_knowledge_base_id,
            name="assets-data-source",
            description="Data source from assets folder",
            data_source_configuration={
                "type": "S3",
                "s3Configuration": {
                    "bucketArn": data_bucket.bucket_arn,
                    "inclusionPrefixes": ["assets/"]
                }
            },
            vector_ingestion_configuration={
                "chunkingConfiguration": {
                    "chunkingStrategy": "FIXED_SIZE",
                    "fixedSizeChunkingConfiguration": {
                        "maxTokens": 512,
                        "overlapPercentage": 20
                    }
                }
            }
        )

        # 7. Outputs
        CfnOutput(
            self,
            "KnowledgeBaseId",
            value=knowledge_base.attr_knowledge_base_id,
            description="Knowledge Base ID"
        )

        CfnOutput(
            self,
            "DataSourceId",
            value=data_source.attr_data_source_id,
            description="Data Source ID"
        )

        CfnOutput(
            self,
            "DataBucketName",
            value=data_bucket.bucket_name,
            description="S3 Bucket for data source"
        )

        CfnOutput(
            self,
            "VectorCollectionName",
            value=vector_collection.name,
            description="OpenSearch Vector Collection Name"
        )