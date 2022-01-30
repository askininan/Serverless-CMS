from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_s3 as s3,
    aws_sns_subscriptions as subs,
)


class ServerlessCmsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "cms-content-bucket")


        # queue = sqs.Queue(
        #     self, "ServerlessCmsQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # topic = sns.Topic(
        #     self, "ServerlessCmsTopic"
        # )

        # topic.add_subscription(subs.SqsSubscription(queue))
