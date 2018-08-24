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
import requests
import time
from datetime import timedelta
from time import gmtime, strftime
from bs4 import BeautifulSoup
def find_links(link,cate,c_time):
    try :
        print link
        output=""
        domain_name=link.split("http://")[1].split("/")[0]
        print domain_name
        #web_page = urllib2.urlopen(link,timeout=4)
        r = requests.get(link,timeout=4)
        web_page = r.content
        web_page = web_page.replace(r"<!DOCTYPE>", "")
        soup = BeautifulSoup(web_page)

        c=soup.find_all('a')
        for e in c:
            #print e
            try:
                l=e['href']
                if l not in output:
                    if l!=link and l!=domain_name and domain_name in l and cate in l:
                        output=output+l+'\n'

                    #check_validity(l,level,domain_name)
            except:
                print 'error after parsing links'
                pass

        print cate
        #print output


        if len(output)>0:
            #print "all links are",output
            path="D://Thesis//data//domain_name//domains_related_crawler//"+link.split("http://")[1].replace("/","#")

            if not os.path.isdir(path):
                os.makedirs(path)
            #st=datetime.datetime.now().ctime()
            #st=date.today()
            #print str(st)
            #print path
            store_path=path+"//"+c_time+'.txt'
            f_wr=open(store_path,"w")
            f_wr.write(output)
            f_wr.close()
            print 'processed',link
            pr_link="D://Thesis//data//domain_name//domains_related_crawler//valid_links.txt"
            f_pr=open(pr_link,'a+')
            f_pr.write(link+'\n')
            f_pr.close()
        else:
            print "no links found invalid",link
            inv_path="D://Thesis//data//domain_name//domains_related_crawler//invalid_links.txt"
            f_inv=open(inv_path,"a+")
            f_inv.write(link+'\n')
            f_inv.close()


    except:
        print "error in main link invalid",link
        inv_path="D://Thesis//data//domain_name//domains_related_crawler//invalid_links.txt"
        f_inv=open(inv_path,"a+")
        f_inv.write(link+'\n')
        f_inv.close()

def time_call():
    #.strftime("%A, %d. %B %Y %I.%M")
    #print current_time+datetime.timedelta(seconds=3)
    #current_time=datetime.datetime.now()
    current_time=beg_time
    while current_time<stop_time:
            start_time=current_time
            #st = datetime.datetime.now().strftime("%A, %d. %B %Y %I.%M")
            #find_links("http://www.thehindu.com/business",'business',st)
            for i in range(44491,len(sources)):
                st = datetime.datetime.now().strftime("%A, %d. %B %Y %I.%M")
                cate=sources[i].split("/")[-1]
                #print cate
                #break
                #print i
                #print sources[i]
                try:
                    find_links(sources[i],cate,st)
                    print i
                except:
                    pass
            #find_links('http://www.thehindu.com/business','business',str(st))
            lates_time=datetime.datetime.now()
            remaining_time=((start_time+datetime.timedelta(hours=12))-lates_time).total_seconds()
            time.sleep(remaining_time)
            current_time=datetime.datetime.now()
            #diff_seconds = (mytime-since).total_seconds()
            #current_time=datetime.datetime.now()

path1="D://Thesis//data//domain_name//domains_related_to_category_path//distributed_Sources//domain_10_sources1.txt"
f_path=open(path1,"r")
sources=f_path.read().split("\n")
f_path.close()
beg_time=datetime.datetime.now()
#print '{:%H:%M:%S}'.format(current_time)

stop_time=beg_time+ timedelta(days=7)
print 'stop time is',stop_time

time_call()