import csv
import os
import thread
import time
import threading
import geoip2.database
import socket
import sys
def check_for_special_char(s):
    for i in s:
        if i.isdigit() or i in " ?.!/;:":
            return True
            break
    return False
"""def location(hostname):
        list1=[]
        try:
            addr = socket.gethostbyname(hostname)
            reader = geoip2.database.Reader('D:/Thesis/GeoLite2-City.mmdb/home/tjmather/mm_website/geoip/BuildDatabase/GeoLite2-City.mmdb')
            #reader = geoip2.database.Reader("D:/Thesis/GeoLite2-Country.mmdb/home/tjmather/mm_website/geoip/BuildDatabase/GeoLite2-Country.mmdb")
            response = reader.city(addr)
            if response.country.name is not  None:
                list1.append(response.country.name.encode("utf-8"))
            else:
                list1.append(response.country.name)
            list1.append(response.city.name)
            list1.append(response.postal.code)
            list1.append(response.location.latitude)
            list1.append(response.location.longitude)
        except:
            pass
        
        return list1 """           
def check_for_category(cat):
    if len(cat)>3 and len(cat)<20 and check_for_special_char(cat)is not True:
        return True
    else:
        return False
def url_reader(threadName,url):
    #location of list of urls in the record

    #path= "D://Thesis//data//category_data//url_info2.CSV"
    #b=open(path,"wb")
    #c=csv.writer(b,delimiter='\t')
    #.writerow(["Date   ","total_url   ","total_categories"])
    #input data location
    path="D://Thesis//data//"
    #path="D://Thesis//data//New folder//"
    filename=os.listdir(path)
    for i in range(275,len(filename)):
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
            domain_name=row1[x-1]
            #print domain_name
            if url.has_key(domain_name):
                    url[domain_name]=url[domain_name]+1
            else:
                    url[domain_name]=1
                    category_domain_info(domain_name,category)
                    #c.writerow(domain_name)
            
        print "\ndate",ac_date
        print "toal urls\n",len(url)
        print "\ttotal unique urls are",len(url)
        print "\t total file procees are\t",i 
"""def domain_location(threadName,url,domain):
    for element in url:
        #print element
        #split each url by / to get category
        splitted_url=element.split("/")
        length=len(splitted_url)
        if length>1:
            dom=splitted_url[2] 
            if domain.has_key(dom):
                #domain[dom]=domain[dom]+1
                pass
            else:
                loc_list=location(dom)
                domain[dom]=loc_list
                print "for \n",dom," location is",loc_list,"\n"""
def category_domain_info(element,category):
    #path= "D://Thesis//data//category_data//url_info2.CSV"
    #b=open(path,"rb")
    #print "into open"
    #reader1 = csv.reader(b,delimiter='\t')
    #url_list=list(reader1)
    #for element in url:
        #split each url by / to get category
        #print element
        splitted_url=element.split("/")
        length=len(splitted_url)
        if length>1:
            try:
                
                dom=splitted_url[2]
                #print dom
                for i in range(3,len(splitted_url)):
                    y=splitted_url[i].strip("")
                    if check_for_category(y):
                        if category.has_key(y):
                            #category[y]=category[y]+1
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
                            #category[y]=1
            except:
                pass
                

       
def remove_redundant_category(category):
    for element in category.keys():
        url_set=category[element]
        if len(url_set)==1:
            flag=1
            for u in url_set:
                if url_set[u]==1:
                    #del url_set[u]
                    #del category[element]
                    flag=0
            if flag==0:
                del category[element]
    for element in category:
            print "\n" ,element,"\n news sources are  ",category[element]
 
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

#output path


#input path
"""path="D://Thesis//data//"
filename=os.listdir(path)
for i in range(0,2):
    file1=path+filename[i]
    f=open(file1,"rb")
    date=filename[i][:-11]
    ac_date=date[0:4]+"/"+date[4:6]+"/"+date[6:len(date)]
    reader1 = csv.reader(f,delimiter='\t')
    row=list(reader1)"""
url_reader("url reader",url)
#category_domain_info(url,category)
#remove_redundant_category(category)
path= "D://Thesis//data//New folder//category.CSV"
b=open(path,"wt")
c=csv.writer(b,delimiter=',')

#for element in category:
            #print "\n" ,element,"\n news sources are  ",category[element]
 #           c.writerow([element , category[element]])
b.close()

