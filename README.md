# s'Tweets of Old

A python program that you use to looks through city agenda PDFs for developer-defined regular expressions.
When the bot finds a match, it tweets a match with the date, matching terms, and a link to the file.

Running this requires you to have a Twitter app registered through the Twitter Developer platform (https://developer.twitter.com/) -or- a temporary key requested from info@westcountylabs.com.

Step 1. Request your data archive from Twitter: https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive This can take a day. Any tweets that you create after you receive this archive will not be deleted!

Step 2. Copy delete\_tweets.py, config.json, and a copy of "tweet.js" from your archive renamed as "old\_tweets.json" into the same folder.

Step 3. If you do not have Python3 installed, install Python3: https://www.python.org/downloads/

Step 4. If you do not have Tweepy (a python library for interacting with Twitter's API) installed, install Tweepy: https://docs.tweepy.org/en/latest/install.html You may need to install pip first: https://pip.pypa.io/en/stable/installing/

Step 5. Open config.json:
	
	5a. Replace the "precious\_terms" with the regular expressions of your choice. Letter case does not matter (I'm trying to save people from making mistakes and deleting too much). Also, consider including TwitterIDs for your favorite people that you mention in your tweets. 
	
	5b. Replace the "precious\_tweets" with the status id of any tweets that you want to save.
	
	5c. Copy and paste your "CONSUMER\_KEY" and "CONSUMER\_SECRET" from your Twitter Developer application information  

Step 6. Replace the first line "old_tweets.json" with: ``` { "tweets" : [ { ``` 
and add ```}``` as the last line of the final.

Step 7. Test run the python script in a terminal. Open the activation link in the account for tweet deletion. Copy the verification code back into the console. 

Step 8. Enter "TEST" to see the matches to your regular expression. If you don't see the matches you desire, correct your regular expressions in the config.json file.

Step 9. When ready to delete, repeat Step 7 and enter "DELETE" for tweet removal. Why do you have to repeat Step 7? I really want people to be thoughtful before they remove their tweets for good!




