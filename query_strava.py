#!/bin/python

import csv
from stravalib import Client
from units import unit
import datetime
import time
import os
import sys
import pygal

import spacestrings

os.chdir(sys.path[0])

ACCEPTED_TYPES = ['Ride', 'Run', 'Swim', 'Hike', 'Walk', 'Snowshoe', 'NordicSki']

def load_participants():
	participants = {}
	with open('../spaceracers.csv') as csvfile:
		reader = csv.DictReader(csvfile, fieldnames=['id', 'token'])
		for row in reader:
			participants[row['id']] = row['token']
	return participants

def query_strava():
	participants = load_participants()
	# This stuff is the same for everybody
	start_time = 1466233220
	start_datetime = datetime.datetime.utcfromtimestamp(start_time);
	
	now = datetime.datetime.now()
	seven_days_ago = now - datetime.timedelta(days=7)

	spaceracers = {}
	status_list = []
	for id in participants:
		client = Client()
		client.access_token = participants[id]
		athlete = client.get_athlete()
		name = athlete.firstname
		if name == "Nathan":
			if athlete.lastname[0] == "H":
				name = "NHS"
		activities = client.get_activities(after=start_datetime)
		activity_list = list(activities)
	
		units_feet = unit('ft')
		total_elevation = units_feet(0)
		for activity in activities:
			if activity.type in ACCEPTED_TYPES:
				total_elevation += units_feet(activity.total_elevation_gain)
		spaceracers[name] = total_elevation
		status_list.append((name, total_elevation.num, total_elevation, id))

	status_list.sort(key=lambda x: x[1])
	status_list.reverse()
	#for item in status_list:
	#	print(item[0])
	#	print(item[2])
	#	print(item[3])
	return status_list

def write_to_file():
	spaceracer_info = query_strava()
	fieldnames = ['racer_name', 'elevation_ft']
	with open('status.csv', 'w', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=',')
		for item in spaceracer_info:
			writer.writerow({'racer_name': item[0],
			'elevation_ft': item[1]})
	with open('datetime.txt', 'w') as datefile:
		datefile.write(str(time.time()))
	make_fancy_chart(spaceracer_info)

def make_fancy_chart(status_list):
	config = pygal.Config()
	config.style = pygal.style.DarkStyle
	config.defs.append(spacestrings.rocketship)
	config.defs.append(spacestrings.shuttle)
	config.defs.append(spacestrings.rocketflip)
	
	config.defs.append('''
		<linearGradient id="background_gradient" x1="0%" y1="0%" x2="0%" y2="100%">
			<stop offset="0%" style="stop-color:rgb(255, 255, 255);stop-opacity:1" />
			<stop offset="100%" style="stop-color:rgb(0, 0, 0);stop-opacity:1" />
		</linearGradient>
	''')
	config.defs.append(spacestrings.kerbal)
	config.defs.append(spacestrings.sputnik)
	config.range = (0, 400000)
	config.show_legend = False
	chart = pygal.Bar(config)
	chart.title = "AD ASTRA PER ASPERA"
	chart.y_labels=(
		{'label': 'SPACE', 'value': 327000},
		{'label': '10,000', 'value': 10000},
		{'label': '50,000', 'value': 50000},
		{'label': '100,000', 'value': 100000},
		{'label': '150,000', 'value': 150000},
		{'label': '200,000', 'value': 200000},
		{'label': '250,000', 'value': 250000},
		{'label': '300,000', 'value': 300000},
    {'label': '400,000', 'value': 400000}
		)

	chart.x_labels = [x[0] for x in status_list] 
	serie = []
	num_racers = len(status_list)
	for item in status_list:
		if item[1] < 10000:
			value = 10000
			fill = "fill:url(#kerbal);"
		else:
			value = item[1]
			if value < 25000:
				fill = "fill:url(#kerbal);"
			elif value < 100000:
				if item[0] == "Gregory":
					fill = "fill:url(#Rocketflip);"
				else:
					fill = "fill:url(#Rocketship);"
			elif value < 327360:
				fill = "fill:url(#shuttle);"
			else:
				fill = "fill:url(#sputnik);"
		serie.append({'value': value, 'style': fill + ' stroke:none; width:24'})
	chart.add('racers', serie)
	print(chart.render_to_file('status.svg'))

write_to_file()
