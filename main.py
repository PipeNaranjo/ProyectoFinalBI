
import requests
import os
import json
import errno
import boto3


access_key = 'AKIAUQYANRW63ENTI5F4'
secret_access_key = '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'
nombre_bucket = 'Pruebas'
nombre_carpeta = 'Cargas'


url = 'https://pokeapi.co/api/v2/'
dir = '/home/ubuntu/PokeApi/'
#endpoints = ['berry', 'berry-firmness', 'berry-flavor','contest-type','contest-effect','super-contest-effect','encounter-method','encounter-condition','encounter-condition-value',
#             'evolution-chain','evolution-trigger','generation','pokedex','version','version-group','item','item-category','item-fling-effect',
#             'item-pocket','location','location-area','pal-park-area','region','machine','move','move-ailment','move-category','move-learn-method',
#             'move-target','ability','characteristic','egg-group','gender','growth-rate','nature','pokeathlon-stat','pokemon','pokemon-color','pokemon-form',
#             'pokemon-habitat','pokemon-shape','stat','type']

endpoints = ['pokemon']

for endpoint in endpoints:
	dir1 = dir+endpoint
	url2= url+endpoint
	respone = requests.get(url2)
	cantidad = respone.json()['count']
	res = requests.get(url2+'?limit='+str(cantidad)+'&offset=0')
	var = res.json()
	s = json.dumps(var, indent=4)
	f = open(dir1+'.json', "w")
	f.write(s)
	f.close()
	#client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key_id = secret_access_key)
	#client.upload_file(dir1+'/'+endpoint+'.json',nombre_bucket,endpoint+'/'+endpoint+'.json')
	if endpoint == 'pokemon':
		for pokemon in var['results']:
			encounters = requests.get(url2+'/'+pokemon['name']+'/encounters')
			if os.path.isdir('/home/ubuntu/PokeApi/encounters/'):
				os.system('/home/ubuntu/PokeApi/encounters/')
			
			en = encounters.json()
			a = json.dumps(en, indent=4)
			f = open(dir+'encounters/'+pokemon['name']+'-encounter.json', "w")
			f.write(s)
			f.close()
			#client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key_id = secret_access_key)
			#client.upload_file(dir1+'/encounters/'+pokemon['name']+'.json')
