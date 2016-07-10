import sys
from bs4 import BeautifulSoup
import datetime
import requests

#this is the establishment time of Twttier, which is the ealiest time of a tweet that can be found
earliest_time=datetime.datetime.strptime("2006-03-01", '%Y-%m-%d')

#pretend we are firefox browser, this ensure we can get right web page
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686 (x86_64); rv:2.0b4pre) Gecko/20100812 Minefield/4.0b4pre'}
#Function: get all tweets in current specific duration
#parameter:
#uri: [string] the link you want to query
#date_from: [datetime] the earliest date of tweets contain this uri
#date_until: [datetime] the latest date of tweets contain this uri
#return: array of  the dates of tweets in this period time
def getDates(uri,date_from,date_until):
	#search patern of the duration specified tweet search
	#https://twitter.com/search?f=tweets&q=[request url]%20since%3A[YYYY-MM-DD]%20until%3A[YYYY-MM-DD]&src=typd
	from_date_str=date_from.strftime("%Y-%m-%d")
	until_date_str=date_until.strftime("%Y-%m-%d")
	search_str='https://twitter.com/search?f=tweets&q={uri}%20since%3A{from_date}%20until%3A{until_date}&src=typd'.format(
		uri = uri, from_date = from_date_str, until_date = until_date_str
		)
	response = requests.get(search_str,headers=headers)
	html = response.text
	soup = BeautifulSoup(html)

	#get all tweets and their text in result (not necessary here, debug use only)
	#tweets = soup.find_all('li', 'js-stream-item')

	#get all tweets text in result this is used for get amount fo results
	tweet_text=soup.find_all('p','js-tweet-text')

	#get all timestamp of  tweets
	tweet_timestamps=soup.find_all('a','tweet-timestamp')
	timestamps=[]


	for i in range(0, len(tweet_text)):
		#get  tweets text (no need here)
		#tweet= tweets[i].get_text().encode('ascii', 'ignore')
		#get time of the tweet
		time_stamp = datetime.datetime.strptime(tweet_timestamps[i]['title'], '%I:%M %p - %d %b %Y')
		timestamps.append(time_stamp)
	return timestamps
#get most likely oldest date of tweet that have uri in given time period with bnary search
def getEarliestDate(uri,from_date,until_date):
	midDate=from_date+(until_date-from_date )/2
	upperbound=from_date
	lowerbound=midDate
	result=getDates(uri,from_date,midDate)
	if len(result)==0:
		upperbound=midDate
		lowerbound=until_date
		result=getDates(uri,midDate,until_date)
	#check result
	#if still zero return none, indicate that we cannot find tweets
	if len(result)==0:
		return None
	#if there are result (less than 10 or search bound closed to one day), return last one (oldest one)
	if len(result)<=10 or from_date==until_date:
		return result[-1]
	else:
		#continue binary search
		return getEarliestDate(uri,upperbound,lowerbound)
#interface function for module
def getTwitterCreationDate(uri,outputArray, indexOfOutputArray):
	date=getEarliestDate(uri,earliest_time,datetime.datetime.now())
	result_str=''
	if date is not None:
		result_str=date.strftime('%Y-%m-%dT%H:%M:%S')
		outputArray[outputArrayIndex] = result_str
	
	return result_str

if __name__ == '__main__':
	if len(sys.argv)<2:
		print("Unit testing usage: ", sys.argv[0] + " url  e.g: " + sys.argv[0] + " http://www.cs.odu.edu ")
	else:
		getTwitterCreationDate(sys.argv[1])