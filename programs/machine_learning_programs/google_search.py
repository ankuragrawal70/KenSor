from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import category_ranking_search as c_search
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
    if len(cat)>2 and len(cat)<20 and check_for_category(cat) is not True:
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
#program starts here
news_links=[]

#domain_distribution dictionay contains domains information in top 100 urls
domain_distribution={}

#url distribution contains urls that are being processed
url_distribution={}
#here the google news url is there
url="http://news.google.co.in/"
user_query="business"
z=google_news_links(url,user_query)
print len(news_links)
#for element in news_links:
#    try:
#        print element
#    except:
#        pass

for i in range(0,10):
    print news_links[i]
    extract_headlines(news_links[i])
for e in domain_distribution:
    print e,domain_distribution[e]
local_ranking=c_search.find_categories(user_query)
local_source_ranking=sorted(local_ranking, key = lambda item: local_ranking[item],reverse=True)
for e in local_source_ranking:
    print e,local_ranking[e]

