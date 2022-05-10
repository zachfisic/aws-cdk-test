from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines
)
from workshop_cdk.pipeline_stage import WorkshopPipelineStage

class WorkshopPipelineStack(Stack):
    def __init__(self, scope:Construct, id:str, **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)

        # Create a CodeCommit repository called "WorkshopRepo"
        repo = codecommit.Repository(
            self,
            'WorkshopRepo',
            repository_name='WorkshopRepo'
        )

        # Initialize the pipeline with the required values. This will serve as the base component moving forward.
        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth", # Synth of pipeline describes commands necessary to install dependencies, build, and synth the application from source. 
                input=pipelines.CodePipelineSource.code_commit(repo, "main"), # The input of the synth step specifies the CDK source repo
                commands=[
                    "npm install -g aws-cdk", # Install the CDK CLI on CodeBuild,
                    "pip install -r requirements.txt", # Instruct CodeBuild to install the required packages
                    "npx cdk synth", # Always end in a synth command. For NPM-based projects this is always `npx cdk synth``.
                ]
            ),
        )