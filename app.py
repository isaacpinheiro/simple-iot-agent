#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import http.client
import json
import re

from orion_json_format import OrionJSONFormat

# MQTT
broker = '127.0.0.1'
port = 1883
topic = 'application/+/#'
client_id = 'python-mqtt-1'

# HTTP
header = {'Content-type': 'application/json'}

def connect_mqtt() -> mqtt:

    def on_connect(client, userdata, flags, rc):

        if rc == 0:
            print('Connected to MQTT Broker!')
        else:
            print('Failed to connect, return code %d\n', rc)

    client = mqtt.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt):

    def on_message(client, userdata, msg):

        if re.match('^application/[0-9]*/device/[a-zA-Z0-9]*/event/up$', msg.topic) != None:

            payload = json.loads(msg.payload.decode())
            ojf = OrionJSONFormat()
            http_conn = http.client.HTTPConnection('127.0.0.1:1026')

            http_conn.request('GET', '/v2/entities/' + payload['devEUI'])
            res = json.loads(http_conn.getresponse().read().decode())

            if res.get('error') != None and res.get('error') == 'NotFound':
                body = json.dumps(ojf.encode_post(payload))
                http_conn.request('POST', '/v2/entities', body, header)
            else:
                body = json.dumps(ojf.encode_put(payload))
                http_conn.request('PUT', '/v2/entities/' + payload['devEUI'] + '/attrs/data', body, header)

            http_conn.close()

    client.subscribe(topic)
    client.on_message = on_message

if __name__ == '__main__':
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


