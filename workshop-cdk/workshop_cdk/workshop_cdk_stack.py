from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw
)
from .hit_counter import HitCounter
from cdk_dynamo_table_view import TableViewer


class WorkshopCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_lambda = _lambda.Function(
            self,
            'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler'
        )

        hello_with_counter = HitCounter(
            self,
            'HelloHitCounter',
            downstream=my_lambda
        )

        # API Gateway will route the request to the hit counter handler, which will log the hit and relay it over to the `my_lambda` function. Then, the responses will be relayed back in the reverse order all the way to the user.
        apigw.LambdaRestApi(
            self,
            'Endpoint',
            handler=hello_with_counter._handler
        )

        # We want to somehow access the DynamoDB table behind our hit counter.
        # However, the current API of our hit counter doesn’t expose the table as a public member.
        TableViewer(
            self,
            'ViewHitCounter',
            title='Hello Hits',
            table=hello_with_counter.table
        )