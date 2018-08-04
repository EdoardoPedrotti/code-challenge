import falcon

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("connected with rc", rc)
    client.subscribe("pricing/#")
    client.subscribe("ranking/#")

message = ""
def on_message(client, userdata, msg):
    message = msg 
    app.logger.info(msg)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


class QuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': (
                "I've always been more interested in "
                "the future than in the past."
            ),
            'author': 'Grace Hopper'
        }

        resp.media = quote

api = falcon.API()
api.add_route('/quote', QuoteResource())

client.connect('localhost', 1883, 60)
client.loop_forever()
