from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit
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