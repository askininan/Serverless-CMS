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

cursor.execute("select version()")
data=cursor.fetchone()
print(data)

###### CREATE DATABASE ###### 
sql = """CREATE DATABASE IF NOT EXISTS Characters"""
cursor.execute(sql)
cursor.connection.commit()


###### CREATE DATABASE TABLE ###### 
sql="""use Characters"""
cursor.execute(sql)
sql = """DROP TABLE IF EXISTS Chars"""
cursor.execute(sql)


# Insert Chars table schema
sql="""use Characters"""
cursor.execute(sql)

sql="""CREATE TABLE IF NOT EXISTS Chars(
id int not null auto_increment,
name text,
surname text,
location text,
primary key(id)
)"""
cursor.execute(sql)
cursor.connection.commit()

# Show tables to test if the table is created
sql="""use Characters"""
cursor.execute(sql)

sql="""show tables"""
cursor.execute(sql)
tables=cursor.fetchall()
print(tables)


###### INSERT DATA ###### 
# Insert example data to Chars table
sql="""insert into Chars(name,surname,location) values ('%s','%s','%s')"""%('Gimli','Son of Gloin','Moria')
cursor.execute(sql)

sql="""insert into Chars(name,surname,location) values ('%s','%s','%s')"""%('Bilbo','Baggins','Shire')
cursor.execute(sql)

sql="""insert into Chars(name,surname,location) values ('%s','%s','%s')"""%('Balrog','Durins Bane','Moria')
cursor.execute(sql)

sql="""insert into Chars(name,surname,location) values ('%s','%s','%s')"""%('Aragorn','Strider','Gondor')
cursor.execute(sql)

sql="""insert into Chars(name,surname,location) values ('%s','%s','%s')"""%('Frodo','Baggins','Shire')
cursor.execute(sql)


# Print all data in Chars table
sql= """select * from Chars"""
cursor.execute(sql)
allchars=cursor.fetchall()
print(allchars)


#Print data where location is 'Moria'
sql="""select name from Chars where location = '%s' """%('Moria')
cursor.execute(sql)
charinfo=cursor.fetchall()
print(charinfo)