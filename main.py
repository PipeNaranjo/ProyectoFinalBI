
import requests
import os
import json
import errno
import boto3


access_key = 'AKIAQK6GXBJHZ5GKSKVH'
secret_access_key = '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'
nombre_bucket = 'Desarrollo'


url = 'https://pokeapi.co/api/v2/'
dir = 'D:/PokeApi/'
#endpoints = ['berry', 'berry-firmness', 'berry-flavor','contest-type','contest-effect','super-contest-effect','encounter-method','encounter-condition','encounter-condition-value',
#             'evolution-chain','evolution-trigger','generation','pokedex','version','version-group','item','item-category','item-fling-effect',
#             'item-pocket','location','location-area','pal-park-area','region','machine','move','move-ailment','move-category','move-learn-method',
#             'move-target','ability','characteristic','egg-group','gender','growth-rate','nature','pokeathlon-stat','pokemon','pokemon-color','pokemon-form',
#             'pokemon-habitat','pokemon-shape','stat','type']

endpoints = ['pokemon']

for endpoint in endpoints:
    url2= url+endpoint
    respone = requests.get(url2)
    try:
        os.mkdir(dir+endpoint+'/')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    cantidad = respone.json()['count']
    res = requests.get(url2+'?limit='+str(cantidad)+'&offset=0')
    var = res.json()
    s = json.dumps(var, indent=4)
    f = open(dir+endpoint+'/'+endpoint+'.json', "w")
    f.write(s)
    f.close()
    #client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key_id = secret_access_key)

    #client.upload_file(dir+endpoint+'/'+endpoint+'.json',nombre_bucket,endpoint+'/'+endpoint+'.json')
    if endpoint == 'pokemon':
        for pokemon in var['results']:
            encounters = requests.get(url2+'/'+pokemon['name']+'/encounters')
            en = encounters.json()
            try:
                os.mkdir(dir+endpoint+'/encounters/')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            
            s = json.dumps(en, indent=4)
            f = open(dir+endpoint+'/encounters/'+pokemon['name']+'.json', "w")
            f.write(s)
            f.close()



