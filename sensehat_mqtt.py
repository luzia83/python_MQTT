# Sense HAT with MQTT

from sense_emu import SenseHat
import paho.mqtt.client as mqtt
import json
import datetime
import time

blue = (0, 0, 255)
yellow = (255, 255, 0)

period=1

pru=dict()
pru = json.loads("{\"period\": 9}")
print("despues")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    client.subscribe("sensehat/dgm/commands")

# The callback for when a PUBLISH message is received from the server.
def on_publish(client, userdata, mid):
    print("Published: "+str(mid))

def on_message(unused_client, unused_userdata, message):
    payload = str(message.payload,"utf-8")

    print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, message.topic, str(message.qos)))

    global period
    try:
      dict_command = json.loads(payload)
    except Exception as ex:
      print(str(ex))
    period = int(dict_command.get('period', '1'))
    print('New period: '+str(period))
    sense.show_message(str(period), text_colour=yellow, back_colour=blue, scroll_speed=0.2)


sense = SenseHat()

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()


while True:
    msg=dict()
    msg['temperature']=sense.temperature
    msg['humidity']=sense.humidity
    msg['pressure']=sense.pressure
    msg['when']=datetime.datetime.now()  
    json_data=json.dumps(msg,default=str)
  
    client.publish("sensehat/dgm", json_data, qos=0, retain=False)
    print('Period '+str(period))
    time.sleep(period)
