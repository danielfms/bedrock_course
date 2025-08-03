# Bedrock Knowledge Base Deployment Guide

This guide follows the AWS samples pattern for deploying OpenSearch Serverless with Bedrock Knowledge Base using CDK.

## Architecture

The solution uses a single stack approach:

1. **Knowledge Base Stack** - Creates all infrastructure in a single stack:
   - OpenSearch Serverless collection and policies
   - S3 bucket for document storage
   - IAM roles and permissions
   - Bedrock Knowledge Base and Data Source

## Prerequisites

- AWS CLI installed and configured
- AWS CDK installed
- Python 3.8+ with required dependencies

## Deployment Process

### Step 1: Setup Configuration

```bash
# Setup configuration (automatic IAM user ARN detection)
python setup_config.py
```

### Step 2: Deploy Knowledge Base Stack

```bash
# Deploy all infrastructure in one stack
./deploy.sh knowledge
```

This creates:
- S3 bucket for document storage
- OpenSearch Serverless collection and policies
- IAM roles and permissions
- Bedrock Knowledge Base and Data Source

### Step 3: Create Vector Index (Manual Step)

After the stack is deployed, you need to manually create the vector index:

1. Go to [OpenSearch Serverless Dashboard](https://us-west-2.console.aws.amazon.com/aos/home)
2. Select the collection: `knowledge-base-vectors`
3. Click "Create Vector Index"
4. Enter index name: `knowledge-base-index`
5. Add vector field:
   - Name: `vector`
   - Dimension: `1536` (for Titan Embed Text v1)
6. Click "Create"

## Configuration

### Automatic Setup

Run the setup script to automatically configure your IAM user ARN:

```bash
python setup_config.py
```

### Manual Configuration

If automatic setup fails, manually update the configuration in `rag_api/config.py`:

```python
CONFIG = {
    "collectionName": "knowledge-base-vectors",
    "indexName": "knowledge-base-index",
    "iamUserArn": "arn:aws:iam::YOUR_ACCOUNT_ID:user/YOUR_USER_NAME",  # Update this
    "region": "us-west-2",
    "embeddingModel": "arn:aws:bedrock:us-west-2::foundation-model/amazon.titan-embed-text-v1",
    "vectorDimension": 1536,
    "chunkingStrategy": "FIXED_SIZE",
    "maxTokens": 512,
    "overlapPercentage": 20
}
```

### Vector Dimensions

The default vector dimension is 1536 for Amazon Titan Embed Text v1. If using a different model, update the dimension in the manual vector index creation step.

## Usage

### Upload Documents

1. Upload documents to the S3 bucket created by the OpenSearch stack
2. The data source will automatically process documents
3. Monitor ingestion in the AWS Console under Bedrock > Knowledge Bases

### Query Knowledge Base

Use the Bedrock API to query the knowledge base:

```python
import boto3

client = boto3.client('bedrock-agent-runtime', region_name='us-west-2')

response = client.retrieve_and_generate(
    input={"text": "Your question here"},
    retrieveAndGenerateConfiguration={
        "type": "KNOWLEDGE_BASE",
        "knowledgeBaseConfiguration": {
            "knowledgeBaseId": "YOUR_KNOWLEDGE_BASE_ID",
            "modelArn": "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0"
        }
    }
)
```

## Troubleshooting

### 401 Authentication Errors

If you encounter 401 errors:

1. Ensure the vector index is created before deploying the Bedrock stack
2. Check that the IAM role has proper permissions
3. Verify the collection is in "Active" state

### Deployment Order

Always follow this order:
1. Deploy OpenSearch stack
2. Create vector index manually
3. Deploy Bedrock stack

### Region Considerations

This setup is configured for `us-west-2`. For other regions:
- Update the embedding model ARN
- Ensure OpenSearch Serverless is available in your region

## Cleanup

To remove all resources:

```bash
./deploy.sh destroy
```

## Security Notes

- The network policy allows public access to OpenSearch
- Modify security policies according to your requirements
- Consider using VPC endpoints for production deployments

## References

- [AWS Samples Repository](https://github.com/aws-samples/Setup-Amazon-Bedrock-with-Agents-and-KnowledgeBase-using-CDK)
- [Medium Article](https://medium.com/@micheldirk/on-aws-cdk-and-amazon-bedrock-knowledge-bases-14c7b208e4cb)
- [OpenSearch Serverless Documentation](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-overview.html)
- [Bedrock Knowledge Base Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) 