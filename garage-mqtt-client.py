#!/usr/bin/python

import config
import json
import time
import math
from time import mktime
from datetime import datetime
import paho.mqtt.client as mqtt
import pytz
import RPi.GPIO as GPIO

# sleep for 1 minute to ensure we have network connectivity on reboot of the Pi, since this is run as a startup script
# TODO: try to make this BETTER than this ugly hack in the future
time.sleep(60)

# set the GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# define the topics to subscribe to
healthCheckTopic = '/garage/' + config.clientId + '/healthCheck'
doorActionTopic = '/garage/' + config.clientId + '/doorAction'
allTopics = [healthCheckTopic, doorActionTopic]

# hook up and define the pins for the magnetic switch
mag_switch_pin = 17
GPIO.setup(mag_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# hook up and define the pins for the relay
# Using BCM 26 as I'm 100% positive it is always pulled LOW on boot,
# otherwise the relay could fire on boot and open the garage door in a power loss situation
relay_pin = 26
GPIO.setup(relay_pin, GPIO.OUT)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print('Connected with result code: ' + str(rc))
    for topic in allTopics:
        client.subscribe(topic, 0)


# The callback for when a PUBLISH message is received from the server.
def on_message_received(client, userdata, msg):
    print('Message Received - Topic: [' + msg.topic + "] - Payload: [" + msg.payload + "]")

    if not validate_message_timestamp(payload=msg.payload, topic=msg.topic):
        print('Ignoring message as the time difference is too great')
    elif msg.topic == healthCheckTopic:
        handle_health_check_request()
    elif msg.topic == doorActionTopic:
        handle_door_action_request(payload=msg.payload)


# validates local time against message time - if there is more than 5 minutes difference, discard the message
# True return value means we are good.  False return value means we need to discard
def validate_message_timestamp(payload, topic):
    jsonPayload = json.loads(payload)
    messageTimestamp = int(jsonPayload["timestamp"])
    localTimestamp = get_utc_timestamp()
    difference = math.fabs(localTimestamp - messageTimestamp)

    if difference > config.maxMessageSkewTime:
        reply = {'error': 'message ignored as time difference (' + str(difference) + ' seconds) is too great'}
        jsonReply = str(json.dumps(reply))
        client.publish(topic + '/reply', jsonReply, 0, False)
        return False
    else:
        return True


def get_utc_timestamp():
    tz = pytz.timezone("UTC")
    utcNow = tz.localize(datetime.utcnow(), is_dst=None)
    timestamp = (utcNow - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
    return timestamp


def handle_health_check_request():
    doorStatus = garage_door_status()
    reply = {'doorStatus': doorStatus}  # 'open' or 'closed'
    jsonReply = str(json.dumps(reply))
    client.publish(healthCheckTopic + '/reply', jsonReply, 0, False)


def handle_door_action_request(payload):
    jsonPayload = json.loads(payload)
    requestedAction = jsonPayload["action"]

    checkStatus = requestedAction
    if checkStatus == 'close':
        checkStatus = 'closed'

    currentDoorStatus = garage_door_status()
    if checkStatus == currentDoorStatus:
        # user wants to 'open', but garage already is open (or vice versa) - Don't do anything in this case
        reply = {'error': 'requested action (' + str(requestedAction) + ') ignored as door is already in that state'}
        jsonReply = str(json.dumps(reply))
        client.publish(doorActionTopic + '/reply', jsonReply, 0, False)
    else:
        open_close_garage_door()
        reply = {'successful': True}
        jsonReply = str(json.dumps(reply))
        client.publish(doorActionTopic + '/reply', jsonReply, 0, False)
        time.sleep(config.garageActionTime)
        handle_health_check_request()

def garage_door_status():
    if GPIO.input(mag_switch_pin):
        return 'open'
    else:
        return 'closed'


def open_close_garage_door():
    # We can't actually choose "open" or "close".
    # All we can do is toggle the relay to make it the opposite of what it currently is
    GPIO.output(relay_pin, True)
    time.sleep(0.2)
    GPIO.output(relay_pin, False)


client = mqtt.Client(client_id=config.clientId)
client.on_connect = on_connect
client.on_message = on_message_received

client.tls_set(ca_certs=config.caBundlePath, certfile=config.certFilePath, keyfile=config.keyFilePath)
client.username_pw_set(config.username, config.password)
client.connect(config.mqttHost, config.mqttPort, config.mqttKeepAlive)

client.loop_forever()
