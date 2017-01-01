import urllib2
import json
import os
from settings import URL, DIR

def request_post_from_site() :
	postid = 1
	while True :
		try:
			loadurl = urllib2.urlopen(URL + str(postid))
		except :
			print "Network Error!, Cannot retrieve posts from Towardlight.com"
			return False
		else:
			jsondata = json.load(loadurl)
		
		if jsondata :
			open(os.path.join(DIR,str(postid)+'.txt'), 'w').write(jsondata[0]['body'])
			print "Post received, ID : %i , Content : '%s....'"%(postid,jsondata[0]['body'][:15])
			postid += 1
		else :
			break

	return True


	