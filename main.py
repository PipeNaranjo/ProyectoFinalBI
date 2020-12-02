


import requests
import os
import json
import boto3


access_key = ''
secret_access_key = ''
nombre_bucket = 'bucket-limpio'

client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)

url = 'https://pokeapi.co/api/v2/'
dir = '/home/ubuntu/PokeApi/'

endpoints = ['berry', 'berry-firmness', 'berry-flavor','contest-type','contest-effect','super-contest-effect','encounter-method','encounter-condition','encounter-condition-value',
             'evolution-chain','evolution-trigger','generation','pokedex','version','version-group','item','item-category','item-fling-effect',
             'item-pocket','location','location-area','pal-park-area','region','machine','move','move-ailment','move-category','move-learn-method',
             'move-target','ability','characteristic','egg-group','gender','growth-rate','nature','pokeathlon-stat','pokemon','pokemon-color','pokemon-form',
             'pokemon-habitat','pokemon-shape','stat','type']

def cargarEndpoint(endpoint,dir1,url2):
	respone = requests.get(url2)
	cantidad = respone.json()['count']
	res = requests.get(url2 + '?limit' + str(cantidad) + '&offset=0')
	var = res.json()

	if os.path.isdir(dir1) == False:
		os.mkdir(dir1)

	archivo = json.dumps(var, indent = 4)
	f = open(dir1 + '/' + endpoint + '.json', "w")
	f.write(archivo)
	f.close()
	client.upload_file(dir1 + '/' +endpoint + '.json', nombre_bucket, endpoint + '/' + endpoint + '.json')
	return var

def cargarEncounters(pokemon,dir1,url2):
	encounters = requests.get(url2 + '/' + pokemon['name'] + '/encounters')

	if os.path.isdir(dir1 + '/encounters') == False:
		os.mkdir(dir1 + '/encounters')

	encounter = encounters.json()
	archivo = json.dumps(encounter, indent = 4)
	f = open(dir1 + '/encounters/' + pokemon['name'] + '-encounter.json', "w")
	f.write(archivo)
	f.close()
	client.upload_file(dir1 + '/encounters/' + pokemon['name'] + '-encounter.json', nombre_bucket, endpoint + '/encounters/' + pokemon['name'] + '-encounter.json')

def verificarCategoria(categoria,lista):
	for i in range(0,len(lista)):
		if  lista[i][0]['category']['name'] == categoria:
			return True,i
	return False,-1

def cargarItems(items):
	lista = []
	for item in items['results']:
		item1 = requests.get(url2 + '/' + item['name'])
		item2 = item1.json()
		res, index = verificarCategoria(item2['category']['name'], lista)
		if res and index >= 0:
			lista[index].append(item2)
		else:
			nueva = []
			nueva.append(item2)
			lista.append(nueva)
	return lista


for endpoint in endpoints:
	dir1 = dir + endpoint
	url2 = url + endpoint
	var = cargarEndpoint(endpoint,dir1,url2)
	if endpoint == 'pokemon':
		for pokemon in var['results']:
			cargarEncounters(pokemon,dir1,url2)
	if endpoint == 'item':
		lista = cargarItems(var)
		for list in lista:
			categoria = list[0]['category']['name']
			js = {'\''+categoria+'\'' : list}
			archivo = json.dumps(js, indent = 4)
			f = open(dir1 + '/' + categoria+'.json', "w")
			f.write(archivo)
			f.close()
			client.upload_file(dir1 + '/' + categoria +'.json', nombre_bucket, endpoint + '/' + categoria + '.json')
