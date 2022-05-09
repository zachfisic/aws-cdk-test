#!/usr/bin/env python3

import aws_cdk as cdk

from workshop_cdk.workshop_cdk_stack import WorkshopCdkStack


app = cdk.App()
WorkshopCdkStack(app, "workshop-cdk")

app.synth()
