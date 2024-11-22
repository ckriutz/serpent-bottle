# serpent-bottle
A Fun Python Flask App!

### What does this Fun Python Flask App do?
Designed to be deployed anywhere, this app includes a dockerfile, and a sample deployment for Kubernetes.

### Getting this to work.
Set two enviroment varaibles:
```
export KEY_VAULT_NAME=<your-unique-keyvault-name>
export MANAGED_IDENTITY_ID=<your-managed-id-client-id>
```

The KEY_VAULT_NAME should be the unique name for the key vault.
The MANAGED_IDENTITY_ID should be the id that has access to the key vault.

🤔 If these values are not supplied, the applicaion will still work. The Key Vault is used to demonstration purposes.

### Creating a secret in the Key Vault
Create a secret called "serpent-secret" and put any phrase or word into the secret. That will be displayed on the webpage.