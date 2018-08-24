import urllib2
import MySQLdb
import pickle
import datetime
import socket
import thread
import threading
import doctest
import os
import requests
import facebook
from time import gmtime, strftime
from bs4 import BeautifulSoup

def find_likes_visits(link,domain_name,source_processed):
    l=str(link)
    try:
        if l not in source_processed:
            graph = facebook.GraphAPI()
            page = graph.get_object(l)
            #print '{} {} has {} likes {} link {} as category.'.format(domain_name,page['name'], page['likes'],page['link'],page['category'])
            #print page['category_list']
            facebbok_page=page['name']
            likes=page['likes']
            print 'likes are',likes
            db = MySQLdb.connect("localhost",user="root",db="web_categorization")
            cursor = db.cursor()
            sql = ("INSERT INTO source_ranking(source_name,facebook_url,facebook_likes) VALUES('%s','%s','%s')" %(domain_name, l,likes))
            try:
                cursor.execute(sql)
                db.commit()
            except:
                print "error in insertion"
                db.rollback()
            source_processed[l]=0
            processed="D://Thesis//data//domain_name//facebook_likes_sources//sources_page_ranks.txt"
            f=open(processed,'a+')
            f.write(domain_name+'\n')
            f.close()
            #print 'visist counts',page['were_here_count']
            #print page ,'visits are ', page['website']
    except:
        print domain_name, 'not found facebook link'
        if l not in source_processed:
            check_path="D://Thesis//data//domain_name//facebook_likes_sources//not_available.txt"
            f1=open(check_path,'a+')
            f1.write(domain_name+'\n')
            f1.close()
        pass

def find_links(link,source_processed):
    #print domain_name
    """domain_name=d_name
    if 'www.' in d_name:
        i=d_name.find('www.')
        #print 'i is',i
        domain_name=d_name[0:i]+d_name[i+4:]
    else:
        domain_name=d_name"""
    #print 'domain name is',domain_name
    try :
        r = requests.get(link,timeout=4)
        web_page = r.content
        web_page = web_page.replace(r"<!DOCTYPE>", "")
        soup = BeautifulSoup(web_page)
        c=soup.find_all('a')
        for e in c:
            try:
                l=e['href']

                if "www.facebook.com" in l:
                    print l
                    if l in source_processed:
                        pass
                    else:
                        find_likes_visits(l,link,source_processed)

                #if l!=link:
                #    check_validity(l,level,domain_name)
            except:
                print 'error after parsing links'
                pass

    except:
        print 'error in main link'
        print link, 'not found facebook link'
        check_path="D://Thesis//data//domain_name//facebook_likes_sources//not_available.txt"
        f1=open(check_path,'a+')
        f1.write(link+'\n')
        f1.close()
        pass

def execution(list1,source_map,t_id):
    for element in list1:
        find_links(element,source_map)

#x={}
#execution(["http://www.popularmechanics.com/"],x,1)
def gdelt_source_fetcher():

        gdelt_path='D://Thesis//data//domain_name//category_gdelt_valid_source//'
        #gdelt_path="D://Thesis//data//domain_name//gdelt_heuristic_approach_1//"
        #gdelt_path='D://Thesis//data//domain_name//special_sources_not_in_gdelt//output//'
        file_list=os.listdir(gdelt_path)
        #print len(file_list)

        check_path="D://Thesis//data//domain_name//facebook_likes_sources//not_available.txt"
        f2=open(check_path,'r')
        temp_list=f2.read().split("\n")
        f2.close()

        process_list=[]
        processed="D://Thesis//data//domain_name//facebook_likes_sources//sources_page_ranks.txt"
        f3=open(processed,'r')
        process_list=f3.read().split('\n')
        #f1=open(processed,'r')
        #process_list=f.read().split(" ")
        #f1.close()
        e=[]
        sources_processed={}
        domain_list=[]
        for f_name in file_list:
            #element=x.rstrip('.txt')
            element='http://'+f_name.rstrip('.txt')
            if element not in temp_list and element not in process_list:
                #f_name='http://'+element.rstrip('.txt')
                e.append(element)
                if element=="http://www.thehindu.com":
                    print 'exist'
        print 'remaining to proceed sources', len(e)

        del temp_list[:]
        del file_list[:]
        del process_list[:]
        i=0
        while 1:
                if (i+1000)<len(e):
                   j=i+1000
                   list1=e[i:j]
                   domain_list.append(list1)
                   i=j
                else:
                    j=i+len(e)-1
                    list1=e[i:j]
                    domain_list.append(list1)
                    break
        j=0
        for b in domain_list:
            print len(b)
        for element in domain_list:
                id1=j+1
                t=threading.Thread(target=execution, args = (element,sources_processed,id1,))
                j=j+1
                #t.daemon=True
                t.start()

gdelt_source_fetcher()