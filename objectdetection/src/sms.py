from twilio.rest import Client
from decouple import config

"""
SMS Class responsible for sending messages to client
"""
class SMS:

    def __init__(self, ct):
        self.time = ct
        self.account_sid = config('SMS_ACCOUNT_SID')
        self.auth_token  = config("SMS_AUTH_TOKEN")
        self.to_ = config("TARGET_NUMBER")
        self.from_ = config("TWILIO_NUMBER")


    def send_sms(self):
        """ Sends an sms message using the Twilio api and notifies the user with
        the current time that a person has been seen while the service is active
        """
        try:
            client = Client(self.account_sid, self.auth_token)
            text_message = "There was somebody detected by your camera at: {}".format(str(self.time))
            message = client.messages.create(
                to=self.to_, 
                from_=self.from_,
                body=text_message)
            print("New message with id: {}".format(message.sid))
        except:
            raise Exception("""Either the Twilio account sid, auth token,
                from or target phone number has been passed incorrectly""")
