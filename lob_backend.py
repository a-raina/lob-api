'''
Created by Anmol Raina
Date: 5th Oct. 2016
'''

import requests
from requests.auth import HTTPBasicAuth
import json
import sys
from flask import Flask, render_template, request, jsonify

import lob

#This should be your Google Civic API key
googleKey = 'PUT YOUR GOOGLE API KEY HERE'

#This should be your lob API key
lob.api_key = 'PUT YOUR LOB API KEY HERE'

#lob endpoint
lob_url = 'https://api.lob.com/v1/'

'''
This call gets the the json object which contains information regarding the governor of the given zipcode.
'''
def get_respone_from_google(zipcode):
    # headers = {'X-Auth-Token':'%s' % token}

    google_civic_url = "https://www.googleapis.com/civicinfo/v2/representatives"
    
    #payload containing zipcode, role and API key. The role can be changed depending on which official you want
    payload = {'address': zipcode, 'levels':'administrativeArea1', 'roles':'headOfGovernment', 'fields':'officials', 'key': googleKey}
    response = requests.get(google_civic_url, params=payload)
    data = response.json()
#    prints json data in a pretty  manner...used for testing
    return data

# print(get_response_json_object(url))

'''
abstract method for connecting to the lob API and recieving data
'''
def get_response_from_lob(url,datum):
	response = requests.post(url, data=datum, auth=HTTPBasicAuth(lob.api_key , ''))
	data = response.json()
	return data

'''
This method queries lob's API to verify given address
'''
def verify_address_from_lob(address_object):
	verification_url = lob_url+'verify'
	
	verify_address = {
		'address_line1':'%s' %address_object['address_line1'],
		'address_line2':'%s' %address_object['address_line2'],
		'address_city':'%s' %address_object['address_city'],
		'address_state':'%s' %address_object['address_state'],
		'address_zip':'%s' %address_object['address_zip']
	}
	
	res = get_response_from_lob(verification_url,verify_address)
	return res


'''
This method queries lob's API to create a given address as lob address object and returns the id of the address obect.
'''
def create_address_from_lob(address_object):
	create_address_url = lob_url+'addresses'

	address = {
		'name':'%s' %address_object['name'],
		'address_line1':'%s' %address_object['address_line1'],
		'address_line2':'%s' %address_object['address_line2'],
		'address_city':'%s' %address_object['address_city'],
		'address_state':'%s' %address_object['address_state'],
		'address_zip':'%s' %address_object['address_zip']
	}

	res = get_response_from_lob(create_address_url,address)
	# print("RESPONS: ",res)
	return res['id']


'''
This method queries lob's API to create a letter  
'''
def create_letter(letter_object):
	letters_url = lob_url+'letters'

	letter={'to' : '%s'  %letter_object['to'],
	  'from' : '%s'  %letter_object['from'],
	  'file' : '%s'  %letter_object['file'],
	  'color' : '%s' %letter_object['color']
  	}

	res = get_response_from_lob(letters_url,letter)
	return res


'''
This method queries creates a letter object from the given parameters
'''
def create_letter_object(to_address,from_address,message):
	#color can be set to False for a black and white letter
	color=True

	#you can style your letter as you desire
	file='''<html><head></head><body><div><p>%s<p></div></body></html>'''%message
	letter={
		'to' : '%s'  %to_address,
		'from' : '%s'  %from_address,
		'file' : '%s'  %file,
		'color' : '%s' %color
	}
	return letter


'''
This method queries creates an address object from the given parameters
'''
def create_address_object(name,address1,address2,city,state,zipcode):
	if len(address2) == 0:
		address2 = ''
	address = {
		'name':'%s' %name,
		'address_line1':'%s' %address1,
		'address_line2':'%s' %address2,
		'address_city':'%s' %city,
		'address_state':'%s' %state,
		'address_zip':'%s' %zipcode
	}
	return address

'''
This method takes as a parameter the response from Google's endpoint and returns an address object containing the governor's address
'''
def create_address_from_google(res):
	address_object = res['officials'][0]['address'][0]
	name = res['officials'][0]['name']
	address = create_address_object(name,address_object['line1'],address_object['line2'],
				address_object['city'],address_object['state'],address_object['zip'])
	return address