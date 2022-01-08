#Twillio Backend for Sending Messages

#imports
import requests, json
from twilio.rest import Client
import requests


#Admin phone is the sending phone from twillio
AdminPhoneNumber="+14153012091"

def send_message(msg,phone):
	message = msg

	client = Client(account_sid, auth_token)
	message = client.messages.create(
	to=phone,
	from_=AdminPhoneNumber,
	body=message)
