import urllib2
import MySQLdb
import pickle
import datetime
import socket
import thread
import threading
import doctest
import os
import facebook
import datetime
import time
import requests
from datetime import timedelta
from time import gmtime, strftime
from bs4 import BeautifulSoup
def find_domain(url_link):
    try :
        output=""
        print link
        r = requests.get(url_link,timeout=4)
        web_page = r.content
        web_page = web_page.replace(r"<!DOCTYPE>", "")
        soup = BeautifulSoup(web_page)
        c=soup.find_all("a")
        for e in c:
            try:
                l=e["href"]
                if l[0]!="/" and "http://" in l and "twitter.com" not in l and "linkedin.com" not in l and "facebook.com" not in l:
                    #domain="http://"+l.split("http://")[1].split("/")[0]
                    if "wikinews.org" not in l:
                        if l not in output:
                            output=output+l+"\n"
            except:
                print 'error after parsing links'
                pass
            #break

        return output

    except:
        print "not found"

def find_links(year,month,day,link):
    try :
        db = MySQLdb.connect("localhost",user="root",db="web_categorization")
        cursor = db.cursor()
        output=""
        r = requests.get(link,timeout=4)
        web_page = r.content
        web_page = web_page.replace(r"<!DOCTYPE>", "")
        soup = BeautifulSoup(web_page)
        element=soup.find('div',id="mw-content-text")
        c=element.find_all("a")
        #print c
        for e in c:
            try:
                l=e["href"]
                wiki_link="https://en.wikinews.org"+l
                news_sources=find_domain(wiki_link).split("\n")
                if len(news_sources)>0:
                    for i in range(0,(len(news_sources)-1)):
                        sql = ("insert into wiki_news_sources(year,month,day,wiki_url,domain_name) values ('%s','%s','%s','%s','%s')"%(year,month,day,wiki_link,news_sources[i]))
                        try:
                            cursor.execute(sql)
                            db.commit()
                        except:
                            print "error in insertion"
                            db.rollback()
                        #print source
            except:
                print 'error after parsing links'
                pass
            print "inserted\n",wiki_link
            #break
        db.close()

    except:
        print "not found"

all_month=["January","February","March","April","May","June","July","August","September","October","November","December"]
main_link="https://en.wikinews.org/wiki/Wikinews:"
year=2000
for i in range(12,16):
    for month in all_month:
        for j in range(1,32):
            link=main_link+str((year+i))+"/"+month+"/"+str(j)
            #print link
            find_links(year+i,month,j,link)
            print "day completed",link
