# Bedrock Knowledge Base with CDK

This project creates a complete Bedrock Knowledge Base infrastructure using AWS CDK in Python.

## Architecture

The knowledge base stack creates the following AWS resources:

1. **S3 Bucket** - Stores the source documents from the `assets/` folder
2. **OpenSearch Serverless Collection** - Vector store for embeddings
3. **IAM Role** - Permissions for Bedrock to access S3 and OpenSearch
4. **Bedrock Knowledge Base** - Main knowledge base resource
5. **Bedrock Data Source** - Connects to S3 bucket and processes documents

## Features

- **Vector Storage**: Uses OpenSearch Serverless for efficient vector search
- **S3 Integration**: Automatically loads documents from the `assets/` folder
- **Chunking**: Configurable document chunking with 512 tokens and 20% overlap
- **Embeddings**: Uses Amazon Titan Embed Text v1 model
- **Auto-cleanup**: Resources are automatically deleted when stack is destroyed

## Deployment

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Deploy the stack**:
   ```bash
   cdk deploy KnowledgeBaseStack
   ```

3. **Upload documents to assets folder**:
   - Place your documents in the `ragApi/assets/` folder
   - Supported formats: PDF, TXT, DOCX, etc.

4. **Start ingestion**:
   - The data source will automatically process documents from the assets folder
   - Monitor progress in the AWS Console under Bedrock > Knowledge Bases

## Usage

After deployment, you can:

1. **Query the knowledge base** using the Bedrock API
2. **Monitor ingestion** in the AWS Console
3. **Add more documents** by uploading to the S3 bucket

## Outputs

The stack provides these outputs:
- `KnowledgeBaseId` - ID of the created knowledge base
- `DataSourceId` - ID of the data source
- `DataBucketName` - S3 bucket name for documents
- `VectorCollectionName` - OpenSearch collection name

## Cleanup

To remove all resources:
```bash
cdk destroy KnowledgeBaseStack
```

## Configuration

Key configuration options in `knowledge_base_stack.py`:

- **Chunking**: 512 tokens with 20% overlap
- **Embedding Model**: Amazon Titan Embed Text v1
- **Vector Collection**: OpenSearch Serverless
- **Document Source**: S3 bucket with `assets/` prefix

## Security

- IAM role with minimal required permissions
- S3 bucket with auto-delete enabled
- OpenSearch access policies configured 