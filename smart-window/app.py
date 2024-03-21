from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
import json
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay

from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse, X509


host_name = "smart-window-10422075.azure-devices.net"
device_id = "smart-window-x509"
x509 = X509("./smart-window-x509-cert.pem", "./smart-window-x509-key.pem")

device_client = IoTHubDeviceClient.create_from_x509_certificate(x509, host_name, device_id)

print('Connecting')
device_client.connect()
print('Connected')

adc = ADC()
relay = GroveRelay(5)


def handle_method_request(request):
    print("Direct method received - ", request.name)

    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off()    

    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)

device_client.on_method_request_received = handle_method_request

while True:
    uv = adc.read(0)
    print("UV sunlight intensity:", uv)

    message = Message(json.dumps({ 'uv_intensity': uv }))
    device_client.send_message(message)

    time.sleep(10)