import os
import socket
from flask import Flask, render_template
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError, HttpResponseError
from azure.storage.blob import BlobServiceClient
import msal
import pyodbc

app = Flask(__name__)

def get_keyvalut_secret():
    try:
        # https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python
        managedIdentityId = os.environ["MANAGED_IDENTITY_ID"]
        keyVaultName = os.environ["KEY_VAULT_NAME"]
        
        kvUri = f"https://{keyVaultName}.vault.azure.net"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=kvUri, credential=credential)
        retrieved_secret = client.get_secret("serpent-secret")
        print(retrieved_secret.value)
        return retrieved_secret.value
    except ClientAuthenticationError as auth_error:
        print(f"Error: {auth_error}")
        return "Unable to Connect to Key Vault. Auth Error. ☹️"
    except HttpResponseError as http_error: 
        print(f"HTTP response error: {http_error}")
        return "Unable to Connect to Key Vault. HttpResponseError ☹️"
    except Exception as e: 
        print(f"An unexpected error occurred: {e}")
        return "Unable to Connect to Key Vault. ☹️"

def list_blob_storage_contents_using_connectionstring():
    try:
        connect_str = os.environ['AZURE_STORAGE_CONNECTION_STRING']
        container_name = 'stuff'
        
        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        
        # Get the container client
        container_client = blob_service_client.get_container_client(container_name)
        
        # List the blobs in the container
        blobs = container_client.list_blobs()
        blob_list = [{'name': blob.name, 'url': f'https://storageserpantwestus301.blob.core.windows.net/{container_name}/{blob.name}'} for blob in blobs]
        
        return blob_list
    except Exception as e:
        print(f"A blob error occurred: {e}")
        return "Unable to list blobs in the container. ☹️"

def get_database_rows_using_connectionstring():
    try:
        connString = os.environ['CONN_STRING']
        conn = pyodbc.connect(connString)
        print("Connected to the SQL Server database successfully.")
        # Create a cursor from the connection
        cursor = conn.cursor()
        # Execute a query
        query = "SELECT * FROM Locations"
        cursor.execute(query)
        # Fetch the first result
        first_result = cursor.fetchone() 
        # Check if there is a result and print it
        if first_result: print(first_result)
        else: print("No results found.")
        return first_result
    except pyodbc.Error as e:
        print(f"Error: {e}")
        return "Unable to connent to the database. ☹️"

@app.route("/")
def hello_file():
    # Get the SVG file for the footer.
    img = './static/githubicon.svg'
    retrieved_secret = get_keyvalut_secret()
    retrived_rows = get_database_rows_using_connectionstring()
    retrived_blobs = list_blob_storage_contents_using_connectionstring()

    return render_template('hello.html', secret=retrieved_secret, img=img, rows=retrived_rows, blobs=retrived_blobs)