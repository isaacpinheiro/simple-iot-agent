#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import http.client
import ssl
import json
import re

from config import config
from orion_json_format import OrionJSONFormat

# HTTP
header1 = {}
header2 = { 'Content-type': 'application/json' }

if config['access_token'] != None and config['access_token'] != '':
    header1['Authorization'] = 'Bearer ' + config['access_token']
    header2['Authorization'] = 'Bearer ' + config['access_token']

def connect_mqtt() -> mqtt:

    def on_connect(client, userdata, flags, rc):

        if rc == 0:
            print('Connected to MQTT Broker!')
        else:
            print('Failed to connect, return code %d\n', rc)

    client = mqtt.Client(config['mqtt_client_id'])
    #client.username_pw_set(username, password)
    client.on_connect = on_connect

    if config['mqtt_tls'] == True:
        client.tls_set(config['mqtt_ca_cert'], certfile = config['mqtt_tls_cert'], keyfile = config['mqtt_tls_key'])
        client.tls_insecure_set(config['mqtt_tls_insecure'])

    client.connect(config['mqtt_broker'], config['mqtt_port'])
    return client

def subscribe(client: mqtt):

    def on_message(client, userdata, msg):

        if re.match(config['topic_regex'], msg.topic) != None:

            payload = json.loads(msg.payload.decode())
            ojf = OrionJSONFormat()
            http_conn = None

            if config['https'] == True and config['unverified'] == True:

                http_conn = http.client.HTTPSConnection(config['orion_address'], context = ssl._create_unverified_context())

            elif config['https'] == True and config['unverified'] == False:

                http_conn = http.client.HTTPSConnection(config['orion_address'])

            else:

                http_conn = http.client.HTTPConnection(config['orion_address'])

            http_conn.request('GET', '/v2/entities/' + payload['devEUI'], headers=header1)
            res = json.loads(http_conn.getresponse().read().decode())

            if res.get('error') != None and res.get('error') == 'NotFound':
                body = json.dumps(ojf.encode_post(payload))
                http_conn.request('POST', '/v2/entities', body, header2)
            else:
                body = json.dumps(ojf.encode_put(payload))
                http_conn.request('PUT', '/v2/entities/' + payload['devEUI'] + '/attrs/data', body, header2)

            http_conn.close()

    client.subscribe(config['mqtt_topic'])
    client.on_message = on_message

if __name__ == '__main__':
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


