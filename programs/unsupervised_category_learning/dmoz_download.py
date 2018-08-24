import MySQLdb
import gexf
import networkx as nx
import wikipedia
import difflib
import operator
import socket
import os
import urllib2, httplib
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
def check_validity(h_link,domain_name,level):
    
    if domain_name in h_link:
            level[h_link.encode('utf-8')]=1
    else:
        if h_link[0]=='/':
            if domain_name[len(domain_name)-1]!='/':
                
                    #print domain_name+h_link
                level[(domain_name+h_link+'\n').encode('utf-8')]=1
            else:
                l=len(domain_name)-1
                x=domain_name[:l]
                level[(x+h_link+'\n').encode('utf-8')]=1


def find_links(link,domain_name,level):
    #print domain_name
    try :      
        web_page = urllib2.urlopen(link,timeout=4)
        soup = BeautifulSoup(web_page)
        #print 'hello'
        c=soup.find_all('a')
        for e in c:
            #print e
            try:
                l=e['href']
                if l!=domain_name:
                    check_validity(l,domain_name,level)
            except:
                print 'error after parsing links'
                pass
       
    except:
        print 'error in main link'
        pass
        
level3={}
dmoz_data_path='D://Thesis//data//Dmoz data//download//level1.txt'
f=open(dmoz_data_path,'r')
urls=f.read().split('\n')
f.close
for u in urls:
    print u
    find_links(u,'http://www.dmoz.com',level3)
#find_links('http://www.dmoz.com',level3)
print len(level3)
path1='D://Thesis//data//Dmoz data//download//level3.txt'
f1=open(path1,'w')
x=level3.keys()
s=''.join(x)
f1.write(s)

    
