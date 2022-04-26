#!/usr/bin/python
# -*- coding: utf-8 -*-

config = {}

config['mqtt_broker'] = '127.0.0.1'
config['mqtt_port'] = 1883
config['mqtt_topic'] = 'application/+/#'
config['mqtt_client_id'] = 'iot-agent-1'
config['topic_regex'] = '^application/[0-9]*/device/[a-zA-Z0-9]*/event/up$'

# MQTT + TLS
config['mqtt_tls'] = False
config['mqtt_ca_cert'] = ''
config['mqtt_tls_cert'] = ''
config['mqtt_tls_key'] = ''
config['mqtt_tls_insecure'] = False # Always use False in production!

# Address from FIWARE Orion or from simple-auth-proxy
config['orion_address'] = '127.0.0.1:1026'
config['https'] = False
config['unverified'] = False # Always use False in production!
config['access_token'] = None

