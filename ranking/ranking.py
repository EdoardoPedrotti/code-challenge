import os
import time
import requests
import json
import paho.mqtt.client as mqtt

print("starting ranking service")

def on_connect(client, userdata, flags, rc):
    print("connected, rc:", rc)

def on_message(client, userdata, msg):
    message = "%s %s" % msg.topci, str(msg.payload)

def get_ranking():
    url = 'https://www.cryptocompare.com/api/data/coinlist/'
    resp = requests.get(url)
    data = resp.json()["Data"]
    sortedCrypto = sorted(data.items(), key = lambda v: int(v[1]['SortOrder']))
    return clean_list(sortedCrypto)

def clean_list(cryptoList):
    toReturn = []
    for c in cryptoList:
        toReturn.append((c[0],c[1]['SortOrder']))
    return toReturn

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

host = os.getenv('HOST')
port = int(os.getenv('PORT') ) 
client.connect(host, port, 60)

oldRanking = dict()
while True:
    rankings = get_ranking()
    print("publishing ranking")
    for r in  rankings:
        if not r[0] in oldRanking.keys():
            oldRanking[r[0]] = r[1]
        elif oldRanking[r[0]] == r[1]:
            continue
        topic = 'ranking/%s' % r[0]
        client.publish(topic, r[1],0)
    time.sleep(5)
client.loop_forever()
