import pymysql
import boto3
import json

region = "eu-central-1"
db_instance = "cmsrdsdatabase2022"


client = boto3.client("secretsmanager")
source = boto3.client("rds", region_name=region)

# Get generated password from Secrets Manager      
secret_pass = client.get_secret_value(
    SecretId="rdsdatabasesecret"
)
database_secrets = json.loads(secret_pass["SecretString"])
cms_password=database_secrets["password"]


# Get RDS instance endpoint
instances = source.describe_db_instances(DBInstanceIdentifier=db_instance)
rds_host = instances.get("DBInstances")[0].get("Endpoint").get("Address")


# Connect to RDS db instance
connection = pymysql.connect(host=rds_host,
                             user='admin',
                             password=cms_password,
                            )

cursor = connection.cursor()

# Test connection by fetching db instance version
cursor.execute("select version()")
data=cursor.fetchone()
print(data)



def lambda_handler():

    cursor.execute('Select * from ')
    sql= """select * from Chars"""
    cursor.execute(sql)

    rows = cursor.fetchall()

    for row in rows:
        print("{0} {1} {2}".format(row[0], row[1], row[2]))

lambda_handler()