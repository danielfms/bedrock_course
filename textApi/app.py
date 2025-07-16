#!/usr/bin/env python3
import os

import aws_cdk as cdk

from text_api.text_api_stack import TextApiStack


app = cdk.App()
TextApiStack(app, "TextApiStack")

app.synth()
