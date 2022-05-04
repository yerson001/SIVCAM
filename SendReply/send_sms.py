import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('AC44ccb9137fb482535fbeeca61aba1f19')
auth_token = os.getenv('860eb8ac9c926043cadf91bf5458ee1d')
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
        body="What goes best with a cup of coffee? Another cup. \n \nThanks for being a loyal customer, we want to show you some love back \n \nShop our new buy 1 get 1 free promo online.",
        from_='whatsapp:+14155238886',
        #photo needs to be publically avaiable -- upload to flickr 
        #media_url=['https://live.staticflickr.com/65535/51898195883_13c197808a_b.jpg'],
        to='whatsapp:+51963828458'
    )

print(message.sid)
