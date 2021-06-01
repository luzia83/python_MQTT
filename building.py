# Building simulation system using MQTT

import csv
import paho.mqtt.client as mqtt
from time import sleep
from datetime import datetime
from random import random
from random import seed
import json
import time

dict_sensor=dict()
dict_ac=dict()

STRUCTURE_FILENAME = 'structure.csv'

def load_structure(filename=STRUCTURE_FILENAME):
    """ Load a static structure for an IoT deployment """

    with open(filename) as f:
        reader = csv.reader(f)

        for row in reader:
            structure_entry = {}
            structure_entry['floorID'] = row[1]
            structure_entry['roomID'] = row[2]
  
            if row[3] == 's':   # Sensor
                dict_sensor[row[0]] = structure_entry
            elif row[3] == 'a': # Actuator
                dict_ac[row[0]] = structure_entry


def on_connect(client, userdata, flags, rc):
    """The callback for when the client receives a CONNACK response from the server."""
    print("MQTT Connected with result code " + str(rc))
    if rc == 0:
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
        topic = "building/dgm/command"
        client.subscribe(topic, qos=2)
        print("MQTT Subscribed to " + topic)
           

def on_message(client, userdata, msg):
    """ The callback for when messages (commands) are received from the server. """
    print(msg.topic + " " + str(msg.payload))
    send_command(str(msg.payload.decode("utf-8")))


def send_command(command):
    """Send a command to a specific actuator"""

    try:
        dict_command = json.loads(command)
    except Exception as e:
        print(e)
        return
    default = ""
    scommand = dict_command.get('command', default)

    print("Processing: "+scommand)
    if scommand == 'ON' or scommand == 'OFF':
            id = str(dict_command.get('id', default))

            if not id in dict_ac:
                print("MQTT Unknown Actuator: " + id)
                return
            else:
                print("Actuator id: " + id)
                structure = dict_ac[id]
                structure['status']=scommand
   



def send_measurement(id):
    structure_entry=dict_sensor[id]

    measurement=dict()
    measurement['id']=id
    measurement['floorID'] = structure_entry['floorID']
    measurement['roomID'] = structure_entry['roomID']
    measurement['timestamp'] = datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M')
    measurement['temperature'] = 10.0+random()*10.0
 
    measurement_json = json.dumps(measurement)
    topic = "building/dgm/measurement"    
    client.publish(topic, measurement_json, qos=2)
    print(measurement_json)
    
if __name__ == "__main__":
    load_structure()
    print(dict_sensor)
    print(dict_ac)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("broker.hivemq.com", 1883, 60)
    client.loop_start()

    seed()
    while 1:
        for id in dict_sensor:
            send_measurement(id)
        print(dict_ac)
        sleep(10)
