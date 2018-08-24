import csv
import os
import thread
import time
import threading
import geoip2.database
import socket
from bs4 import BeautifulSoup
#import gexf
#mport networkx as nx
#import matplotlib.pyplot as plt
import sys
import MySQLdb
def domain_check(domain_name):
    d_name=domain_name.split('/')[0]
    #if d_name=='/':
    #    print d_name
    d_name='http://'+d_name+'\n'
    if d_name not in domain:
        domain[d_name]=1
def domain_identification(url_name):
    splitted_url=url_name.split("//")
    if len(splitted_url)>=2:
        domain_check(splitted_url[1])
    else:
        #print 'hello'
        #print splitted_url[0]
        domain_check(splitted_url[0])
def url_reader():
    path="D://Thesis//data//"
    filename=os.listdir(path)
    try:
        for i in range(0,len(filename)-2):
            file1=path+filename[i]
            f=open(file1,"rb")
            date=filename[i][:-11]
            ac_date=date[0:4]+"/"+date[4:6]+"/"+date[6:len(date)]
            reader1 = csv.reader(f,delimiter='\t')
            row=list(reader1)
            f.close()
            #row is a set of rows of the given file
            #url is a hash_map that contains the urls and their count
            for row1 in row:
                x=len(row1)
                url_name=row1[x-1]
                domain_identification(url_name)
                """if url.has_key(url_name):
                        url[url_name]=url[url_name]+1
                else:
                        url[url_name]=1
                        domain_identification(url_name)"""
                        #category_domain_info(domain_name)
                        #loc(domain_name)
            print "\ndate",ac_date
            #print "toal urls\n",len(url)
            #print "\ttotal unique urls are",len(url)
            print "\t file procees are\t",i
            print 'domain length is',len(domain)
            #print domain
            #print url
    except:
        print 'error'
        pass

domain={}
url={}
#url_reader()
#domain_path="D://Thesis//data//domain_name//gdelt_domain.txt"
f=open(domain_path,'w')
x=domain.keys()
s=''.join(x)
f.write(s)
f.close()
"""f1=open(domain_path,'r')
e=f1.read().split('\n')
for x in e:
    if 'http://unmiss.unmissions.org' in x:
        c='http://unmiss.unmissions.org'
    else:
        if x.count('.')==0 or ',' in x:
            continue
        else:
            if '?' in x:
                c=x.split('?')[0]
            else:
                c=x
    if c not in domain:
        domain[c+'\n']=1
f1.close()
d_path1="D://Thesis//data//domain_name//gdelt_domain1.txt"
f=open(d_path1,'w')
x=domain.keys()
s=''.join(x)
f.write(s)
print len(domain)"""
