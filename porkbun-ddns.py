import json
import requests
import os
import time

apiConfig = json.load(open("config.json")) #load the config file into a variable
rootDomain = os.environ.get('DOMAIN')
subDomain = os.environ.get('SUBDOMAIN')
interval = 15

def getRecords(domain): #grab all the records so we know which ones to delete to make room for our record. Also checks to make sure we've got the right domain
	allRecords=json.loads(requests.post(apiConfig["endpoint"] + '/dns/retrieve/' + domain, data = json.dumps(apiConfig)).text)
	if allRecords["status"]=="ERROR":
		print('Error getting domain. Check to make sure you specified the correct domain, and that API access has been switched on for this domain.');
	return(allRecords)
	
def getMyIP():
	ping = json.loads(requests.post(apiConfig["endpoint"] + '/ping/', data = json.dumps(apiConfig)).text)
	return(ping["yourIp"])

def deleteRecord():
	for i in getRecords(rootDomain)["records"]:
		if i["name"]==fqdn and (i["type"] == 'A'):
			print("Deleting existing " + i["type"] + " Record")
			deleteRecord = json.loads(requests.post(apiConfig["endpoint"] + '/dns/delete/' + rootDomain + '/' + i["id"], data = json.dumps(apiConfig)).text)

def checkRecord():
	for i in getRecords(rootDomain)["records"]:
		if i["name"]==fqdn and (i["type"] == 'A'):
			return(i["content"])

def createRecord():
	createObj=apiConfig.copy()
	createObj.update({'name': subDomain, 'type': 'A', 'content': myIP, 'ttl': 300})
	endpoint = apiConfig["endpoint"] + '/dns/create/' + rootDomain
	print("Creating record: " + fqdn + " with answer of " + myIP)
	create = json.loads(requests.post(apiConfig["endpoint"] + '/dns/create/'+ rootDomain, data = json.dumps(createObj)).text)
	return(create)

while True:
	fqdn = subDomain + "." + rootDomain

	recordIP=checkRecord()
	print("DNS record: " + recordIP)
	myIP=getMyIP()
	print("my IP: " + myIP)
	if myIP == recordIP:
		print("Update not needed")
	else:
		print("Proceed to update")
		deleteRecord()
		print(createRecord()["status"])

	print("Next check in " + str(interval) + " minutes")
	time.sleep(interval*60)
