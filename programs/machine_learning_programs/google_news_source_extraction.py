from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from newspaper import Article
#from unsupervised_category_learning import category_ranking_search as c_search
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
def google_news_links(domain_name,category,news_links,domain_distribution):
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
                            if li.encode("utf-8") not in news_links:
                                news_links.append(li.encode('utf-8'))
                                try:
                                    domain_name_distri(li,domain_distribution)
                                except:
                                    pass
                n_link=driver.find_element_by_class_name("pn")
                n_link=n_link.get_attribute("href")
                print 'next page link is',n_link
                n_link=str(n_link)
                driver.close()
                next_page_links(n_link)


                #return n_link
    except:
        print 'error'

#next page links is called recursively to get next page link as all links are not occupied on one page
def next_page_links(link,news_links,domain_distribution):
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
                            if li.encode("utf-8") not in news_links:
                                news_links.append(li.encode('utf-8'))
                                try:
                                    domain_name_distri(li,domain_distribution)
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
        return
def extract_headlines(link):
    try :
        article=Article(link)
        article.download()
        article.parse()
        #print article.publish_date,"\n"
        #@print article.authors,"\n"
        #print article.title
        text=article.text
        v= article.title+"\n"+" ".join(text.split("\n"))
        return v
        #print article.text

    except:
        pass
#program starts here
#here the google news url is there
def query(user_query):
    news_links=[]
    domain_distribution={}
    url="http://news.google.co.in/"
    z=google_news_links(url,user_query,news_links,domain_distribution)
    print len(news_links)
    article_result=[]
    result=""
    for i in range(0,10):
        #print news_links[i]
        news_links[i]=news_links[i].decode("utf-8")
        if news_links[i]!='None':
            try:
                article=extract_headlines(news_links[i])
                result=result+news_links[i]+"\n"+article
                article_result.append(result)
            except:
                pass
    return article_result
    #for e in domain_distribution:
    #    print e,domain_distribution[e]

#query("business")

#local_ranking=c_search.find_categories(user_query)
#local_source_ranking=sorted(local_ranking, key = lambda item: local_ranking[item],reverse=True)
#for e in local_source_ranking:
#    print e,local_ranking[e]