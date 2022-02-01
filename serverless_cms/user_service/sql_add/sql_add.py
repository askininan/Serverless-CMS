import pymysql
import boto3
import json

region = 'eu-central-1'
db_instance = 'cmsrdsdatabase'


client = boto3.client('secretsmanager')
            
response = client.get_secret_value(
    SecretId='serverlesscmsCMSRDSSecret5B-zEjnIURsujOn'
)

database_secrets = json.loads(response['SecretString'])

cms_password=database_secrets['password']



source = boto3.client('rds', region_name=region)

instances = source.describe_db_instances(DBInstanceIdentifier=db_instance)
rds_host = instances.get('DBInstances')[0].get('Endpoint').get('Address')



connection = pymysql.connect(host=rds_host,
                             user='cmsadmin',
                             password=cms_password,
                            )

cursor = connection.cursor()


cursor.execute("select version()")
data=cursor.fetchone()
print(data)


sql = """CREATE DATABASE IF NOT EXISTS Characters"""
cursor.execute(sql)
cursor.connection.commit()


sql="""use Characters"""
cursor.execute(sql)
sql = """DROP TABLE IF EXISTS Chars"""
cursor.execute(sql)

#creating table Chars
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

sql="""use Characters"""
cursor.execute(sql)

sql="""show tables"""
cursor.execute(sql)
tables=cursor.fetchall()
print(tables)

sql="""insert into Chars(name,surname,location) values ('%s','%s','%s')"""%('Gimli','Son of Gloin','Moria')
cursor.execute(sql)

sql="""insert into Chars(name,surname,location) values ('%s','%s','%s')"""%('Bilbo','Baggins','Shire')
cursor.execute(sql)

sql="""insert into Chars(name,surname,location) values ('%s','%s','%s')"""%('Balrog','Durins Bane','Moria')
cursor.execute(sql)

sql="""insert into Chars(name,surname,location) values ('%s','%s','%s')"""%('Aragorn','Strider','Gondor')
cursor.execute(sql)

sql= """select * from Chars"""
cursor.execute(sql)
allchars=cursor.fetchall()
print(allchars)

sql="""select name from Chars where location = '%s' """%('Moria')
cursor.execute(sql)
charinfo=cursor.fetchall()

print(charinfo)