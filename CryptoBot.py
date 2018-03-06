# -- coding: utf-8 --

import hashlib
import hmac
import httplib
import json
import urllib

from collections import OrderedDict

while True:
	# Constantes
	MB_TAPI_ID = 'KKKKKKKKKKKKKKKKK'
	MB_TAPI_SECRET = 'KKKKKKKKKKKKK'
	REQUEST_HOST = 'www.mercadobitcoin.net'
	REQUEST_PATH = '/tapi/v3/'

	# Nonce
	#Para obter variação de forma simples
	#timestamp pode ser utilizado:
	import time
	tapi_nonce = str(int(time.time()))
	# tapi_nonce = 8

	# Parâmetros
	params = {
		'tapi_method': 'list_orderbook',
		'tapi_nonce': tapi_nonce,
		'coin_pair': 'BRLBTC',
		'full' : 'false'
	}
	params = urllib.urlencode(params)

	# Gerar MAC
	params_string = REQUEST_PATH + '?' + params
	H = hmac.new(MB_TAPI_SECRET, digestmod=hashlib.sha512)
	H.update(params_string)
	tapi_mac = H.hexdigest()

	# Gerar cabeçalho da requisição
	headers = {
		'Content-type': 'application/x-www-form-urlencoded',
		'TAPI-ID': MB_TAPI_ID,
		'TAPI-MAC': tapi_mac
	}

	# Realizar requisição POST
	try:
		conn = httplib.HTTPSConnection(REQUEST_HOST)
		conn.request("POST", REQUEST_PATH, params, headers)
		valores_asks = []
		valores_bids = []
		soma_asks = 0.0
		soma_bids = 0.0
		time.sleep(1)
		for i in range(20):
		   valores_asks.append(0)

		for j in range(20):
		   valores_bids.append(0)
		
		# Print response data to console
		response = conn.getresponse()
		response = response.read()

		# É fundamental utilizar a classe OrderedDict para preservar a ordem dos elementos
		response_json = json.loads(response, object_pairs_hook=OrderedDict)
		address = response_json
		print( ' ')
		print( "************ status: {}".format(response_json['status_code']) + " *************")
		print( " ")
		with open('data.json', 'w') as outfile:
			json.dump(address, outfile, indent = 4)
		print( "Asks:                     Bids:")
		for x in range(0, 20):
			print( response_json['response_data']['orderbook']['asks'][x]['limit_price'] + "               " + response_json['response_data']['orderbook']['bids'][x]['limit_price'] )
		for x in range(0, 20):
			 valores_asks[x] = response_json['response_data']['orderbook']['asks'][x]['limit_price']
			 soma_asks = soma_asks + float (valores_asks[x])
		media_asks = soma_asks/20
		for x in range(0, 20):
			 valores_bids[x] = response_json['response_data']['orderbook']['bids'][x]['limit_price']
			 soma_bids = soma_bids + float (valores_bids[x])
		media_bids = soma_bids/20
		print( 'Ask medio:                Bid Medio:')
		print( str(media_asks) + "               " + str(media_bids))
	except:
		print( "Erro, status = %s" % response_json['status_code'])
	finally:
		if conn:
			conn.close()
