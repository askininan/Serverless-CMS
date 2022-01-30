import json
import logging
import boto3

def lambda_handler(event, context):
    data = json.loads(event['body'])
    if 'text' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't put content.")

    # Initialize dynamodb boto3 object
    dynamodb = boto3.resource('dynamodb')
    
    # Set dynamodb table name variable from env
    ddbTableName = "content_table"
    table = dynamodb.Table(ddbTableName)

    # write the content to ddb database
    table.put_item(Item=data)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(data)
    }

    return response