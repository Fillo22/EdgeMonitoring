import asyncio
import sys
import signal
import threading
from azure.iot.device import IoTHubModuleClient
import os
from services.checks import ConnectivityChecker
from services.storage import AzureStorageService
import json


# Event indicating client stop
stop_event = threading.Event()
storage_service = AzureStorageService(os.environ.get("AZURE_STORAGE_CONNECTION_STRING"))



def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()

    async def receive_message_handler(message):
        if message.input_name == "monitoring":
            print("the data in the message received on input1 was ")
            print(message.data)
            print("custom properties are")
            print(message.custom_properties)
            print("forwarding mesage to output1")
            await client.send_message_to_output(message, "monitored")

    try:
        client.on_message_received = receive_message_handler
    except:
        client.shutdown()
        raise

    return client


async def run_sample(client):
    while True:
        tasks_json = os.environ.get("TASKS_JSON")
        if not tasks_json:
            raise Exception("TASKS_JSON environment variable not found")

        tasks = json.loads(tasks_json)
        checker = ConnectivityChecker(tasks)
        checker.check_connectivity()
        df = checker.to_polars_df()

        connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.environ.get("AZURE_STORAGE_CONTAINER_NAME")
        blob_name = "connectivity_results.csv"

        if not all([connection_string, container_name]):
            raise Exception("Azure storage connection information not found in environment variables")

        storage_service.save_to_blob(df,blob_name,container_name)
        await asyncio.sleep(1000)


def main():
    if not sys.version >= "3.5.3":
        raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
    print ( "IoT Hub Client for Python" )

    # NOTE: Client is implicitly connected due to the handler being set on it
    client = create_client()

    # Define a handler to cleanup when module is is terminated by Edge
    def module_termination_handler(signal, frame):
        print ("IoTHubClient sample stopped by Edge")
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    # Run the sample
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_sample(client))
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        print("Shutting down IoT Hub Client...")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == "__main__":
    main()
