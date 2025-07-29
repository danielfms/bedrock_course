#!/usr/bin/env python3
import os

import aws_cdk as cdk

from rag_api.rag_api_stack import RagApiStack
from rag_api.knowledge_base_stack import KnowledgeBaseStack


app = cdk.App()
RagApiStack(app, "RagApiStack")
KnowledgeBaseStack(app, "KnowledgeBaseStack")

app.synth()
