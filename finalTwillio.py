#Twillio Backend for Sending Messages

#imports
import requests, json
from twilio.rest import Client
import requests

#Twillio Account ID
account_sid = 'AC5a0bfbd5b477c769757be6b337e1160b'
#Twillio API token
auth_token = '86f2de606427a1f92d20e82678f7a3b3'
#Admin phone is the sending phone from twillio
AdminPhoneNumber="+14153012091"

def send_message(msg,phone):
	message = msg

	client = Client(account_sid, auth_token)
	message = client.messages.create(
	to=phone,
	from_=AdminPhoneNumber,
	body=message)
