import base64
import boto3
import json

response  = {
    'statusCode': 200,
    'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    },
    'body': ''
}

def lambda_handler(event, context):

    file_name = event['headers']['file-name']
    print(file_name)
    print (base64.b64decode(event['body']))
    
    file_content = base64.b64decode(event['body'])
    
    # Initialize s3 boto3 object
    s3 = boto3.resource('s3')
    
    # Set s3 table name variable
    BucketName = "serverless-cms-cmscontentbucket2170626e-1l96779yr71sn"
    bucket = s3.Bucket(BucketName)

    try:
        s3_response = bucket.put_object(Bucket=BucketName, Key=file_name, Body=file_content)   

        response['body'] = 'Your file has been uploaded'

        return response

    except Exception as e:
        raise IOError(e)  