import os
print(os.environ, "\n")

import dotenv
dotenv.load_dotenv('.env')
print('dotENV is fine\n')

consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
print('tokens are fine\n')

from requests_oauthlib import OAuth1Session
print('oauthlib is fine\n')

session = OAuth1Session(consumer_key,
	client_secret=consumer_secret,
	resource_owner_key=access_token,
	resource_owner_secret=access_token_secret)

print('oauthsession is fine\n')

# The URL endpoint to update a status (i.e. tweet)
url = 'https://api.twitter.com/1.1/statuses/update.json'

# The contents of status (i.e. tweet text)
status = 'If you are reading this on Twitter, the API request worked!'

# Send a POST request to the url with a 'status' parameter
resp = session.post(url, { 'status': status })

# Show the text from the response
print(resp.text)

def tweet(status):
	resp = session.post(url, { 'status': status })
	return resp.text