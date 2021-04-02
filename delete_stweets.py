#---------------------------------------------------------
# Steve Trush
# steve@westcountylabs.com
# Delete Your Old Tweets By Your Self
#---------------------------------------------------------

#imports
import json
import datetime
import csv
import re
import string
import tweepy
from tweepy import TweepError as TweetError
from tweepy import RateLimitError as RateLimitError
import time


class Tweet:
	def __init__(self, number, text):
		self.number = number
		self.text = text


#generate_regex: takes a list of regular expression strings, concatenates them with OR and '\S*'
def generate_regex(search_terms):
	result = r"".join([r"\S*"+term.lower()+"\S*|" for term in search_terms])
	return result[:-1]	#gets rid of the last | 

def delete_tweet(tweet, api, confirm_delete):
	if not confirm_delete:
		return False
	try:
		api.destroy_status(tweet.number)
		return True
	except TweetError as te:
		print(te)
		print("There was a problem deleting tweet #" + tweet.text)
		return False
	except RateLimitError as te:
		print(te)
		print("Hit the rate limit... needing to sleep for 15 minutes.")
		time.sleep(15 * 60)
		try:
			api.destroy_status(tweet.number)
			return True
		except TweetError as te:
			print(te)
			print("There was a problem deleting tweet #" + tweet.number)
			return False


#seek_tweets_to_delete: takes a list of tweet objects and the search regular expression 
#returns nothing, other than the satisfaction of deleting tweets that don't match the regex  
def seek_tweets_to_delete(tweets, search_regex, api, confirm_delete): 
	# Process each page contained in the document.
	if not confirm_delete:
		print("Testing... *assume any IDs not printed WILL BE deleted*\n")
	for tweet in tweets:
		text = tweet.text
		m = re.findall(search_regex,text.lower())
		if m is not None and len(m) > 0:
			print("Found a tweet to save: " +text)
			print(list(set(m)))
		else:
			if confirm_delete:
				if delete_tweet(tweet, api, confirm_delete):
					print("Deleted tweet #"+tweet.number)

#main loop
def main():
	
	print("Welcome to s'Tweet of Ole deletion script. Make sure your config.json and old_tweets.json files are ready and in the same folder.\n")
	
	config_data = None

	with open('config.json') as json_data:
		config_data = json.load(json_data)

	search_regex = generate_regex(config_data["precious_terms"])
	print("Here's the regular expression to search for tweets to save: \n"+search_regex)

	twitter_creds = config_data["twitter_creds"]

	#Get data for Twitter application:
	CONSUMER_KEY =    twitter_creds["CONSUMER_KEY"] 
	CONSUMER_SECRET = twitter_creds["CONSUMER_SECRET"]

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	try:
		redirect_url = auth.get_authorization_url()
	except tweepy.TweepError:
		print('Error! Failed to get request token - make sure config.json has the license info.')
		exit()
	
	print('\nPlease authorize the app by clicking or opening this link: ' + redirect_url)
	
	verifier = input('\nEnter Verifier code from twitter.com: ').strip()
	
	try:
		auth.get_access_token(verifier)
	except tweepy.TweepError:
		print('Error! Failed to get access token.')
		exit()
	
	api = tweepy.API(auth)


	old_tweets = [];
	precious_tweets = config_data["precious_tweets"]
	with open("old_tweets.json") as tweetfile:
		reader = json.load(tweetfile)
		for twit in reader["tweets"]:
			if int(twit['tweet']['id']) not in precious_tweets:
				old_tweets.append(Tweet(twit['tweet']['id'],twit['tweet']['full_text']))
			else:
				print("\nSkipping precious tweet: "+twit['tweet']['full_text'])

	print("\nReady to delete tweets! THERE IS NO UNDELETE... but hey, at least you can look at your archive.\n")
	user_choice = input('To test how your regular expressions will match (no deletions will be made), enter the word TEST. \nTo consent to deleting your tweets, enter DELETE.\nTo exit, type anything else: ').strip()
	if user_choice == "TEST":
		print("OK, searching your tweet archives for matches. Nothing will be deleted from Twitter.")
		seek_tweets_to_delete(old_tweets,search_regex, api, False)
	elif user_choice == "DELETE":
		print("Deleting in progress! [Hit Ctrl-C if you really want to save tweets]")
		seek_tweets_to_delete(old_tweets,search_regex, api, True)
	else:
		print("OK, exiting.")
		exit()

	

#execute the main if this is the script being run
if __name__ == "__main__":
	main()

