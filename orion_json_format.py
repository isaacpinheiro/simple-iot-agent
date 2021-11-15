#!/usr/bin/python
# -*- coding: utf-8 -*-

class OrionJSONFormat:

    def encode_post(self, payload):

        return {
            "id": payload['devEUI'],
            "type": "User",
            "data": {
                "type": "String",
                "value": payload['data']
            }
        }

    def encode_put(self, payload):

        return {
            "type": "String",
            "value": payload['data']
        }

