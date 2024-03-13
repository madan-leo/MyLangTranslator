from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

#credential = DefaultAzureCredential(additionally_allowed_tenants=['*'])
#secret_client = SecretClient(vault_url="https://azuretranslationapi.vault.azure.net/", credential=credential)
#secret = secret_client.get_secret(os.environ["OPENAI_API_KEY"]).value
test = os.getenv("AZURE_LOG_TABLE_CONN_STRING")
print(test)
#print(secret.value)