from azure.data.tables import TableServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions
from datetime import datetime
import uuid

# Connect to Azure table using SAS URL
def connect_azure_table():
    with TableServiceClient(endpoint="https://mjstorageaccount1980.table.core.windows.net/translationaudit?sp=rau&st=2024-02-16T19:20:30Z&se=2025-02-17T19:20:00Z&spr=https&sv=2022-11-02&sig=yBPUue9%2BvCc9XuBjRwky1O%2BUU9fiDL5KLOEbaIsy%2BiU%3D&tn=translationaudit") as table_service_client:
    #with TableServiceClient(endpoint="https://adlgetdatadev001.table.core.windows.net/TranslationLogs?sp=rau&st=2024-03-06T22:17:59Z&se=2032-01-07T22:17:00Z&spr=https&sv=2022-11-02&sig=qU7SBH%2BkoeLO6xgYJUqUo1CXu4ZJ6qGTk%2BIzENvD4gE%3D&tn=TranslationLogs") as table_service_client:
        properties = table_service_client.get_table_client("TranslationLogs")
        return properties

# Create Entity/Row in the table
def create_entity(Partition, User, FromLang, ToLang, FromText, ToText, FromDoc, ToDoc):
    now = datetime.now()
    my_entity = {
        'PartitionKey': Partition,
        #'RowKey': now.strftime("%m/%d/%Y, %H:%M:%S").replace("/","").replace(":","").replace(", ",""),
        'RowKey' : str(uuid.uuid4()),
        'FromLang': FromLang,
        'ToLang': ToLang,
        'FromText': FromText,
        'ToText': ToText,
        'FromDoc': FromDoc,
        'ToDoc': ToDoc,
        'User': User
    }
    table_service_client = TableServiceClient(endpoint="https://mjstorageaccount1980.table.core.windows.net/translationaudit?sp=rau&st=2024-02-16T19:20:30Z&se=2025-02-17T19:20:00Z&spr=https&sv=2022-11-02&sig=yBPUue9%2BvCc9XuBjRwky1O%2BUU9fiDL5KLOEbaIsy%2BiU%3D&tn=translationaudit")
    table_client = table_service_client.get_table_client(table_name="translationaudit")
    entity = table_client.create_entity(entity=my_entity)
    return entity