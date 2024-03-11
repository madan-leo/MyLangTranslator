import requests, uuid
import os

# Call Text translation api by passing Key and end point
def texttranslator_api (input_text, Tolanguage):
    # Add your key and endpoint
    key = "85c9f8217fbc4f60ae40e47c021d6a34"
    endpoint = "https://api.cognitive.microsofttranslator.com"
    location = "eastus"
    path = '/translate'
    constructed_url = endpoint + path
    params = {
        'api-version': '3.0',
        'from': '',
        'to': Tolanguage
    }
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    # You can pass more than one object in body.
    body = [{
        'text': input_text
    }]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    return response

# call Document translation api by passing end point and key. It's a asynchronous batch operation
def doctranslation_api(filename, tolang):
    import requests, json
    endpoint = "https://mjbingtranslator.cognitiveservices.azure.com/translator/text/batch/v1.1"
    key = "92a99bc2cce845898e6574f3497a59cb"
    path = "/batches"
    constructed_url = endpoint + path
    source_container = "https://mjstorageaccount1980.blob.core.windows.net/original-files/"
    payload = {
        "inputs": [
            {
                "source": {
                   # Specifu source container and file name where the blob is picked from for translation
                    "sourceUrl": source_container + filename,
                    "storageSource": "AzureBlob"
                },
                "targets": [
                    {
                        # Specify target container and file name where the translated blob is stored
                        "targetUrl": "https://mjstorageaccount1980.blob.core.windows.net/translated-files?sp=racwl&st=2024-02-14T21:06:41Z&se=2025-02-15T05:06:41Z&sv=2022-11-02&sr=c&sig=Awnui3pBx8YZG8KwsEHC%2B4ewg%2BhEXgVqgjIg5Th0y%2FM%3D",
                        "storageSource": "AzureBlob",
                        "language": tolang
                    }
                ],
                # pass 'File' if it's a single file, other options are folder if you want whole folder to be translated
                "storageType": "File",
            }
        ]
    }
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }
    response = requests.post(constructed_url, headers=headers, json=payload)
    return response

# function to upload a blob file to a container: This code is not being used, its embedded in app.py
def upload_blob_file(self, blob_service_client, container_name):
    container_client = blob_service_client.get_container_client(self,container="original-files")
    with self as data:
        blob_client = container_client.upload_blob(name=self.name, data=data, overwrite=True)
    return blob_client

# function to download a blob file from a container: This code is not being used, its' embedded in app.py
def downloadfile(self, blob_service_client, filename):
    blob_client = blob_service_client.get_blob_client(container="translated-files", blob=filename)
    with open(file=os.path.join(r'filepath', 'filename'), mode="wb") as sample_blob:
        download_stream = blob_client.download_blob()
        sample_blob.write(download_stream.readall())