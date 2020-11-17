import re
import json
from urllib.request import urlopen
from IPy import IP

#url = 'http://ipinfo.io/json'
#response = urlopen(url)
#data = json.load(response)
addr = '11.221.102.102'

ip = IP(addr)
print(ip.iptype() == "PUBLIC")
'''
if addr == '':
    url = 'https://ipinfo.io/json'
else:
    url = 'https://ipinfo.io/' + addr + '/json'
res = urlopen(url)
#response from url(if res==None then check connection)
data = json.load(res)
#will load the json response into data
for attr in data.keys():
    #will print the data line by line
    print(attr,' '*13+'\t->\t',data[attr])
    '''
'''
city = data['city']
country=data['country']
region=data['region']
'''
'''
IP=data['ip']
org=data['org']

city = data['city']
country=data['country']
region=data['region']

print ('Your IP detail\n ')
print ('IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0}'.format(org,region,country,city,IP))'''