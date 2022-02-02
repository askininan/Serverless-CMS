import json
import aws_cdk
from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    SecretValue,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_rds as rds,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_ec2 as ec2,
    aws_secretsmanager as secretsmanager,
)


class ServerlessCmsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


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



        ######### User_Service Stack ######### 

        # Deploy custom VPC
        vpc = ec2.Vpc(
            self, "CMS_vpc",
            cidr="10.0.0.0/16"
        )

        ##### ERROR: jsii.errors.JSIIError: Expected array type, got {"$jsii.byref":"aws-cdk-lib.aws_ec2.SecurityGroup@10003"} #####

        # Deploy custom security group that allows all traffic inbound
        # securitygroup = ec2.SecurityGroup(
        #     self,
        #     id="sg1",
        #     vpc=vpc,
        #     allow_all_outbound=True,
        #     description="CDK manually created Security Group"
        # )
        # securitygroup.add_ingress_rule(
        #     peer=ec2.Peer.any_ipv4(),
        #     connection=ec2.Port.all_traffic(),
        # )


        rds_db=rds.DatabaseInstance(
            self, 
            "CMS_RDS",
            instance_identifier="cmsrdsdatabase2022",
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
            # security_groups=securitygroup,
            credentials=rds.Credentials.from_generated_secret("admin",
                secret_name="rdsdatabasesecret"
            )
        )





        # Creating a policy for lambda role to access Secret's Manager secrets
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": ["*"],
                    "Resource": ["*"]
                }
            ]
        }
        custom_policy_document = iam.PolicyDocument.from_json(policy_document)

        secrets_man_policy = iam.Policy(self, "Secrets Manager Access Policy",
        document=custom_policy_document
        )

        # Create a role for lambda and attach secrets policy to it
        vpc_exec_role = iam.Role(self, "VPC Execution Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )   
        secrets_man_policy.attach_to_role(vpc_exec_role)

         # Attach required AWS Managed Policies for user_service lambda functions to vpc_exec_role
        vpc_exec_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))
        vpc_exec_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))


        # Deploy user_service lambda function
        user_function = lambda_.Function(
            self, 
            id="user_service",
            code=lambda_.Code.from_asset("./serverless_cms/user_service/user_service.zip"),
            timeout=aws_cdk.Duration.seconds(300),
            handler="user_service.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            role=vpc_exec_role
        )
        


       

        # Add a new resource to our existing APIGW
        user_service_apiResource = api.root.add_resource("user_service_apiResource")

        # File_service lambda function and APIGW integration
        user_content_integration = apigw.LambdaIntegration(user_function)
        user_service_apiResource.add_method("GET", user_content_integration)



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
