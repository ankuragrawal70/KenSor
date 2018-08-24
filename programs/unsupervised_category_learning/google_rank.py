from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import category_ranking_search as c_search
import domain_to_category as d_category
#from machine_learning_programs import google_news_source_extraction
import threading
import requests
def check_for_special_char(s):
    for i in s:
        if i.isdigit() or i in " ?.!/;:#&+":
            return True
            break
    return False
def check_for_category(cat):
    if len(cat)>2 and len(cat)<20 and check_for_special_char(cat) is not True:
        return True
    else:
        return False
def domain_name_distri(url):
    try:
        splitted=url.split('//')[1].split('/')
        domain_name='http://'+splitted[0]
        if domain_name in domain_distribution:
            domain_distribution[domain_name]=domain_distribution[domain_name]+1
        else:
            domain_distribution[domain_name]=1
        #splitt=url.split('/')

    except:
        #print 'errror in distribution'
        pass

#google links function extract links from the web pages for the news sources and fin next page links
def google_news_links(domain_name,category):
    try:
                str1="https://www.youtube.com/?gl=IN"
                str2="https://www.blogger.com/?tab=nj"
                driver = webdriver.Firefox()
                driver.get(domain_name)
                elem = driver.find_element_by_name("q")

                #emter category health and gives links for health category news sources
                elem.send_keys(category)
                elem.send_keys(Keys.RETURN)
                n_link=" "
                #links = driver.find_element_by_xpath("//a[@class='l _HId']")
                links = driver.find_elements_by_xpath("//*[@href]")
                for l in driver.find_elements_by_tag_name('a'):
                    li=l.get_attribute("href")
                    li=str(li)
                    #print str(li)
                    strg="google"
                    if strg in li:
                        pass
                    else:
                        #print 'link us',li
                        if li==str1 or li==str2:
                            pass
                        else:
                            if li not in news_links:
                                news_links.append(li.encode('utf-8'))
                            try:
                                domain_name_distri(li)
                            except:
                                pass
                n_link=driver.find_element_by_class_name("pn")
                n_link=n_link.get_attribute("href")
                print 'next page link is',n_link
                n_link=str(n_link)
                next_page_links(n_link)
                #links=driver.find_element_by_class_name("l _HId")
                #print links
                #next_page_links(x)
                #return n_link
                driver.close()

                #return n_link
    except:
        print 'error'

#next page links is called recursively to get next page link as all links are not occupied on one page
def next_page_links(link):
    try:
                if len(news_links)>20:
                    return
                driver = webdriver.Firefox()
                driver.get(link)
                elem = driver.find_element_by_name("q")
                links = driver.find_elements_by_xpath("//*[@href]")

                #str1 and str2 links are to be avoided
                str1="https://www.youtube.com/?gl=IN"
                str2="https://www.blogger.com/?tab=nj"
                for l in driver.find_elements_by_tag_name('a'):
                    li=l.get_attribute("href")
                    li=str(li)
                    #print str(li)
                    strg="google"
                    if strg in li:
                        pass
                    else:
                        #print 'link us',li
                        if li==str1 or li==str2:
                            pass
                        else:
                            if li not in news_links:
                                news_links.append(li.encode('utf-8'))
                            try:
                                domain_name_distri(li)
                            except:
                                pass
                n_link=driver.find_element_by_class_name("pn")
                n_link=n_link.get_attribute("href")
                print 'next page link is',n_link
                n_link=str(n_link)
                next_page_links(n_link)

                driver.close()
    except:
        print 'error'
def extract_headlines(link):
    try :
        #print link
        output=""
        #domain_name=link.split("http://")[1].split("/")[0]
        #print domain_name
        #web_page = urllib2.urlopen(link,timeout=4)
        r = requests.get(link,timeout=4)
        web_page = r.content
        web_page = web_page.replace(r"<!DOCTYPE>", "")
        soup = BeautifulSoup(web_page)

        print soup.title.string

    except:
        pass
top_200=[]
avl_souce=[]
def main_sources():
    gdelt_path='D://Thesis//data//domain_name//category_gdelt_valid_source//'
    file_list=os.listdir(gdelt_path)
    for e in file_list:
        e="http://"+e.rstrip(".txt")
        avl_souce.append(e)
    gdelt_path='D://Thesis//data//domain_name//gdelt_heuristic_approach_1//'
    file_list=os.listdir(gdelt_path)
    for e in file_list:
        e="http://"+e.rstrip(".txt")
        avl_souce.append(e)
    sp_path="D://Thesis//data//domain_name//machine_1_special_categories//sources.txt"
    f=open(sp_path,"r")
    temp=f.read().split("\n")
    for dom in temp:
        avl_souce.append(dom)
def compare_with_top_200():
    world_ranking="D://Thesis//data//domain_name//news_sources_ranking//based_on_4inm_website//"
    direc=os.listdir(world_ranking)
    r_sources=[]
    ranked_sources=[]
    for i in range(14,15):
        print direc[i]
        f=open(world_ranking+direc[i],'r')

    #ranked_sources are 200 sources containing global ranking
        #top_200.append(
        top= f.read().split("\n")
        for e in top:
            if e in avl_souce:
                top_200.append(e)

        #print top_200
        f.close()
        #print r_sources
    #for sou in r_sources:
    #    ranked_sources=ranked_sources+sou
#program starts here
main_sources()
#print avl_souce
#compare_with_top_200()
#print top_200
news_links=[]

#domain_distribution dictionay contains domains information in top 100 urls
domain_distribution={}

#url distribution contains urls that are being processed
url_distribution={}
#here the google news url is there
url="http://news.google.co.in/"
user_query="business"
z=google_news_links(url,user_query)
#print len(news_links)
#for element in news_links:
#    try:
#        print element
#    except:
#        pass
category_path=[]
ranking_domain={}
for i in range(0,10):
    url=news_links[i]
    print url
    try:
        #doma_name=url.split("http://")[1].split("/")
        #print doma_name
        slice_path=url.split("http://")[1].split("/")
        print slice_path
        cat_path=""+slice_path[0]
        for i in range(1,len(slice_path)):
            if check_for_category(slice_path[i]):
                cat_path=cat_path+"/"+slice_path[i]
        category_path.append(cat_path)
        extract_headlines(news_links[i])
    except:
        pass

children=d_category.result(user_query)
childs=children[0].split("\n")
similiar_cat=children[3].split("\n")
print similiar_cat

#printing category path for google news
for e in category_path:
    print e
local_ranking=c_search.find_categories(user_query)
for i in range(0,len(childs)):
    temp_ranking_map=c_search.find_categories(childs[i])
    for e in temp_ranking_map:
        if user_query in e and childs[i] in e:
            #print "hello"
            if e not in local_ranking:
                local_ranking[e]=temp_ranking_map[e]
for i in range(0,len(similiar_cat)):
    temp_ranking_map=c_search.find_categories(similiar_cat[i])
    for e in temp_ranking_map:
            #print "hello"
            if e not in local_ranking:
                local_ranking[e]=temp_ranking_map[e]
local_source_ranking=sorted(local_ranking, key = lambda item: local_ranking[item].score,reverse=True)
print "total ranked sources are",len(local_ranking)
in_top_of_world=0
for i in range(0,len(local_source_ranking)):
    if i>=len(local_source_ranking):
        break
    e=local_source_ranking[i]
    domain="http://"+e.split("http://")[1].split("/")[0]
    #print e,domain
    #if domain in top_200 and domain not in ranking_domain:
    #    in_top_of_world=in_top_of_world+1
    if domain not in ranking_domain:
            ranking_domain[domain]=e
    print e," ",local_ranking[e].traffic_imp," ",local_ranking[e].social_media," ",local_ranking[e].ar_freshness," ",local_ranking[e].score

print "length of available sources",len(top_200)
print "availabe in top 200 are",in_top_of_world


count=0
length=0
# domain distribution contains google page links
for e in domain_distribution:
    #print e,domain_distribution[e]
    if e in avl_souce:
        length=length+1
        if e in ranking_domain:
            count=count+1
            print "available",e
        else:
            print "not available",e
print length
print count