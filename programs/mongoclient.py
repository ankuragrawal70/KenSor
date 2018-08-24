from pymongo import MongoClient
import csv
import os
import thread
import time
import threading
import geoip2.database
import socket

def check_for_special_char(s):
    for i in s:
        if i.isdigit() or i in " ?.!/;:":
            return True
            break
    return False       
def check_for_category(cat):
    if len(cat)>3 and len(cat)<20 and check_for_special_char(cat)is not True:
        return True
    else:
        return False
def category_domain_info(threadName,url,category):
    path= "D://Thesis//data//category_data//url_info2.CSV"
    b=open(path,"rb")
    print "into open"
    reader1 = csv.reader(b,delimiter='\t')
    url_list=list(reader1)
    for element in url_list:
        #split each url by / to get category
        print element
        splitted_url=element.split("/")
        length=len(splitted_url)
        if length>1:
            dom=splitted_url[2]
            #print dom
            for i in range(3,len(splitted_url)):
                y=splitted_url[i].strip("")
                if check_for_category(y):
                    if category.has_key(y):
                        domain_hash=category[y]
                        if domain_hash.has_key(dom):
                            domain_hash[dom]=domain_hash[dom]+1
                            category[y]=domain_hash
                        else:
                            domain_hash[dom]=1
                    else:
                        domain_for_category={}
                        domain_for_category[dom]=1
                        category[y]=domain_for_category
    
    for element in category:
            print "\n" ,element,"\n news sources are  ",category[element]
def url_reader(threadName,url):
    """#location of list of urls in the record
    path= "D://Thesis//data//category_data//url_info2.CSV"
    b=open(path,"wb")
    c=csv.writer(b,delimiter='\t')"""
    #client = MongoClient('mongodb://localhost:27017/')
    client = MongoClient()
    db = client.test_database
    docs=db.docs
    collection = db.test_collection   
    path="D://Thesis//data//"
    filename=os.listdir(path)
    #print len(filename)
    for i in range(0,len(filename)):
        file1=path+filename[i]
        #print file1
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
            domain_name=row1[x-1]
            #print isinstance(domain_name, str)
            x=domain_name.replace('.','_')
            #print domain_name
            #print domain_name
            #try:
            cursor=docs.find({ x : {"$exists" : 1 } })
            if cursor.count()>0:
                print "hello"
                pass
            else:
                #url[domain_name]=1
                doc={x:1}
                doc_id=docs.insert(doc)

                print doc_id
                    
            #except:
             #   pass
        print "\ndate",ac_date
        #print "toal urls\n",len(url)
        #print "\ttotal unique urls are",len(url)
        #print "\t total file procees are\t",i 


"""def category_domain_info(threadName,url,category):
    for element in url:
        #split each url by / to get category
        splitted_url=element.split("/")
        length=len(splitted_url)
        if length>1:
            dom=splitted_url[2] 
            for i in range(3,len(splitted_url)):
                y=splitted_url[i].strip("")
                if check_for_category(y):
                    if category.has_key(y):
                        domain_hash=category[y]
                        if domain_hash.has_key(dom):
                            domain_hash[dom]=domain_hash[dom]+1
                            category[y]=domain_hash
                        else:
                            domain_hash[dom]=1
                    else:
                        domain_for_category={}
                        domain_for_category[dom]=1
                        category[y]=domain_for_category
    
    for element in category:
            print "\n" ,element,"\n news sources are  ",category[element]"""
   
    
        
url={}
category={}
domain={}


url_reader("url reader",url)
        #category_domain_info,("main thread",url,category)
        #thread.start_new_thread(url_reader,("url reader",url))
        #time.sleep(4)
        #thread.start_new_thread(category_domain_info,("main thread",url,category))
        #thread.start_new_thread(domain_location,("main thread",url,domain))

