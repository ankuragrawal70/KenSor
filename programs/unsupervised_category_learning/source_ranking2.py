import csv
import os
import thread
import time
import threading
import geoip2.database
import socket
import csv
import MySQLdb
#import gexf
#mport networkx as nx
#import matplotlib.pyplot as plt
import sys
def url_reader(source_url):
    print source_url
    restrincted_domain=source_url.lstrip('http://').replace('/','#')
    print restrincted_domain
    domain="http://"+source_url.split("http://")[1].split("/")[0]
    #print domain
    try:

        path="D://Thesis//data//2015_data//"
        filename=os.listdir(path)
        i=0
        #i=271
        x=0
        #i=271
        while i<len(filename)-2:
                article_count=0
                ac_date=""
            #for i in range(400,len(filename)-2):
            #try:
                while x!=i+7:
                    file1=path+filename[x]
                    f=open(file1,"rb")
                    date=filename[x][:-11]
                    ac_date=date[0:4]+"/"+date[4:6]+"/"+date[6:len(date)]
                    print ac_date
                    reader1 = csv.reader(f,delimiter='\t')
                    row=list(reader1)
                    f.close()

                    #row is a set of rows of the given file
                    #url is a hash_map that contains the urls and their count
                    for row1 in row:
                        y=len(row1)
                        url_name=row1[y-1]

                        if domain in url_name and 'technology' in url_name:
                            print url_name
                            if url.has_key(url_name):
                                    pass
                            else:
                                    url[url_name]=1
                                    #category_domain_info(url_name)
                                    article_count=article_count+1
                                    #loc(domain_name)

                    print "\ndate",ac_date
                    #print "toal urls\n",len(url)
                    #print "\ttotal unique urls are",len(url)
                    print "\t file procees are\t",x
                    x=x+1
                i=i+7
                url.clear()
                print 'weekly articles are on date',article_count,"   ",ac_date+'\n'
                try:
                    stats_path="D://Thesis//data//domain_name//news_sources_ranking//based_on_data_frequency_change//technology//"+restrincted_domain+'.txt'
                    f2=open(stats_path,'a+')
                    f2.write(str(ac_date)+" "+str(article_count)+'\n')
                    f2.close()
                except:
                    pass
            #except:
            #    print 'error'
            #    pass
    except:
        print 'error'
        pass

def execution(list1,t_id):
    for source in list1:
        url_reader(source)
        print 'completed ',source,t_id

        #this will store the info of domains completed
        completed_path="D://Thesis//data//domain_name//news_sources_ranking//based_on_data_frequency_change//technology//completed//completed_source.txt"
        f_com=open(completed_path,'a+')
        f_com.write(source+'\n')
        f_com.close()
url={}


path="D://Thesis//data//domain_name//domains_related_to_a_category_all_1//"
#category_sources=os.listdir(path+'technology.txt')
f=open(path+"technology.txt",'r')
source_files=f.read().split("\n")
print len(source_files)

e=[]
#following path is used to access processed file and so ignoring completed urls
comp_path="D://Thesis//data//domain_name//news_sources_ranking//based_on_data_frequency_change//technology//completed//completed_source.txt"
c_des=open(comp_path,'r')
processed=c_des.read().split('\n')
domain_list=[]
#for sou in source_files:
#    url_reader(sou)

for element in source_files:
    if element not in processed:
        e.append(element)
"""i=0
while 1:
            if (i+300)<len(e):
                   j=i+300
                   list1=e[i:j]
                   domain_list.append(list1)
                   i=j
            else:
                    j=i+len(e)-1
                    list1=e[i:j]
                    domain_list.append(list1)
                    break
j=0

for x in domain_list:
    print len(x)
#url_reader('http://www.thehindu.com/business')
for element in domain_list:
                id1=j+1
                t=threading.Thread(target=execution, args = (element,id1,))
                j=j+1
                #t.daemon=True
                t.start()"""
print len(e)
for i in range(360,480):
    url_reader(e[i])
    completed_path="D://Thesis//data//domain_name//news_sources_ranking//based_on_data_frequency_change//technology//completed//completed_source.txt"
    f_com=open(completed_path,'a+')
    f_com.write(e[i]+'\n')
    f_com.close()
