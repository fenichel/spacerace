#!/bin/python

import cgitb
import cgi
import csv

from stravalib import Client
from units import unit
import datetime
import pygal

cgitb.enable()
kerbal = ''
rocketship = ''

def read_from_file():
	data = []
	with open('status.csv') as csvfile:
		units_feet = unit('ft')
		reader = csv.DictReader(csvfile, fieldnames=['racer_name', 'elevation_ft'])
		for row in reader:
			data.append((row['racer_name'], float(row['elevation_ft'])))
	return data

def print_spaceracer_table(status_list):
	print("<table>")
	print("<tr><td>Name</td><td>Elevation</td></tr>")
	for item in status_list:
		print("<tr>")
		print("<td>" + item[0] + "</td>")
		print("<td>" + str(int(item[1])) + " ft</td>")
		print("</tr>")
	print("</table>")

def do_stuff():
	status_list = read_from_file()
	# This part is the actual web page
	print("Content-type: text/html") #We are using HTML, so we need to tell the server
	print() #Just do it because it is in the tutorial :P
	print()
	print("<title> Spacerace </title>")
	
	print()
	print("<body>")
	print("<br/>In the interest of load times, this page now reloads data once every hour.<br/>")
	print("<img src=\"status.svg\"></img>")
	#make_fancy_chart(status_list)
	print("<br/>")
	print("Feet climbed since June 18, 2016")
	print("<br/>")
	print_spaceracer_table(status_list)
	print("</body>")


do_stuff()
