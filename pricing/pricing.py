import os
import time
import requests
import json
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("connected with rc", rc)

def on_message(client, userdata, msg):
    message = "%s %s" % msg.topic, str(msg.payload)

def get_prices():
    url = 'https://api.coinmarketcap.com/v2/ticker/'
    resp = requests.get(url)
    
    data = resp.json()['data']
    numCrypto = resp.json()['metadata']['num_cryptocurrencies']
    currStart = 101
    while currStart < numCrypto:
        url = 'https://api.coinmarketcap.com/v2/ticker?start=%s' % (currStart)
        resp = requests.get(url)
        newData = resp.json()['data']
        data.update(newData)
        currStart += 100
    print(len(data), numCrypto)
    listing = create_listing(data)
    return listing

def create_listing(data):
    toReturn = dict()
    for key, value in data.items():
        key = value['symbol']
        toReturn[key] = value['quotes']['USD']['price']
    return toReturn

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

host = os.getenv('HOST')
port = int(os.getenv('PORT')) 
client.connect(host, port, 60)

oldPrices = dict()

while True:
    print("updating prices")
    prices = get_prices()
    for key, value in prices.items():
        # if not key in oldPrices.keys():
            # oldPrices[key] = value
        # elif oldPrices[key] == value:
            # continue
        topic = "pricing/%s" % key
        client.publish(topic, value, 0)
    time.sleep(5)
client.loop_forever()

