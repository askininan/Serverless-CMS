import json
import boto3

def lambda_handler(event, context):
    data = json.loads(event['body'])
    
    # Initialize dynamodb boto3 object
    dynamodb = boto3.resource('dynamodb')
    
    # Set dynamodb table name variable from env
    ddbTableName = "serverless-cms-contenttableB601D8ED-1UON8P7Y5402O"
    table = dynamodb.Table(ddbTableName)

    # write the content to ddb database
    table.put_item(Item=data)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(data)
    }

    return response