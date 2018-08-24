import urllib2
import MySQLdb
import pickle
import datetime
import socket
import thread
import threading
import doctest
import os
import requests
import locale
import facebook
from time import gmtime, strftime
from bs4 import BeautifulSoup

#find_twitter_data is supplied the twitter page of a source
def find_twitter_data(link):
    try:
        #print domain_name
        #web_page = urllib2.urlopen(link,timeout=4)
        r = requests.get(link,timeout=4)
        web_page = r.content
        web_page = web_page.replace(r"<!DOCTYPE>", "")
        soup = BeautifulSoup(web_page)
        c=soup.find_all('a')
        stats=[-1,-1,-1,-1]
        for e in c:
            try:
                c_link=e['data-nav']
                if c_link=="followers":

                    #mydivs = e.findAll("span", { "class" : "ProfileNav-value" })
                    folowers=e['title'].split(" ")[0]
                    print 'followers are',folowers
                    stats[0]=int(folowers.replace(',',''))

                if c_link=="following":

                    following=e['title'].split(" ")[0]
                    print 'following are',following
                    stats[1]=int(following.replace(',',''))
                if c_link=="tweets":

                    tweets=e['title'].split(" ")[0]
                    print 'tweets are',tweets
                    stats[2]=int(tweets.replace(',',''))
                if c_link=="favorites":
                    #print e
                    favourite=e['title'].split(" ")[0]
                    print 'favourite are',favourite
                    stats[3]=int(favourite.replace(',',''))
            except:
                #print 'error after parsing links'
                pass
        """if all(len(v) ==0 for v in stats):
            div=soup.find_all("div")
            print div"""
        return stats

    except:
        pass


#find_link method is supplied the domain name of a web site and it outputs the twitter page link of that web site
def find_links(link):
    try :

        r = requests.get(link,timeout=4)
        web_page = r.content
        web_page = web_page.replace(r"<!DOCTYPE>", "")
        soup = BeautifulSoup(web_page)
        c=soup.find_all('a')
        for e in c:
            try:
                l=e['href']
                #print l

                if l not in sources_processed:
                    if "twitter.com/" in l and len(l)<150:
                            print l
                            #find_twitter_data method return strings containing twitter data

                            twitter_stats=find_twitter_data(l)
                            print twitter_stats
                            #print "statistics is ","\n".join(twitter_stats)

            except:
                #print 'error after parsing links'
                pass

    except:
        print 'error in main link'

sources_processed={}
completed_domains={}

#find_links function is given domain name as parameter
find_links("http://www.indianexpress.com")



