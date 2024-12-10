import os
from flask import Flask, render_template
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError, HttpResponseError
import pyodbc

app = Flask(__name__)

def get_keyvalut_secret():
    try:
        # https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python
        #keyVaultName = os.environ["KEY_VAULT_NAME"]
        managedIdentityId = os.environ["MANAGED_IDENTITY_ID"] if os.environ["MANAGED_IDENTITY_ID"] is not None else ""
        keyVaultName = os.environ["KEY_VAULT_NAME"] if os.environ["KEY_VAULT_NAME"] is not None else ""
        
        kvUri = f"https://{keyVaultName}.vault.azure.net"
        credential = DefaultAzureCredential(managed_identity_client_id=managedIdentityId)
        client = SecretClient(vault_url=kvUri, credential=credential)
        retrieved_secret = client.get_secret("serpent-secret")
        print(retrieved_secret.value)
        return retrieved_secret.value
    except ClientAuthenticationError as auth_error:
        print(f"Error: {auth_error}")
        return "Unable to Connect to Key Vault. ☹️"
    except HttpResponseError as http_error: 
        print(f"HTTP response error: {http_error}")
        return "Unable to Connect to Key Vault. ☹️"
    except Exception as e: 
        print(f"An unexpected error occurred: {e}")
        return "Unable to Connect to Key Vault. ☹️"

def get_database_rows():
    try:
        connString = os.environ['CONN_STRING']
        conn = pyodbc.connect(connString)
        print("Connected to the SQL Server database successfully.")
        # Create a cursor from the connection
        cursor = conn.cursor()
        # Execute a query
        query = "SELECT * FROM Cities"
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
    retrived_rows = get_database_rows()

    return render_template('hello.html', secret=retrieved_secret, img=img, rows=retrived_rows)