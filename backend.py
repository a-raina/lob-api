'''
Created by Anmol Raina
Date: 5th Oct. 2016
anmol.raina642@gmail.com
'''

import requests
import json
import statistics
import math
import sys
from flask import Flask, render_template, request, jsonify, Markup
import lob_backend as lob

app = Flask(__name__)

'''
This is the controller for communicating with the main backend of the project.
All the API calls are made in lob_backend.py.
'''
def lob_backend_controller(form):
    #The follow variables extract the various information from the frontend
    firstname = form['firstname']
    lastname = form['lastname']
    address1 = form['address1']
    address2 = form['address2']
    city = form['city']
    state = form['state']
    zipcode = form['zipcode']
    message = form['message']  
    letter=None
    # print(address1, address2,city,state,zipcode)
    #using a try and except to handle various edge error cases
    try:
        fromAddress=lob.create_address_object(firstname+" "+lastname,address1,address2,city,state,zipcode)  
        # print(fromAddress)
        res=lob.verify_address_from_lob(fromAddress)   
        # print("ADDRESS VERFIFICATION: ", res) 
        #error handling for if the address could not be verified
        if 'error' in res:
            return("<p>The address you entered could not be verified. Please enter a valid address.</p>")
        else:
            if len(fromAddress['address_state']) > 2:
                fromAddress['address_state'] = res['address']['address_state']
                fromAddress['address_line1'] = res['address']['address_line1']
                fromAddress['address_line2'] = res['address']['address_line2']
                fromAddress['address_city'] = res['address']['address_city']
                fromAddress['address_zip'] = res['address']['address_zip']
                zipcode = fromAddress['address_zip']
        fromId = lob.create_address_from_lob(fromAddress)
        res = lob.get_respone_from_google(zipcode)
        #error handling for if Google's API did not return an object with the given zipcode
        if 'error' in res:
            return("<p>ERROR.</p><p>Hmmm...looks like the Google API could not find an approprite governor for the given zipcode.</p>")
        toAddress = lob.create_address_from_google(res)
        toId = lob.create_address_from_lob(toAddress)
        letterObject = lob.create_letter_object(toId,fromId,message)
        letter = lob.create_letter(letterObject)
    except Exception as e:
        return("<p>Whooops...looks like something went wrong</p><p>Here is the error:</p><p>%s</p>"%e)
    if letter == None:
        return("<p>Whooops...looks like something went wrong</p><p>Looks like the letter was not created fro some reason..</p>")
    return letter


'''
This method controls the view and interacts with the controller declared above.
'''
@app.route("/", methods=['POST', 'GET'])
def main():
    
    if request.method == 'POST':
        # print("POSTTTT")
        if request.form['submit'] == 'Send Letter':
            # print("GETS HERE")
            #call to the controller
            letter = lob_backend_controller(request.form)
            #check for errors
            if type(letter) == str:
                letter = "<h3>ERROR</h3>" + letter
                value = Markup(letter)
                return render_template('displayResponse.html', value=value)
            deliveryDate = letter['expected_delivery_date']
            letterId = letter['id']
            letterUrl = letter['url']
            governorName = letter['to']['name']
            #construct the html string indicating success
            returnStr = "<h3>SUCCESS!</h3>"
            returnStr += "<p>Your letter to governor %s has been created and will be sent!</p>"%governorName
            returnStr+= '<p>You can preview it here <a href="%s" >Preview</a></p>'%letterUrl
            returnStr+= "<p>Expected delivery date: %s</p>"%deliveryDate
            returnStr+= "<p>Letter Id: %s</p>"%letterId
            value = Markup(returnStr)
            return render_template('displayResponse.html', value=value)
        # print("YOOOO")
    elif request.method == 'GET':
        # print("GETTTTT")
        pass

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)


