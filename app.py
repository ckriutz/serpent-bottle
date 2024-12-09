import os
from flask import Flask, render_template
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import pyodbc

app = Flask(__name__)

# Get the two environment variables.
managedIdentityId = os.environ["MANAGED_IDENTITY_ID"] if os.environ["MANAGED_IDENTITY_ID"] is not None else ""
keyVaultName = os.environ["KEY_VAULT_NAME"] if os.environ["KEY_VAULT_NAME"] is not None else ""
server = os.environ['AZURE_SQL_SERVER'] if os.environ["AZURE_SQL_SERVER"] is not None else ""
port = os.environ['AZURE_SQL_PORT'] if os.environ["AZURE_SQL_SERVER"] is not None else 1433
database = os.environ['AZURE_SQL_DATABASE'] if os.environ["AZURE_SQL_DATABASE"] is not None else ""
authentication = 'ActiveDirectoryMsi' #os.getenv('AZURE_SQL_AUTHENTICATION')  # The value should be 'ActiveDirectoryMsi'
connString = f'Driver={{ODBC Driver 18 for SQL Server}};Server={server},{port};Database={database};Authentication={authentication};Encrypt=yes;'

connString=os.environ['CONN_STRING']
# Goal here is to show 2 differnet activities.
# First, accessing KeyValut and getting back a secret.
# Second is connecting to SQL server and getting back some data.

def get_keyvalut_secret():
    try:
        # https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python
        #keyVaultName = os.environ["KEY_VAULT_NAME"]
        
        kvUri = f"https://{keyVaultName}.vault.azure.net"
        credential = DefaultAzureCredential(managed_identity_client_id=managedIdentityId)
        client = SecretClient(vault_url=kvUri, credential=credential)
        retrieved_secret = client.get_secret("serpent-secret")
        print(retrieved_secret.value)
        return retrieved_secret.value
    except:
        return ""

def get_database_rows():
    try:
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

@app.route("/")
def hello_file():
    # Get the SVG file for the footer.
    img = './static/githubicon.svg'
    retrieved_secret = get_keyvalut_secret()
    retrived_rows = get_database_rows()

    return render_template('hello.html', secret=retrieved_secret, img=img, rows=retrived_rows)