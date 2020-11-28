
import requests
import os
import json
import boto3


access_key = 'AKIAUQYANRW63ENTI5F4'
secret_access_key = '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'
nombre_bucket = 'pruebastrabajofinal'


url = 'https://pokeapi.co/api/v2/'
dir = '/home/ubuntu/PokeApi/'
#endpoints = ['berry', 'berry-firmness', 'berry-flavor','contest-type','contest-effect','super-contest-effect','encounter-method','encounter-condition','encounter-condition-value',
#             'evolution-chain','evolution-trigger','generation','pokedex','version','version-group','item','item-category','item-fling-effect',
#             'item-pocket','location','location-area','pal-park-area','region','machine','move','move-ailment','move-category','move-learn-method',
#             'move-target','ability','characteristic','egg-group','gender','growth-rate','nature','pokeathlon-stat','pokemon','pokemon-color','pokemon-form',
#             'pokemon-habitat','pokemon-shape','stat','type']

endpoints = ['berry','berry-firmness','berry-flavor']
for endpoint in endpoints:
	dir1 = dir+endpoint
	url2= url+endpoint
	respone = requests.get(url2)
	print(respone.json())
	cantidad = respone.json()['count']
	res = requests.get(url2+'?limit='+str(cantidad)+'&offset=0')
	var = res.json()
	if os.path.isdir(dir1) == False:
		os.mkdir(dir1)
	s = json.dumps(var, indent=4)
	f = open(dir1+'/'+endpoint+'.json', "w")
	f.write(s)
	f.close()
#	client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)
#	client.upload_file(dir1+'/'+endpoint+'.json',nombre_bucket,endpoint+'/'+endpoint+'.json')
	if endpoint == 'pokemon':
		for pokemon in var['results']:
			encounters = requests.get(url2+'/'+pokemon['name']+'/encounters')
			if os.path.isdir(dir1+'/encounters') == False:
				os.mkdir(dir1+'/encounters')
			en = encounters.json()
			a = json.dumps(en, indent=4)
			f = open(dir1+'/encounters/'+pokemon['name']+'-encounter.json', "w")
			f.write(s)
			f.close()
			#client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key_id = secret_access_key)
			#client.upload_file(dir1+'/'+endpoint+'/encounters/'+pokemon['name']+'-encounter.json',nombre_bucket,endpoint+'/encounters/'+pokemon['name']+'encounter.json')

