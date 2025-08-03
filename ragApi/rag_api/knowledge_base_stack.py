import json
from aws_cdk import (
    Stack,
    aws_iam,
    aws_s3,
    aws_opensearchserverless,
    aws_bedrock,
    RemovalPolicy,
    CfnOutput,
    Fn
)
from constructs import Construct

class KnowledgeBaseStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Hardcoded configuration values
        self.collection_name = "knowledge-base-vectors"
        self.embedding_model_arn = "arn:aws:bedrock:us-west-2::foundation-model/amazon.titan-embed-text-v1"
        self.vector_dimension = 1536
        self.chunking_strategy = "FIXED_SIZE"
        self.max_tokens = 512
        self.overlap_percentage = 20

        # ========================================
        # OPENSEARCH INFRASTRUCTURE
        # ========================================

        # 1. S3 Bucket for document storage
        self.data_bucket = aws_s3.Bucket(
            self,
            "DocumentBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # 2. Encryption Security Policy
        self.encryption_policy = aws_opensearchserverless.CfnSecurityPolicy(
            self,
            "EncryptionPolicy",
            name="kb-encryption-policy",
            type="encryption",
            policy=json.dumps({
                "Rules": [
                    {
                        "Resource": [
                            f"collection/{self.collection_name}"
                        ],
                        "ResourceType": "collection"
                    }
                ],
                "AWSOwnedKey": True
            })
        )

        # 3. Network Security Policy (allows public access - modify for your security requirements)
        self.network_policy = aws_opensearchserverless.CfnSecurityPolicy(
            self,
            "NetworkPolicy",
            name="kb-network-policy",
            type="network",
            policy=json.dumps([
                {
                    "Rules": [
                        {
                            "Resource": [
                                f"collection/{self.collection_name}"
                            ],
                            "ResourceType": "collection"
                        }
                    ],
                    "AllowFromPublic": True
                }
            ])
        )

        # 4. OpenSearch Serverless Collection
        self.vector_collection = aws_opensearchserverless.CfnCollection(
            self,
            "VectorCollection",
            name=self.collection_name,
            type="VECTORSEARCH",
            description="Vector collection for knowledge base embeddings"
        )
        
        # Add dependencies for OpenSearch collection
        self.vector_collection.add_dependency(self.encryption_policy)
        self.vector_collection.add_dependency(self.network_policy)

        # 5. IAM Role for Bedrock with comprehensive permissions
        self.bedrock_role = aws_iam.Role(
            self,
            "BedrockRole",
            assumed_by=aws_iam.ServicePrincipal("bedrock.amazonaws.com"),
            inline_policies={
                "OpenSearchPolicy": aws_iam.PolicyDocument(
                    statements=[
                        aws_iam.PolicyStatement(
                            effect=aws_iam.Effect.ALLOW,
                            actions=[
                                "aoss:APIAccessAll",
                                "aoss:CreateIndex",
                                "aoss:DeleteIndex",
                                "aoss:UpdateIndex",
                                "aoss:DescribeIndex",
                                "aoss:ListIndices",
                                "aoss:CreateCollectionItems",
                                "aoss:DeleteCollectionItems",
                                "aoss:UpdateCollectionItems",
                                "aoss:BatchGetCollectionItems",
                                "aoss:Search",
                                "aoss:CreateCollection",
                                "aoss:DeleteCollection",
                                "aoss:DescribeCollection",
                                "aoss:ListCollections",
                                "aoss:UpdateCollection"
                            ],
                            resources=["*"]
                        ),
                        aws_iam.PolicyStatement(
                            effect=aws_iam.Effect.ALLOW,
                            actions=[
                                "s3:GetObject",
                                "s3:ListBucket",
                                "s3:GetBucketLocation"
                            ],
                            resources=[
                                self.data_bucket.bucket_arn,
                                f"{self.data_bucket.bucket_arn}/*"
                            ]
                        ),
                        aws_iam.PolicyStatement(
                            effect=aws_iam.Effect.ALLOW,
                            actions=[
                                "kms:Decrypt",
                                "kms:Encrypt", 
                                "kms:GenerateDataKey",
                                "kms:DescribeKey"
                            ],
                            resources=["*"]
                        ),
                        aws_iam.PolicyStatement(
                            effect=aws_iam.Effect.ALLOW,
                            actions=[
                                "logs:CreateLogGroup",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents"
                            ],
                            resources=["*"]
                        )
                    ]
                )
            }
        )

        # 6. Data Access Policy for Bedrock role
        self.data_access_policy = aws_opensearchserverless.CfnAccessPolicy(
            self,
            "DataAccessPolicy",
            name="kb-data-access-policy",
            type="data",
            policy=json.dumps([
                {
                    "Rules": [
                        {
                            "Resource": [
                                f"collection/{self.collection_name}"
                            ],
                            "Permission": [
                                "aoss:*"
                            ],
                            "ResourceType": "collection"
                        },
                        {
                            "Resource": ["*"],
                            "Permission": [
                                "aoss:*"
                            ],
                            "ResourceType": "index"
                        }
                    ],
                    "Principal": [
                        self.bedrock_role.role_arn
                    ]
                }
            ])
        )
        
        # Add dependencies for data access policy
        self.data_access_policy.add_dependency(self.vector_collection)

        # ========================================
        # BEDROCK KNOWLEDGE BASE
        # ========================================

        # 7. Bedrock Knowledge Base
        self.knowledge_base = aws_bedrock.CfnKnowledgeBase(
            self,
            "KnowledgeBase",
            knowledge_base_configuration=aws_bedrock.CfnKnowledgeBase.KnowledgeBaseConfigurationProperty(
                type="VECTOR",
                vector_knowledge_base_configuration=aws_bedrock.CfnKnowledgeBase.VectorKnowledgeBaseConfigurationProperty(
                    embedding_model_arn=self.embedding_model_arn
                )
            ),
            storage_configuration=aws_bedrock.CfnKnowledgeBase.StorageConfigurationProperty(
                type="OPENSEARCH_SERVERLESS",
                opensearch_serverless_configuration=aws_bedrock.CfnKnowledgeBase.OpenSearchServerlessConfigurationProperty(
                    collection_arn=self.vector_collection.attr_arn,
                    field_mapping=aws_bedrock.CfnKnowledgeBase.FieldMappingProperty(
                        vector_field="vector",
                        text_field="text",
                        metadata_field="metadata"
                    ),
                    vector_index_name=self.index_name
                )
            ),
            name="my-knowledge-base",
            description="Knowledge base for RAG applications",
            role_arn=self.bedrock_role.role_arn
        )

        # Add dependencies for knowledge base
        self.knowledge_base.add_dependency(self.vector_collection)
        self.knowledge_base.add_dependency(self.data_access_policy)

        # 8. Bedrock Data Source
        self.data_source = aws_bedrock.CfnDataSource(
            self,
            "DataSource",
            knowledge_base_id=self.knowledge_base.attr_knowledge_base_id,
            name="assets-data-source",
            description="Data source from S3 bucket",
            data_source_configuration={
                "type": "S3",
                "s3Configuration": {
                    "bucketArn": self.data_bucket.bucket_arn
                }
            },
            vector_ingestion_configuration={
                "chunkingConfiguration": {
                    "chunkingStrategy": self.chunking_strategy,
                    "fixedSizeChunkingConfiguration": {
                        "maxTokens": self.max_tokens,
                        "overlapPercentage": self.overlap_percentage
                    }
                }
            }
        )
        
        # Add dependency for data source
        self.data_source.add_dependency(self.knowledge_base)

        # ========================================
        # OUTPUTS
        # ========================================

        # OpenSearch Outputs
        CfnOutput(
            self,
            "CollectionName",
            value=self.vector_collection.name,
            description="OpenSearch Collection Name"
        )

        CfnOutput(
            self,
            "CollectionArn",
            value=self.vector_collection.attr_arn,
            description="OpenSearch Collection ARN"
        )



        CfnOutput(
            self,
            "BucketName",
            value=self.data_bucket.bucket_name,
            description="S3 Bucket Name"
        )

        CfnOutput(
            self,
            "BedrockRoleArn",
            value=self.bedrock_role.role_arn,
            description="Bedrock IAM Role ARN"
        )

        # Bedrock Outputs
        CfnOutput(
            self,
            "KnowledgeBaseId",
            value=self.knowledge_base.attr_knowledge_base_id,
            description="Knowledge Base ID"
        )

        CfnOutput(
            self,
            "DataSourceId",
            value=self.data_source.attr_data_source_id,
            description="Data Source ID"
        )

        CfnOutput(
            self,
            "KnowledgeBaseName",
            value=self.knowledge_base.name,
            description="Knowledge Base Name"
        ) 