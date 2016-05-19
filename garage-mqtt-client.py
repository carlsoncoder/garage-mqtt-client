#!/usr/bin/python

import paho.mqtt.client as mqtt
import json
import config

# define the topics to subscribe to
healthCheckTopic = '/garage/' + config.clientId + '/healthCheck'
doorStatusTopic = '/garage/' + config.clientId + '/doorStatus'
doorActionTopic = '/garage/' + config.clientId + '/doorAction'
allTopics = [healthCheckTopic, doorStatusTopic, doorActionTopic]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print('Connected with result code: ' + str(rc))
    for topic in allTopics:
        client.subscribe(topic, 0)

# The callback for when a PUBLISH message is received from the server.
def on_message_received(client, userdata, msg):
    print('Message Received:')
    print(msg.topic + " - " + msg.payload)

    if (msg.topic == healthCheckTopic):
        handle_health_check()
    elif (msg.topic == doorStatusTopic):
        handle_door_status()
    elif (msg.topic == doorActionTopic):
        handle_door_action(payload=msg.payload)

def handle_health_check():
    print 'handle_health_check'
    reply = {'IsAvailable': True}
    jsonReply = str(json.dumps(reply))
    client.publish(healthCheckTopic + '/reply', jsonReply, 0, False)

def handle_door_status():
    print 'handle_door_status'
    reply = {'doorStatus': 'open'}  # 'open' or 'closed'
    jsonReply = str(json.dumps(reply))
    client.publish(doorStatusTopic + '/reply', jsonReply, 0, False)

def handle_door_action(payload):
    print 'handle_door_action'
    jsonPayload = json.loads(payload)
    shouldOpen = False
    if (jsonPayload["action"] == 'open'):
        shouldOpen = True

    reply = {'doorStatus': 'open'}  # 'open' or 'closed'
    jsonReply = str(json.dumps(reply))
    client.publish(doorActionTopic + '/reply', jsonReply, 0, False)


client = mqtt.Client(client_id=config.clientId)
client.on_connect = on_connect
client.on_message = on_message_received

client.tls_set(ca_certs=config.caBundlePath, certfile=config.certFilePath, keyfile=config.keyFilePath)
client.username_pw_set(config.username, config.password)
client.connect(config.mqttHost, config.mqttPort, config.mqttKeepAlive)

client.loop_forever()
