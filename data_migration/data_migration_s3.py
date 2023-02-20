"""
PERFORMS DATA MIGRATION FROM SHAREPOINT TO AWS S3 BUCKET
"""
import os
import json
import boto3
from office365.sharepoint.files.file import File
from sharepoint_api import Sharepoint



# read json file
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = '\\'.join([ROOT_DIR, 'config.json'])

with open(CONFIG_PATH) as config_file:
    config = json.load(config_file)
    config_sharepoint = config['share_point']
    config_aws = config['aws_bucket']

SHAREPOINT_CLIENTID = config_sharepoint['client_id']
SHAREPOINT_CLIENTSECRET = config_sharepoint['client_secret']
SHAREPOINT_URL = config_sharepoint['url']
SHAREPOINT_FOLDER_PATH = config_sharepoint['folder_path']
SHAREPOINT_SUBFOLDER_PATH = config_sharepoint['subfolder_path']


AWS_ACCESS_KEY_ID = config_aws['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = config_aws['aws_secret_access_key']
BUCKET_NAME = config_aws['bucket_name']
BUCKET_SUBFOLDER = config_aws['bucket_subfolder']


#Calling function to get Sharepoint connection
connect = Sharepoint.get_sharepoint_context_using_app(
                SHAREPOINT_URL,
                SHAREPOINT_CLIENTID,
                SHAREPOINT_CLIENTSECRET)
web = connect.web
connect.load(web)
connect.execute_query()
#Printing the Web Title of Sharepoint Site
print('Connected to SharePoint: ',web.properties['Title'])

#Getting folder details
#Printing list of files from sharepoint folder
folder_details = Sharepoint.sharepoint_folder_details(connect, SHAREPOINT_FOLDER_PATH)
print(folder_details)

#Getting File details
#Printing list of files from sharepoint folder
file_list = Sharepoint.file_details(connect, SHAREPOINT_SUBFOLDER_PATH)
print(file_list)

for files in file_list:
    file_url = SHAREPOINT_SUBFOLDER_PATH + '/' + files
    response = File.open_binary(connect, file_url)
    #print(response)
    session = boto3.Session(
                AWS_ACCESS_KEY_ID,
                AWS_SECRET_ACCESS_KEY    )
    s3 = boto3.client("s3")
    s3 = session.resource('s3')
    result = s3.meta.client.put_object(Body= response.content, Bucket=BUCKET_NAME, Key=BUCKET_SUBFOLDER+'/'+files)
    res = result.get('ResponseMetadata')
    if res.get('HTTPStatusCode') == 200:
        print('Successfully Uploaded %s to Amazon S3 bucket %s / %s' % (files, BUCKET_NAME,BUCKET_SUBFOLDER))
    else:
        print('File Not Uploaded')
        