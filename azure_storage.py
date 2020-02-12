import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


# NEVER COMMIT THIS FILE TO GIT, OR GIVE PUBLIC ACCESS IN ANY OTHER WAY
# NOT TO BE USED IN PRODUCTION - DEV & TESTING ONLY
AZURE_CREDENTIALS_FILE = './.azure.key'


def azure_connection_string():
    if 'AZURE_STORAGE_CONNECTION_STRING' in os.environ:
        conn_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    #DEV AND TESTING ONLY
    else:
        if os.path.exists(AZURE_CREDENTIALS_FILE):
            with open(AZURE_CREDENTIALS_FILE, 'r') as file:
                credentials = [x.strip() for x in file.readlines()]
                conn_str = credentials[1]
        else:
            raise ValueError
    return conn_str


def azure_create_container(container_name):
    conn_str = azure_connection_string()
    try:
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    except Exception as e:
        print("Unable to create blob service client: {}".format(e))
    try:
        blob_service_client.create_container(container_name)
    except Exception as e:
        print("Unable to create container: {}".format(e))


def azure_create_blob(container_name, key, value):
    conn_str = azure_connection_string()
    try:
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    except Exception as e:
        print("Unable to create blob service client: {}".format(e))
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=key)
        blob_client.upload_blob(value)
    except Exception as e:
        print("Unable to upload blob: {}".format(e))


def azure_download_blob(container_name, key):
    conn_str = azure_connection_string()
    try:
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    except Exception as e:
        print("Unable to create blob service client: {}".format(e))


def azure_container_blobs(container_name):
    pass

def azure_delete_blob(container_name, key):
    pass

def azure_blob_exists(container_name, key):
    pass

def azure_delete_container(container_name):
    pass
