import urllib2
import MySQLdb
import pickle
import datetime
import socket
import thread
import requests
import threading
import doctest
import os
from time import gmtime, strftime
from bs4 import BeautifulSoup
from multiprocessing import Process
def check_validity(h,level,domain_name):
    h_link=''
    if 'www.' in h:
        i=h.find('www.')
        #print 'i is',i
        h_link=h[0:i]+h[i+4:]
    else:
        h_link=h
    #print h_link
    #print h_link,domain_name
    if domain_name in h_link:
        #print 'yes'
        cate=h_link.encode('utf-8')
        category_url=cate+'\n'
        #print category_url
        if level.has_key(category_url):
            level[category_url]=level[category_url]+1
        else:
            level[category_url]=1

    else:
        #print 'yes'
        if h_link[0]=='/':
            if domain_name[len(domain_name)-1]!='/':
                c=(domain_name+h_link+'\n').encode('utf-8')
                #if h_link=='/news/regions/middle-east/iran':
                #         print 'found category'
                #         print c
                if level.has_key(c):
                    level[c]=level[c]+1
                else:
                    level[c]=1
            else:
                l=len(domain_name)-1
                x=domain_name[:l]
                c_link=(x+h_link+'\n').encode('utf-8')
                if level.has_key(c_link):
                    level[c_link]=level[c_link]+1
                else:
                    level[c_link]=1
def find_links(link,level,d_name):
    #print domain_name
    domain_name=d_name
    if 'www.' in d_name:
        i=d_name.find('www.')
        #print 'i is',i
        domain_name=d_name[0:i]+d_name[i+4:]
    else:
        domain_name=d_name
    #print "domain name after checking",domain_name
    #print 'domain name is',domain_name
    try :
        if "http://" not in link:
            r = requests.get("http://"+link,timeout=4)
        else:
            r=requests.get(link,timeout=4)
        web_page = r.content

        #web_page = urllib2.urlopen(link,timeout=4)
        #print "hello1"
        soup = BeautifulSoup(web_page)
        c=soup.find_all('a')
        #print "hello"
        for e in c:
            try:
                l=e['href']
                if l!=link:
                    check_validity(l,level,domain_name)
            except:
                #print 'error after parsing links'
                pass

    except:
        print 'error in main link'

#def cat_domains(d):
def cat_domains(domain_name):
    #d='http://www.thehindu.com'

    level1={}
    result=[]
    #print 'given domain is',domain_name
    find_links(domain_name,level1,domain_name)
    print "length is",len(level1)
    #print level1
    x=level1.keys()
    x.sort(key = lambda s: len(s),reverse=True)
    url_count=0
    if len(x)>4:
        url_count=5
    else:
        url_count=len(x)

    #print 'url_count is',url_count
    if len(x)>9:
        for i in range(0,10):
            #print 'checking urls are',x[i]
            find_links(x[i],level1,domain_name)
    else:
            for i in range(0,len(x)):
                #print 'checking urls are',x[i]
                find_links(x[i],level1,domain_name)
    for k,v in level1.items():
            if v>=(url_count-1):
                result.append(k)
                #print k
    #for e in result:
    #    print e
    return result
    
#cat_domains('http://www.globalpost.com')

def execution(list1,id):
    path="D://Thesis//data//domain_name//gdelt_heuristic_approach//fraesh_processed//"
    for s in list1:
        print "source is",s
        try:
            x=cat_domains(s)
            #print x
            re=''.join(x)
            print re
            name=s.lstrip("http://")
            if len(re)>0:
                print "saved sources are",path+name+".txt"
                f=open(path+name+'.txt','w')
                f.write(re)
                f.close()
                #write into completed file
                path5="D://Thesis//data//domain_name//gdelt_heuristic_approach//process//processed.txt"
                proc=open(path5,"a+")
                proc.write(s+"\n")
                proc.close()
                print "processed is",s
            else:
                print 'not found'
                """no_cat_path="D://Thesis//data//domain_name//special_sources_not_in_gdelt//output//"
                f1=open(no_cat_path+'file.txt','a+')
                f1.write(s+'\n')
                f1.close()"""
            #print s,'is completed thread is',id
        except:

            #print 'error'
            continue


        #print s
if __name__=='__main__':
    #input path which contains the data
    e=['http://www.nytimes.com','http://www.newsweek.com','http://www.usatoday.com','http://www.washingtonpost.com','http://www.supersport.com','http://blogs.economictimes.indiatimes.com','http://www.scientificamerican.com','http://www.edition.cnn.com','http://www.theage.com.au','http://www.reuters.com','http://abcnews.go.com','http://www.bostonglobe.com','http://www.independent.co.uk','http://www.safc.com','http://www.nation.co.ke']
    #e=['http://timesofindia.indiatimes.com']
    t=[]
    d_path1="D://Thesis//data//domain_name//category_gdelt_valid_source//"
    t=os.listdir(d_path1)
    #print regions
    """for ele in regions:
        path_final=d_path1+ele
        f=open(path_final,'r')
        temp_list=f.read().split('\n')
        t=t+temp_list"""

    #already processed
    path2="D://Thesis//data//domain_name//gdelt_heuristic_approach//"
    files=os.listdir(path2)

    # destination path to check if file has already been processed or not
    path1="D://Thesis//data//domain_name//gdelt_heuristic_approach//process//processed.txt"
    file_p=open(path1,"r")
    processed_files=file_p.read().split("\n")
    #for fi in t:
    #    if fi.rstrip(".txt") not in processed_files and fi.rstrip(".txt") not in files:
    #        e.append(fi.rstrip(".txt"))

    domain_list=[]

    i=0
    while 1:
        if (i+5)<len(e):
           j=i+5
           list1=e[i:j]
           domain_list.append(list1)
           i=j
        else:
            j=i+len(e)-1
            list1=e[i:j]
            domain_list.append(list1)
            break
    j=0
    for el in domain_list:
        print len(el)

    for element in domain_list:
        id1=j+1
        t=threading.Thread(target=execution, args = (element,id1,))
        j=j+1
        #t.daemon=True
        t.start()
#execution(['http://indianexpress.com'],1)
    

    



