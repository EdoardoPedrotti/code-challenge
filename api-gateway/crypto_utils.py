from sortedcontainers import SortedDict
from itertools import islice

def get_top_assets(limit, ranking, pricing):
  if ranking == None:
    raise Exception("null ranking dict")
  top_n = SortedDict(islice(ranking.items(), 0, limit))
  
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
