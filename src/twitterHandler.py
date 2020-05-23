import json
import requests
import tweepy as twp
import os
import time
from requests_oauthlib import OAuth1


MEDIA_ENDPOINT_URL = "https://upload.twitter.com/1.1/media/upload.json"
POST_TWEET_URL = "https://api.twitter.com/1.1/statuses/update.json"

with open('twitterConfig.json') as file_out:
	file_data = json.load(file_out)
config_data = file_data

oauth = OAuth1(
	file_data['api_key'],
	client_secret=file_data['api_key_secret'],
	resource_owner_key=file_data['access_token'],
	resource_owner_secret=file_data['access_token_secret']
)

video_filename = "videoMashed0.mp4"

global media_id
def update_status_with_video(tweet, video):
	global media_id
	api = twitter_auth_setup()
	finalise_upload(append_upload(init_upload(video)))
	api.update_status(status=tweet, media_ids=[media_id])
	print("posted the video")

def twitter_auth_setup():
	api = config_data
	# set up OAuth handling
	auth = twp.OAuthHandler(config_data['api_key'], config_data['api_key_secret'])
	auth.set_access_token(config_data['access_token'], config_data['access_token_secret'])
	api = twp.API(auth)
	return api

def init_upload(video):
	global media_id
	request_data = {
		'command': 'INIT',
		'media_type': 'video/mp4',
		'total_bytes': os.path.getsize(video_filename),
		'media_category': 'tweet_video'
	}
 
	req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)
	media_id = req.json()['media_id']
	return video

def append_upload(video):
	global media_id
	segment_id = 0
	bytes_sent = 0
	filename = video_filename
	file = open(filename, 'rb')

	while bytes_sent < os.path.getsize(filename):
		chunk = file.read(5*1024*1024)

		request_data = {
			'command': 'APPEND',
			'media_id': media_id,
			'segment_index': segment_id
		}

		files = {
		'media':chunk	
		}

		req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, files=files, auth=oauth)

		if req.status_code < 200 or req.status_code > 299:
			sys.exit(0)

		segment_id = segment_id + 1
		bytes_sent = file.tell()
	return video


def finalise_upload(video):
	global media_id
	request_data = {
		'command': 'FINALIZE',
		'media_id': media_id
	}

	req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)

	processing_info = req.json().get('processing_info', None)
	state = processing_info['state']

	if state == u'succeeded':
		return
	if state == u'failed':
		sys.exit(0)

	check_after_secs = processing_info['check_after_secs']
	time.sleep(check_after_secs)

	request_params = {
		'command': 'STATUS',
		'media_id': media_id
	}

	req = requests.get(url=MEDIA_ENDPOINT_URL, params=request_params, auth=oauth)

	processing_info = req.json().get('processing_info', None)
	finalise_upload(video)
