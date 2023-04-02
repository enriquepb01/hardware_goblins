'''
Subscribe to both RPi sound sensor data
'''

import paho.mqtt.client as mqtt

import paho.mqtt.client as mqtt
import time


# MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the ultrasonic ranger topic here
    client.subscribe('goblin/test', 2)
    client.message_callback_add('goblin/test', goblin_callback)

#Default message callback.
def on_message(client, userdata, msg):
    pass

def goblin_callback(client, userdata, msg):
    print('Goblin: ' + str(msg.payload, 'utf-8'))


if __name__ == '__main__':
    #starts mqtt connection
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
        print('Waiting for message...')
        



        
        
        