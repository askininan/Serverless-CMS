#!/usr/bin/env python3

import aws_cdk as cdk

from serverless_cms.serverless_cms_stack import ServerlessCmsStack


app = cdk.App()
ServerlessCmsStack(app, "serverless-cms")

app.synth()
