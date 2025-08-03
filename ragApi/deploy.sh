#!/bin/bash

# Deployment script following AWS samples pattern
# Based on: https://github.com/aws-samples/Setup-Amazon-Bedrock-with-Agents-and-KnowledgeBase-using-CDK

echo "🚀 Bedrock Knowledge Base Deployment Script"
echo "=========================================="

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI not configured. Please run 'aws configure' first."
    exit 1
fi

# Check if CDK is installed
if ! command -v cdk &> /dev/null; then
    echo "❌ CDK not installed. Please install CDK first."
    exit 1
fi



# Function to deploy knowledge base stack
deploy_knowledge_base() {
    echo "📦 Deploying Knowledge Base Stack..."
    cdk deploy KnowledgeBaseStack
    if [ $? -eq 0 ]; then
        echo "✅ Knowledge Base Stack deployed successfully!"
        echo ""
        echo "📋 Next steps:"
        echo "1. Go to OpenSearch Serverless Dashboard: https://us-west-2.console.aws.amazon.com/aos/home"
        echo "2. Select the collection: knowledge-base-vectors"
        echo "3. Click 'Create Vector Index'"
        echo "4. Enter index name: knowledge-base-index"
        echo "5. Add vector field: name='vector', dimension=1536, type='knn_vector'"
        echo "6. Set similarity: 'cosine' or 'euclidean'"
        echo "7. Click 'Create' and wait for it to be active"
        echo ""
        echo "⚠️  IMPORTANT: After creating the vector index, run:"
        echo "   ./deploy.sh knowledge"
        echo ""
        echo "This will deploy the Bedrock Knowledge Base that uses the vector index."
    else
        echo "❌ Knowledge Base Stack deployment failed!"
        exit 1
    fi
}

# Function to deploy all stacks
deploy_all() {
    echo "📦 Deploying all stacks..."
    cdk deploy --all
    if [ $? -eq 0 ]; then
        echo "✅ All stacks deployed successfully!"
    else
        echo "❌ Deployment failed!"
        exit 1
    fi
}

# Function to destroy all stacks
destroy_all() {
    echo "🗑️ Destroying all stacks..."
    cdk destroy --all
    if [ $? -eq 0 ]; then
        echo "✅ All stacks destroyed successfully!"
    else
        echo "❌ Destruction failed!"
        exit 1
    fi
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  knowledge     Deploy Knowledge Base Stack"
    echo "  all           Deploy all stacks"
    echo "  destroy       Destroy all stacks"
    echo "  help          Show this help message"
    echo ""
    echo "Deployment Order:"
    echo "1. $0 knowledge     # Deploy Knowledge Base Stack"
    echo "2. Create vector index manually in OpenSearch Dashboard"
    echo ""
    echo "Examples:"
    echo "  $0 knowledge      # Deploy Knowledge Base stack only"
    echo "  $0 all            # Deploy everything"
    echo "  $0 destroy        # Clean up all resources"
}

# Main script logic
case "${1:-help}" in
    "knowledge")
        deploy_knowledge_base
        ;;
    "all")
        deploy_all
        ;;
    "destroy")
        destroy_all
        ;;
    "help"|*)
        show_help
        ;;
esac 