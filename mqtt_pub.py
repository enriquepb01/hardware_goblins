'''
Publish sound sensor information - RPi 1
'''

import paho.mqtt.client as mqtt
import time
import requests
import sys



def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    # RPi doesn't subscribe to anything



if __name__ == '__main__':
    # connect to MQTT broker
    client = mqtt.Client()
    #client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    # constantly get data and publish it
    while True:
        try:
            goblin = input("Goblin: ")
            client.publish('goblin/test', goblin)
            time.sleep(.1)

        except IOError:
            print ("Error")

        except KeyboardInterrupt:
            # Gracefully shutdown on Ctrl-C
            break