import os
import urllib2
import MySQLdb
import pickle
import datetime
import socket
import thread
import threading
import doctest
import os
import re
import facebook
from time import gmtime, strftime
from bs4 import BeautifulSoup


#function finds url from the web site
def find_domain(url):

            web_page = urllib2.urlopen(url,timeout=4)
            soup = BeautifulSoup(web_page)
            #c=soup.find_all('a')
            #for e in c:
            try:
                        div_tag=soup.find_all("div",{"class":'col span_1_of_2'})
                        print div_tag[0].find('a')['href']+'\n'

            except:
                    print 'error after parsing links'
                    pass
def process(source,file_name):
    try:
            path="D://Thesis//data//domain_name//news_sources_ranking//europe//"
            f_des=open(path+file_name+'.txt','a+')
            #source="http://www.4imn.com/us/"
            web_page = urllib2.urlopen(source,timeout=4)
            soup = BeautifulSoup(web_page)
            c=soup.find_all('a')
            for e in c:
                try:
                        l=e['href']
                        if '/review' in l:
                            #find_domain("http://www.4imn.com"+l)

                            #this is used to find domain name of particular news source

                            #url="http://www.4imn.com"+l
                            url=l
                            web_page = urllib2.urlopen(url,timeout=4)
                            soup = BeautifulSoup(web_page)
                            #c=soup.find_all('a')
                            #for e in c:
                            try:
                                        div_tag=soup.find_all("div",{"class":'col span_1_of_2'})
                                        val=div_tag[0].find('a')['href']+'\n'
                                        print str(val)
                                        f_des.write(str(val))

                            except:
                                    print 'error after parsing links'
                                    pass

                except:
                    print 'error after parsing links'
                    pass


    except:
            print 'error in main link'


link="http://www.4imn.com/Europe/"
try:
    web_page = urllib2.urlopen(link,timeout=4)
    soup = BeautifulSoup(web_page)
    c=soup.find_all('a')
    count=0
    for e in c:
        try:
            l=e['href']
            if "http://www.4imn.com/" in l and l!="http://www.4imn.com/":
                #print l

                #filename=l.split("us/")[1].rstrip('.htm')
                file_name=e.text
                #print file_name
                if len(file_name)>0:
                    print l,file_name
                    count=count+1
                    process(l,file_name)

        except:
            pass
    print count
except:
    print 'error in main link'
#process()