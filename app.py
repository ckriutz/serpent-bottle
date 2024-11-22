import os
from flask import Flask, render_template
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

app = Flask(__name__)

@app.route("/")
def hello_file():
    # Get the SVG file for the footer.
    img = './static/githubicon.svg'

    # Get the managed identity and keyvault info.
    try:
        # https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python
        keyVaultName = os.environ["KEY_VAULT_NAME"]
        managedIdentityId = os.environ["MANAGED_IDENTITY_ID"]
        kvUri = f"https://{keyVaultName}.vault.azure.net"

        credential = DefaultAzureCredential(managed_identity_client_id=managedIdentityId)
        client = SecretClient(vault_url=kvUri, credential=credential)
        retrieved_secret = client.get_secret("serpent-secret")
        print(retrieved_secret.value)        

        return render_template('hello.html', secret=retrieved_secret.value, img=img)
    except:
        print("no key vault")
        return render_template('hello.html', secret="", img=img)