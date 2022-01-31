from ast import Lambda
from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_rds as rds,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_sns_subscriptions as subs,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_ec2 as ec2
)


class ServerlessCmsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        ######### User_Service Stack ######### 
        vpc = ec2.Vpc(
            self, "CMS_vpc",
            cidr="10.0.0.0/16"
        )

        rds.DatabaseInstance(
            self, 
            "CMS_RDS",
            database_name="user_content_sql_database_2022",
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0_23
            ),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            storage_type=rds.StorageType.GP2,
            allocated_storage=20,
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False,
            delete_automated_backups=True,
            vpc=vpc,
            port=3306,
            multi_az=False,
            publicly_accessible=True,
            vpc_subnets={
                "subnet_type": ec2.SubnetType.PUBLIC
            },
            credentials=rds.Credentials.from_generated_secret("cmsadmin")
        )

        ######### Post_Service Stack ######### 

        # Deploy dynamoDB table
        table_ddb = dynamodb.Table(
            self, 
            id="content_table",
            partition_key=dynamodb.Attribute(
                name="id", 
                type=dynamodb.AttributeType.STRING
            )
        )

        # Deploy post_service lambda function
        post_function = lambda_.Function(
            self, 
            id="post_service",
            code=lambda_.Code.from_asset("./serverless_cms/post_service/"),
            handler="post_service.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
        )

        # Grant permission to post_funtion to write ddb table
        table_ddb.grant(post_function, "dynamodb:PutItem")


        # Deploy ApiGW
        api = apigw.RestApi(self, "CMS-API")

        post_service_apiResource = api.root.add_resource("post_service_apiResource")


        #Post_service lambda function and APIGW integration
        post_content_integration = apigw.LambdaIntegration(post_function)
        post_service_apiResource.add_method("POST", post_content_integration)



        ######### File_Service Stack ######### 

        # Deploy s3 bucket
        bucket = s3.Bucket(self, "cms-content-bucket")

        # Deploy file_service lambda function
        file_function = lambda_.Function(
            self, 
            id="file_service",
            code=lambda_.Code.from_asset("./serverless_cms/file_service/"),
            handler="file_service.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
        )

        # Grant permission to file_funtion to write onto s3
        bucket.grant_read_write(file_function)

        # Add a new resource to our existing APIGW
        file_service_apiResource = api.root.add_resource("file_service_apiResource")

        # File_service lambda function and APIGW integration
        file_content_integration = apigw.LambdaIntegration(file_function)
        file_service_apiResource.add_method("POST", file_content_integration)










        # queue = sqs.Queue(
        #     self, "ServerlessCmsQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # topic = sns.Topic(
        #     self, "ServerlessCmsTopic"
        # )

        # topic.add_subscription(subs.SqsSubscription(queue))
