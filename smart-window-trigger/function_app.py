import json
import os
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()


@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="event-hub-trigger",
                               connection="IOT_HUB_CONNECTION_STRING") 
def event_hub_trigger(azeventhub: func.EventHubEvent):
    # Getting data from the cloud
    body = json.loads(azeventhub.get_body().decode('utf-8'))
    device_id = azeventhub.iothub_metadata['connection-device-id']

    logging.info(f'Received message: {body} from {device_id}')

    uv_intensity = body['uv_intensity']

    # IoT logic
    if uv_intensity <= 800:
        # print("The UV intensity is ok, turning relay on.")  # open the window
        direct_method = CloudToDeviceMethod(method_name='relay_on', payload='{}')
    else:
        # print("The UV intensity is too high, turning relay off.")  # close the window
        direct_method = CloudToDeviceMethod(method_name='relay_off', payload='{}')

    # Connect to Registry Manager
    logging.info(f'Sending direct method request for {direct_method.method_name} for device {device_id}')

    registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
    registry_manager = IoTHubRegistryManager(registry_manager_connection_string)

    # Using Registry Manager to send message to IoT device
    registry_manager.invoke_device_method(device_id, direct_method)

    logging.info('Direct method request sent!')

# Invoke url: https://smart-window-10422075.azurewebsites.net/api/relay_on
@app.route(route="relay_on", auth_level=func.AuthLevel.ANONYMOUS)
def relay_on(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    device_id = os.environ['DEVICE_ID']
    direct_method = CloudToDeviceMethod(method_name='relay_on', payload='{}')
    # Connect to Registry Manager
    logging.info(f'Sending direct method request for {direct_method.method_name} for device {device_id}')

    registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
    registry_manager = IoTHubRegistryManager(registry_manager_connection_string)

    # Using Registry Manager to send message to IoT device (relay)
    registry_manager.invoke_device_method(device_id, direct_method)

    logging.info('Direct method request sent!')

    return func.HttpResponse(f"This HTTP triggered function executed successfully. The relay has been turned on!")

# Invoke url: https://smart-window-10422075.azurewebsites.net/api/relay_off
@app.route(route="relay_off", auth_level=func.AuthLevel.ANONYMOUS)
def relay_off(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    device_id = os.environ['DEVICE_ID']
    direct_method = CloudToDeviceMethod(method_name='relay_off', payload='{}')
    # Connect to Registry Manager
    logging.info(f'Sending direct method request for {direct_method.method_name} for device {device_id}')

    registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
    registry_manager = IoTHubRegistryManager(registry_manager_connection_string)

    # Using Registry Manager to send message to IoT device (relay)
    registry_manager.invoke_device_method(device_id, direct_method)

    logging.info('Direct method request sent!')

    return func.HttpResponse(f"This HTTP triggered function executed successfully. The relay has been turned off!")