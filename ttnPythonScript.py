# Get data from TTN Console using Python

import paho.mqtt.client as mqtt
import json
import base64
#----------------------------------------------
#          Configure these values!

APPEUI = ""      #Application EUI
APPID = ""              #Application ID
PSW = ""    #ACCESS KEYS

#-----------------------------------------------

def on_connect(client, userdata, flags, rc):
    client.subscribe('+/devices/+/up'.format(APPEUI))

def on_message(client, userdata, msg):
			j_msg = json.loads(msg.payload.decode('utf-8'))
			dev_eui = j_msg['hardware_serial']
			device = j_msg["dev_id"]
			counter = j_msg["counter"]
			payload_raw = j_msg["payload_raw"]
			payload_fields = j_msg["payload_fields"]
			datetime = j_msg["metadata"]["time"]
			gateways = j_msg["metadata"]["gateways"]
			for gw in gateways:
					gateway_id = gw["gtw_id"]
					rssi = gw["rssi"]
					print(datetime + ", " + device + ", " + str(counter) + ", "+ gateway_id + ", "+ str(rssi) + ", " + str(payload_fields))
			
			    
# set paho.mqtt callback
ttn_client = mqtt.Client()

ttn_client.on_connect = on_connect

ttn_client.on_message = on_message
ttn_client.username_pw_set(APPID, PSW)

#-------------------------------------------------------------------------------------------------------
ttn_client.connect("brazil.thethings.network", 1883, 60)         #configure for server you are using
#-------------------------------------------------------------------------------------------------------
try:
    ttn_client.loop_forever()
except KeyboardInterrupt:
    print('disconnect')
ttn_client.disconnect()
