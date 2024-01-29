from azure.storage.blob import BlobServiceClient

class AzureStorageService:
    def __init__(self, connection_string):
        self.connectionstring = connection_string
        self.results = []

    def save_to_blob(self, df, blob_name, container_name):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        df.write_csv(blob_name)
        with open(blob_name, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)