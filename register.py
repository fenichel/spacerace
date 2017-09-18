#!/bin/python

import cgitb
import cgi
import csv
import json

from stravalib.client import Client

cgitb.enable() #This will show any errors on your webpage
# This part is the actual web page
print("Content-type: text/html") #We are using HTML, so we need to tell the server

print()

print("<title> Space Race Registration Successful </title>")
print("<body>")
print("\n")

client = Client();
code = cgi.FieldStorage()['code'].value;

client_id = ''
client_secret = ''

with open('../client_info.txt') as infofile:
	data = json.load(infofile)
	client_id = data['id']
	client_secret = data['secret']

access_token = client.exchange_code_for_token(client_id=client_id, 
	client_secret=client_secret, code=code)

client.access_token = access_token
athlete = client.get_athlete()

registered = False
with open('../spaceracers.csv') as csvfile:
	reader = csv.DictReader(csvfile, fieldnames=['id', 'token'])
	for row in reader:
		if row['id'] == str(athlete.id):
			print("""<a href="going_to_space.py">You've already registered</a>""")
			registered = True
			break

if not registered:	
	f = open('../spaceracers.csv', 'a')
	f.write(str(athlete.id) + ',' + str(access_token) +'\n')
	f.close()
	print("""<a href="going_to_space.py">Let's go to space!</a>""")

print("</body>")
