from constructs import Construct
from aws_cdk import (
    Stage
)
from .workshop_cdk_stack import WorkshopCdkStack

class WorkshopPipelineStage(Stage):

    @property
    def hc_endpoint(self):
        return self._hc_endpoint

    @property
    def hc_viewer_url(self):
        return self._hc_viewer_url

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Add a stage to the pipeline that will deploy our application.
        # This will declare a new core.Stage (component of a pipeline), and in that stage instantiate our application stack.
        service = WorkshopCdkStack(self, 'WebService')
    
        # Expose endpoints
        self._hc_enpdoint = service.hc_endpoint
        self._hc_viewer_url = service.hc_viewer_url