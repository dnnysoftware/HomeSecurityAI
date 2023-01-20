import os
from twilio.rest import Client
import datetime

"""
SMS Class responsible for sending messages to client
"""
class SMS:
    def __init__(self, ct):
        self.time = ct
        self.account_sid = os.environ.get("ACCOUNT_SID")
        self.auth_token  = os.environ.get("AUTH_TOKEN")
        self.to_ = os.environ.get("TARGET_NUMBER")
        self.from_ = os.environ.get("TWILIO_NUMBER")


    def send_sms(self):
        
        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            to=self.to_, 
            from_=self.from_,
            body="There was somebody detected by your camera at " + str(self.time))
        print(message.sid)
