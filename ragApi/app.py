#!/usr/bin/env python3
import os

import aws_cdk as cdk

from rag_api.rag_api_stack import RagApiStack


app = cdk.App()
RagApiStack(app, "RagApiStack")

app.synth()
