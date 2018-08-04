import os
import time
import requests
import json
import paho.mqtt.client as mqtt
from flask_mqtt import Mqtt
from flask import Flask
from flask import Response
from flask import request
from werkzeug.contrib.cache import SimpleCache
from sortedcontainers import SortedDict
from itertools import islice
import crypto_utils as cu

app = Flask(__name__)
host = os.getenv('HOST')
port = int(os.getenv('PORT')) 
app.config['MQTT_BROKER_URL'] = host
app.config['MQTT_BROKER_PORT'] = port
mqtt = Mqtt(app)
cache = SimpleCache()




# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect(host, port, 60)
# client.loop_forever()
# app.logger.info("mqtt connected")
test = "sgnep"
@app.route("/")
def price_and_rank():
  limit = int(request.args.get('limit'))
  try:
    if cache.get('pricing') == None:
      return "pricing not yet available"
    toReturn = cu.get_top_assets(limit, cache.get('ranking'), cache.get('pricing'))
    resp = Response(response=json.dumps(toReturn),
                    status=200,
                    mimetype="application/json")
    return resp 
  except Exception as e:
     raise e


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('pricing/#')
    mqtt.subscribe('ranking/#')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):

    topicSplit = message.topic.split("/")
    msgType = topicSplit[0]
    crypto= topicSplit[1]
    value = message.payload.decode() 
    if msgType == 'pricing':
      cu.updatePricing(crypto, value, cache)
    if msgType == 'ranking':
      cu.updateRanking(crypto, value, cache)

def get_top_assets(limit, c):
  ranking = c.get('ranking')
  pricing = c.get('pricing')
  if ranking == None:
    raise Exception("null ranking dict")
  top_n = SortedDict(islice(ranking.items(), 0, limit-1))
  top_assets = []
  for r in top_n:
    asset = dict()
    asset['rank'] = r
   
    asset['symbol'] = ranking[r]

    if ranking[r] in pricing.keys():
        asset['price'] = pricing[ranking[r]]
    else:
        asset['price'] = 'N/A'
    top_assets.append(asset)
  return top_assets

def updatePricing(crypto, price, c):
  prices = c.get('pricing')
  if prices == None:
    prices = dict()
  prices[crypto] = price
  c.set('pricing', prices)

def updateRanking(crypto, rank, c):
  ranking = c.get('ranking')
  if ranking == None:
    ranking = SortedDict()
  rank = int(rank)
  ranking[rank] = crypto
  c.set('ranking', ranking)
