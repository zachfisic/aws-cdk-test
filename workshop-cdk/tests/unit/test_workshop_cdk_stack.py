import pytest
from aws_cdk import (
        Stack,
        aws_lambda as _lambda,
        assertions
    )
from workshop_cdk.hit_counter import HitCounter


# Create a test that validates that the table is getting created.
def test_dynamodb_table_created():
    stack = Stack()
    HitCounter(
        stack,
        "HitCounter",
        downstream=_lambda.Function(
            stack,
            "TestFunction",
            runtime=_lambda.Runtime.NODEJS_14_X,
            handler='hello.handler',
            code=_lambda.Code.from_asset('lambda')),
    )
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::DynamoDB::Table", 1)


# Create a test that validates that the table is created with with the two environment variables DOWNSTREAM_FUNCTION_NAME & HITS_TABLE_NAME
def test_lambda_has_env_vars():
    stack = Stack()
    HitCounter(
        stack,
        "HitCounter",
        downstream=_lambda.Function(
            stack,
            "TestFunction",
            runtime=_lambda.Runtime.NODEJS_14_X,
            handler='hello.handler',
            code=_lambda.Code.from_asset('lambda')))
    template = assertions.Template.from_stack(stack)
    
    envCapture = assertions.Capture()
    template.has_resource_properties("AWS::Lambda::Function", {
        "Handler": "hitcount.handler",
        "Environment": envCapture,
    })

    # We won't know what the value of the function_name or table_name will be since the CDK will calculate a hash
    # to append to the end of the name of the constructs, so we use a dummy value for now.
    # Once we run the test it will fail and show us the expected value.
    assert envCapture.as_object() == {
        "Variables": {
            # "DOWNSTREAM_FUNCTION_NAME": {"Ref": "TestFunctionXXXXXX"},
            # "HITS_TABLE_NAME": {"Ref": "HitCounterHitsXXXXXX"},
            "DOWNSTREAM_FUNCTION_NAME": {"Ref": "TestFunction22AD90FC"},
            "HITS_TABLE_NAME": {"Ref": "HitCounterHits079767E5"},
        },
    }


# Create a test to verify that our DynamoDB table is encrypted.
def test_dynamodb_with_encryption():
    stack = Stack()
    HitCounter(
        stack,
        "HitCounter",
        downstream=_lambda.Function(
            stack,
            "TestFunction",
            runtime=_lambda.Runtime.NODEJS_14_X,
            handler='hello.handler',
            code=_lambda.Code.from_asset('lambda')))

    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::DynamoDB::Table", {
        "SSESpecification": {
            "SSEEnabled": True,
        },
    })


# Create a test to validate read_capacity input.
def test_dynamodb_raises():
    stack = Stack()
    with pytest.raises(Exception):
        HitCounter(
            stack,
            "HitCounter",
            downstream=_lambda.Function(
                stack,
                "TestFunction",
                runtime=_lambda.Runtime.NODEJS_14_X,
                handler='hello.handler',
                code=_lambda.Code.from_asset('lambda')
            ),
            read_capacity=1,
        )