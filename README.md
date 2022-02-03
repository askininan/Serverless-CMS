
# Serverless CMS Project with AWS CDK

The content demonstrates a CDK app with an instance of a stack (`serverless_cms_stack`)
which contains an API Gateway, three Lambda functions (file_service, user_service and post_service),
an RDS database table with preconfigured example data, an S3 bucket and a DynamoDB table. Also two SQS
messaging queues to connect the services together asynchronously (to be added).

Stack-file: serverless_cms/serverless_cms_stack.py
## Building Steps

* `npm install -g aws-cdk`                install aws-cdk

MAC and Linux
 * `source .venv/bin/activate`            activate your virtualenv

Windows
 * `.venv\Scripts\activate.bat`           activate your virtualenv     

After activating virtualenv:
 * `pip install -r requirements.txt`      install requirements into virtualenv 

Deploy

The stack is advised to be deployed at region: `eu-central-1` as there are dependencies to that particular region in the code. Or you may replace it to your preferred region in the code.

 * `cdk bootstrap aws://ACCOUNT-NUMBER-1/REGION-1`       bootstrap cdk with your account and a specific region
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk diff`        compare deployed stack with current state
 * `cdk deploy`      deploy this stack to your default AWS account/region
### Important Note

In order to create and connect RDS DB table: After deploying the stack, it is required to edit the inbound rules of the deployed
security group to allow `port:3306`, Source:`0.0.0.0/0, ::/0` from the console as I wasn't able to figure out the write CDK synthax for it just yet.
Note: Code snippet is commented out for further development.

The example data table can be inserted by executing `sql_add.py` which connects RDS database with Secrets Manager authentication.

S3 and DynamoDB table names need to be changed with the deployed resource names in order to test file_service and post_service.
  
## Project Diagram
Ideal project diagram is visioned as seen below. However, project is still on going as all the resources are not created in code yet, and the diagram may change.

![alt text](https://github.com/askininan/Serverless-CMS/blob/main/architecture%20diagram/CMS_Diagram.drawio.png)


### Parts that are still in on-going phase:
1. Parsing the data from RDS DB through user_service function to API Gateway by GET method
2. Creating GET method for post_service with Client ID filter
3. Creating SQS queues for lambda functions to trigger each other