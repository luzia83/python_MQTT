import paho.mqtt.client as mqtt
import time
import csv
import requests
import json
from datetime import datetime

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_publish(client, userdata, mid):
    print("Published: "+str(mid))

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
#client.tls_set()
client.will_set("bikes/dgm/will","disconnected!") # Use an unique topic
client.connect("broker.mqttdashboard.com", 1883, 60)
client.loop_start()


url = 'http://datosabiertos.malaga.eu/recursos/transporte/EMT/EMTocupestacbici/ocupestacbici.csv'
headers = {'User-Agent': 'myagent'}
response=requests.get(url,headers=headers)
response.encoding='utf-8'
reader = csv.reader(response.text.splitlines(),delimiter=',')
header_row = next(reader)
now = datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M')

for row in reader:
    data = {
        'id': row[0],
        'name': row[1],
        'address': row[3],
        'occupation': row[8],
        'free_places': row[7],
        'latitude': row[9],
        'longitud': row[10]
    }
    json_data = json.dumps(data)

    msg=""
    for i in range(len(row)):
        msg = msg + header_row[i] + ": " + row[i] + "\n"

    print(msg)
    client.publish("bikes/lgt", json_data, qos=0, retain=False)

    time.sleep(1)

client.disconnect()

