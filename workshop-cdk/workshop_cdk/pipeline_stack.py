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

        # Import and create an instance of the WorkshopPipelineStage. Later, we might instantiate this stage multiple times
        # (e.g. a separate development/test deployment).
        deploy = WorkshopPipelineStage(self, "Deploy")

        # Add the stage to our pipeline.
        # A Stage in a CDK pipeline represents a set of one or more CDK Stacks that should be deployed together, to a particular environment.
        deploy_stage = pipeline.add_stage(deploy)

        # Add post-deployment steps via deployStage.AddPost(...) from CDK Pipelines.
        # We add two actions to our deployment stage: to test our TableViewer endpoint and our APIGateway endpoint, respectively.
        deploy_stage.add_post(
            pipelines.ShellStep(
                "TestViewerEndpoint",
                env_from_cfn_outputs={
                    "ENDPOINT_URL": deploy.hc_viewer_url # exposed from `cfn_output` of our deploy stage
                },
                commands=["curl -Ssf $ENDPOINT_URL"],
            )
        )
        deploy_stage.add_post(
            pipelines.ShellStep(
                "TestAPIGatewayEndpoint",
                env_from_cfn_outputs={
                    "ENDPOINT_URL": deploy.hc_endpoint # exposed from `cfn_output` of our deploy stage
                },
                commands=[
                    "curl -Ssf $ENDPOINT_URL",
                    "curl -Ssf $ENDPOINT_URL/hello",
                    "curl -Ssf $ENDPOINT_URL/test",
                ],
            )
        )