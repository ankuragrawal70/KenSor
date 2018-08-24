__author__ = 'Ankur Agrawal'
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
def process_links(link):
    try:
        web_page = urllib2.urlopen(link,timeout=4)
        soup = BeautifulSoup(web_page)
        c=soup.find_all('a')
        count=0

        for e in c:
            try:
                l=e['href']
                count=count+1
                #if ".iitr." in l or l[0]=='/':
                print l
            except:
                print'error in links'
    except:
        deadlinks.append(links)
        print 'dead main link'
def dead_links(link):
    """if link in links_distributio:
        links_distributio[l]=links_distributio[l]+1
        return"""
    try:
        #print 'hello'
        web_page = urllib2.urlopen(link,timeout=4)
        soup = BeautifulSoup(web_page)
        c=soup.find_all('a')
        for e in c:
            try:
                    l=e['href']
                    #if "iitr." in l or l[0]=='/':
                    if 'iitr.' in l or l[0]=='/':
                        if l[0]=='/':
                            process_l=link+l
                        else:
                            process_l=l
                        if process_l not in links_distributio:
                            links_distributio[process_l]=1
                            print 'link is',process_l
                            print 'calling dead link function again'
                            dead_links(process_l)

                        else:
                            #links_distributio[l]=links_distributio[l]+1
                            #pass
                            return

            except:
                print'error in links'
    except:

        print 'dead main link'
        if link not in deadlinks:
            deadlinks.append(link)
            path="D://deadlinks.txt"
            f=open(path,'a+')
            f.write(link+'\n')
            f.close()

if __name__ == '__main__':
    links_distributio={}
    deadlinks=[]
    dead_links("http://www.iitr.ac.in/")
    print 'total links are', len(links_distributio)
    print links_distributio
    print deadlinks
