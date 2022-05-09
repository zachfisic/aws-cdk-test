#!/usr/bin/env python3

import aws_cdk as cdk

# from workshop_cdk.workshop_cdk_stack import WorkshopCdkStack
from workshop_cdk.pipeline_stack import WorkshopPipelineStack

app = cdk.App()
# WorkshopCdkStack(app, "workshop-cdk")
WorkshopPipelineStack(app, "WorkshopPipelineStack")

app.synth()
