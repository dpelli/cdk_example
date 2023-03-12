from constructs import Construct
from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_logs,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)
from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion

from cdk_workshop import constants


class CdkWorkshopStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.common_layer = self._build_common_layer()
        self.rest_api = self._build_api_gw()
        api_resource: apigw.Resource = self.rest_api.root.add_resource("items")
        self._add_post_lambda_integration(api_resource)

    def _build_api_gw(self) -> apigw.RestApi:
        rest_api: apigw.RestApi = apigw.RestApi(
            self,
            "service-rest-api",
            rest_api_name="Service Rest API",
            deploy_options=apigw.StageOptions(
                throttling_rate_limit=2, throttling_burst_limit=10
            ),
        )

        return rest_api

    def _build_common_layer(self) -> PythonLayerVersion:
        return PythonLayerVersion(
            self,
            "CommonLayer",
            entry="lambda",
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
            removal_policy=RemovalPolicy.DESTROY,
        )

    def _add_post_lambda_integration(self, api_name: apigw.Resource):

        lambda_function = _lambda.Function(
            self,
            "HelloHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda", exclude=["pyproject.toml", "poetry.lock"]),
            handler="hello.handler",
            retry_attempts=0,
            timeout=Duration.seconds(constants.API_HANDLER_LAMBDA_TIMEOUT),
            memory_size=constants.API_HANDLER_LAMBDA_MEMORY_SIZE,
            layers=[self.common_layer],
            log_retention=aws_logs.RetentionDays.ONE_DAY,
        )

        # POST /items/
        api_name.add_method(
            http_method="POST",
            integration=apigw.LambdaIntegration(handler=lambda_function),
        )

        # GET /items/
        api_name.add_method(
            http_method="GET",
            integration=apigw.LambdaIntegration(handler=lambda_function),
        )
