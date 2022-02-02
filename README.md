
# Serverless CMS Project with AWS CDK

The content demonstrates a CDK app with an instance of a stack (`serverless_cms_stack`)
which contains an API Gateway, three Lambda functions (file_service, user_service and post_service),
an RDS database table with preconfigured example data, an S3 bucket and a DynamoDB table. Also two SQS
messaging queues to connect the services together asynchronously (to be added).

The whole stack is written in AWS CDK: Python3, and is advised to be deployed at region: `eu-central-1`
as there are dependencies to that particular region in the code. Or you may replace it to your preferred region in the code.

## Important Prerequsities
In order to create and connect RDS DB table: After deploying the stack, it is required to edit the inbound rules of the deployed
security group to allow `port:3306`, Source:`0.0.0.0/0, ::/0` from the console as I wasn't able to figure out the write CDK synthax for it just yet.
Note: Code snippet is commented out for further development.

The example data table can be inserted by executing `sql_add.py` which connects RDS database automatically with Secrets Manager authentication.

To create the virtualenv it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv manually once the init process completes.

## Building Steps
MAC and Linux
 * `python3 -m venv .venv`                Manually create a virtualenv
 * `source .venv/bin/activate`            Activate your virtualenv

Windows
 * `.venv\Scripts\activate.bat`           Activate your virtualenv     

After activating virtual env:
 * `pip install -r requirements.txt`      Install requirements
  


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

