import urllib2
import praw
import urllib
from urlparse import urljoin
from os.path import expanduser
from bs4 import BeautifulSoup as bs
import os
import requests
from subprocess import call

home = expanduser("~")+"/Desktop/"
def dl(each):
	filename=each.split('/')[-1]
	urllib.urlretrieve(each, filename)

def dligifv(each):
	filename=each.split('/')[-1]
	each1 = each.split(".")
	each1[-1] = "webm"
	if not os.path.exists(home+filename):
		urllib.urlretrieve(".".join(each1), home+filename)

def dlalbum(x):
	response = requests.get(x+"/all")
	soup =  bs(response.text,"lxml")
	listimg = soup.find(id="imagelist")
	directory = home+"/"+x.split("/")[-1]
	if not os.path.exists(directory):
	    os.makedirs(directory)
	images = listimg.find_all("a",href=True)
	for i in range(len(images)):
		try:
			print "Downloading album image "+str(i+1)+" of "+str(len(images))
			# print images[i]['href']
			iimgurdl(urljoin(x,images[i]['href']),directory,i)	
		except:
			pass

def gfydl(link):
	response = requests.get(link)
	soup = bs(response.text,"lxml")
	each = soup.find(id="mp4Source")['src']
	filename=each.split('/')[-1]
	mp3file = urllib2.urlopen(each)
	if not os.path.exists(home+filename):
		with open(home+filename,'wb') as f:
			f.write(mp3file.read())


def iimgurdl(link,directory=None,i=None):
	# print link,directory,i
	if "gifv" in link:
		dligifv(link)

	else:
		if directory and i:
			filename=link.split('/')[-1]
			if len(filename.split(".")[0])>8 and filename.split(".")[0][-1]=="b":
				pass
			else:	
				fpath =  directory+"/"+str(i)+"_"+filename
				if not os.path.exists(fpath):

					urllib.urlretrieve(link,fpath)
		else:
			filename=link.split('/')[-1]
			fpath =  home+filename
			if not os.path.exists(fpath):
		
				urllib.urlretrieve(link,fpath)
					
def imgurDL(link):
	if "i.imgur" in link:
		iimgurdl(link)
	elif "imgur.com/a/" in link:
		dlalbum(link)
	elif "imgur" in link:
		pass	 	
def typeget(link):
	if "imgur" in link:
		imgurDL(link)
	elif "gfycat" in link:
		gfydl(link)	
	else:
		viddl(link)	
def viddl(link):

	command = "youtube-dl --output " + home +"%(title)s.%(ext)s"+ " "+link
	try:
		call(command.split(), shell=False)
	except:
		pass	

r = praw.Reddit(user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')

linkorsub = raw_input("Single Link or Subreddit? 1 , 2 :\n")
if linkorsub == "1":
	home = expanduser("~") + "/.scrape/"+"common"+"/"
	link = raw_input("Enter link:\n")
	typeget(link)
else:
	subr = raw_input("Enter Subreddit of choice:\n")
	top = input("Enter post limitation(integer):\n")
	fromt = raw_input("Enter time period: hour,day,week,month,year,all\n")

	home = expanduser("~") + "/.scrape/"+subr+"/"

	if not os.path.exists(home):
	    os.makedirs(home)

	print "Your files will be stored in " +home     

	submissions = r.get_subreddit(subr).get_top(limit=top,params={"t":fromt})
	count=1
	for i in submissions:
		print "Downloading "+str(count)+": " +i.url +" ... "
		try:
			typeget(i.url)

		except:
			pass	
		count+=1	
