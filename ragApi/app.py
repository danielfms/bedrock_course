#!/usr/bin/env python3
import os

import aws_cdk as cdk

from rag_api.rag_api_stack import RagApiStack
#from rag_api.knowledge_base_stack import KnowledgeBaseStack


app = cdk.App()

# Create stacks
rag_stack = RagApiStack(app, "RagApiStack")
#knowledge_base_stack = KnowledgeBaseStack(app, "KnowledgeBaseStack")

app.synth()
