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
import locale
import facebook
from time import gmtime, strftime
from bs4 import BeautifulSoup
#locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
#web_page = urllib2.urlopen(link,timeout=4)
#domain_name=link.split("http://")[1].split("/")[0]
def find_twitter_data(link):
    try:
        #print domain_name
        #web_page = urllib2.urlopen(link,timeout=4)
        r = requests.get(link,timeout=4)
        web_page = r.content
        web_page = web_page.replace(r"<!DOCTYPE>", "")
        soup = BeautifulSoup(web_page)
        c=soup.find_all('a')
        stats=[-1,-1,-1,-1]
        for e in c:
            try:
                c_link=e['data-nav']
                if c_link=="followers":
                    #mydivs = e.findAll("span", { "class" : "ProfileNav-value" })
                    folowers=e['title'].split(" ")[0]
                    print 'followers are',folowers
                    stats[0]=int(folowers.replace(',',''))

                if c_link=="following":
                    following=e['title'].split(" ")[0]
                    print 'following are',following
                    stats[1]=int(following.replace(',',''))
                if c_link=="tweets":
                    tweets=e['title'].split(" ")[0]
                    print 'tweets are',tweets
                    stats[2]=int(tweets.replace(',',''))
                if c_link=="favorites":
                    #print e
                    favourite=e['title'].split(" ")[0]
                    print 'favourite are',favourite
                    stats[3]=int(favourite.replace(',',''))
            except:
                #print 'error after parsing links'
                pass
        """if all(len(v) ==0 for v in stats):
            div=soup.find_all("div")
            print div"""
        return stats

    except:
        pass


def find_links(link):
    try :

        r = requests.get(link,timeout=4)
        web_page = r.content
        web_page = web_page.replace(r"<!DOCTYPE>", "")
        soup = BeautifulSoup(web_page)
        c=soup.find_all('a')
        for e in c:
            try:
                l=e['href']
                #print l

                if l not in sources_processed:
                    if "twitter.com/" in l and len(l)<150:
                            print l
                            #find_twitter_data method return strings containing twitter data
                            twitter_stats=find_twitter_data(l)
                            #print twitter_stats
                            #print "statistics is ","\n".join(twitter_stats)
                            if all(v==-1 for v in twitter_stats):
                                print link, 'not found twitter link'
                                check_path="D://Thesis//data//domain_name//twitter_information_sources//not_available.txt"
                                f1=open(check_path,'a+')
                                f1.write(link+'\n')
                                f1.close()

                            else:

                                    db = MySQLdb.connect("localhost",user="root",db="web_categorization")
                                    cursor = db.cursor()
                                    sql = ("INSERT INTO twitter_info(domain_name,twitter_url,followers,following,tweets,favourates) VALUES('%s','%s','%s','%s','%s','%s')" %(link, l,(twitter_stats[0]),(twitter_stats[1]),(twitter_stats[2]),(twitter_stats[3])))
                                    try:
                                        cursor.execute(sql)
                                        print 'after insertion'
                                        db.commit()
                                    except:
                                        print "error in insertion"
                                        db.rollback()
                                    sources_processed[l]=0
                                    #print 'after insertion'
                                    processed="D://Thesis//data//domain_name//twitter_information_sources//completed.txt"
                                    f=open(processed,'a+')
                                    f.write(link+'\n')
                                    f.close()

            except:
                #print 'error after parsing links'
                pass

    except:
        print 'error in main link'
        print link, 'not found twitter link'
        check_path="D://Thesis//data//domain_name//twitter_information_sources//not_available.txt"
        f1=open(check_path,'a+')
        f1.write(link+'\n')
        f1.close()

sources_processed={}
completed_domains={}
#find_links("http://www.timesofindia.indiatimes.com")
def execution(list1,t_id):
    for element in list1:
        if element not in completed_domains:
            find_links(element)
            print "processed",element,t_id
            completed_domains[element]=1


def gdelt_source_fetcher():

        #gdelt_path='D://Thesis//data//domain_name//category_gdelt_valid_source//'
        #gdelt_path="D://Thesis//data//domain_name//gdelt_heuristic_approach_1//"
        #gdelt_path='D://Thesis//data//domain_name//special_sources_not_in_gdelt//output//'
        gdelt_path="D://Thesis//data//domain_name//news_sources_ranking//based_on_4inm_website//top_200_news_sources_world.txt"
        #file_list=os.listdir(gdelt_path)
        f_sou=open(gdelt_path,"r")
        file_list=f_sou.read().split("\n")
        #print len(file_list)"""


        check_path="D://Thesis//data//domain_name//twitter_information_sources//not_available.txt"
        f2=open(check_path,'r')
        temp_list=f2.read().split("\n")
        f2.close()

        process_list=[]
        processed="D://Thesis//data//domain_name//twitter_information_sources//completed.txt"
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
            element=f_name
            #element='http://'+f_name.rstrip('.txt')
            if element not in temp_list and element not in process_list:
                #f_name='http://'+element.rstrip('.txt')
                #if element=="http://www.timesofindia.indiatimes.com":
                #    print element
                e.append(element)
        print 'remaining to proceed sources', len(e)

        del temp_list[:]
        del file_list[:]
        del process_list[:]
        i=0#
        while 1:
                if (i+200)<len(e):
                   j=i+200
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
                t=threading.Thread(target=execution, args = (element,id1,))
                j=j+1
                #t.daemon=True
                t.start()
#find_twitter_data(link)
gdelt_source_fetcher()