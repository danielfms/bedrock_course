#!/usr/bin/env python3
import os

import aws_cdk as cdk

from image_api.image_api_stack import ImageApiStack


app = cdk.App()
ImageApiStack(app, "ImageApiStack")

app.synth()
