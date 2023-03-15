#!/usr/bin/env python3

import aws_cdk as cdk

from cdk.cdk_example_stack import CdkExampleStack


app = cdk.App()
CdkExampleStack(app, "cdk-example")

app.synth()
