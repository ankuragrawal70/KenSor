import csv
import os
import thread
import time
import threading
import geoip2.database
import socket
class category_node:
    def __init__(self,name):
        self.c_name=name
        self.parent=[]
        self.references={}
        self.news_sources={}
def check_for_special_char(s):
    for i in s:
        if i.isdigit() or i in " ?.!/;:":
            return True
            break
    return False
def check_for_category(cat):
    if len(cat)>4 and len(cat)<20 and check_for_special_char(cat)is not True:
        return True
    else:
        return False
def traversal(sp,output):
     print "category",sp.c_name
     #print sp.parent
     if len(sp.parent)==0:
         print "news sources in",sp.c_name
         #,"are",sp.news_sources
         #print "sub categories are\n"
         for element in sp.references:
             print "Sub_category :: " ,element
             #,"\nnews sources are",category[element].news_sources
             print "\n"
     else:
         print "\n parents category are"
         for element in sp.parent:
             print element.c_name
         #print "\n news sources in",sp.c_name
         #,"category are",sp.news_sources,"\n"
         #print "\nsub categories and news sources are\n"
         for element in sp.references:
             print "sub_category ::",element,
             #"\nnews sources are",category[element].news_sources
             print "\n"
def url_reader(threadName,url):
    #location of list of urls in the record

    #path= "D://Thesis//data//category_data//url_info2.CSV"
    #b=open(path,"wb")
    #c=csv.writer(b,delimiter='\t')
    #.writerow(["Date   ","total_url   ","total_categories"])
    #input data location
    path="D://Thesis//data//"
    filename=os.listdir(path)
    for i in range(275,475):
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
            if url.has_key(domain_name):
                    url[domain_name]=url[domain_name]+1
            else:
                    url[domain_name]=1
                    category_domain_info(domain_name)
                    #domain_category_info(domain_name)
                    #c.writerow(domain_name)
            
        print "\ndate",ac_date
        #print "toal urls\n",len(url)
        #print "\ttotal unique urls are",len(url)
        print "\t file procees are\t",i 

def category_domain_info(element):
        splitted_url=element.split("/")
        length=len(splitted_url)
        if length>1:
            dom=splitted_url[2]
            #print dom
            cat_list=[]
            for i in range(3,len(splitted_url)):
                y=splitted_url[i].strip("")
                if check_for_category(y):
                    #if y=="gadgets-news":
                     #   print "hello"
                    cat_list.append(y)
                    #print len(cat_list)
            #print cat_list
            for e in cat_list:
                if e=="gadgets-news":
                    print cat_list
            i=0
            while i<len(cat_list)-1:
                #temp_hash={}
                #if cat_list[i]=="gadgets-news":
                 #           print "hello"
                 
                if category.has_key(cat_list[i]):
                    ref=category[cat_list[i]]
                    if i==0:
                        if ref.news_sources.has_key(element):
                            ref.news_sources[element]=ref.news_sources[element]+1
                        
                        else:
                            ref.news_sources[element]=1
                            category[cat_list[i]]=ref
                        
                        
                    temp=ref.references                    
                    if temp.has_key(cat_list[i+1]):
                        #x=cat_list[i+1]+1
                        temp[cat_list[i+1]]=temp[cat_list[i+1]]+1
                        #temp[cat_list[i+1]]=x
                        category[cat_list[i]]=ref
                    else:
                        
                        temp[cat_list[i+1]]=1
                        if category.has_key(cat_list[i+1]):
                            x=category[cat_list[i+1]]
                            x.parent.append(category[cat_list[i]])
                            x.news_sources[element]=1
                            category[cat_list[i+1]]=x
                        else:
                            new_c=category_node(cat_list[i+1])
                            new_c.parent.append(category[cat_list[i]])
                            new_c.news_sources[element]=1
                            category[cat_list[i+1]]=new_c
                else:
                    #print "hello"
                    new_cat=category_node(cat_list[i])
                    new_cat.news_sources[element]=1
                    #print "c_name is",new_cat.c_name
                    #temp_hash=ref
                    category[cat_list[i]]=new_cat
                i=i+1
            """if len(cat_list)>1:               
                a=category[cat_list[i]]
                a.news_sources[dom]=1
                category[cat_list[i]]=a"""

    
            #for element in category:
             #    print element+"/",category[element]
           

   
    
        
url={}
category={}
domain={}
output=""
url_reader("url reader",url)
ca=""
while ca is not None:
    ca=raw_input("\n input the category you want to search for\n")
    if category.has_key(ca):
        sp=category[ca]
        traversal(sp,output)
    else:
        print "no category present of this kind"
#print category['gadgets'].news_sources
#print sp.c_name
#print sp.news_sources

#category_domain_info(url,category)
#remove_redundant_category(category)
    
    


