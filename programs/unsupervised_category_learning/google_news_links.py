from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import threading
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
        """print splitted
        for i in range(0,len(splitted)):
            if check_for_category(splitted[i]):
                pass
            else:
                splitted.pop(i)
        print splitted"""
        """url_str=splitted[0]
        for e in splitted:
            if check_for_category(e):
                url_str=url_str+'/'+e
        try:
                print url_str
        except:
                pass
        if url_str not in url_distribution:
            url_distribution[url_str]=1"""
    except:
        print 'errror in distribution'
        pass
def google_news_links(domain_name):
    try:
                str1="https://www.youtube.com/?gl=IN"
                str2="https://www.blogger.com/?tab=nj"
                driver = webdriver.Firefox()
                driver.get(domain_name)
                elem = driver.find_element_by_name("q")
                elem.send_keys('health')
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

                """for link in links:
                    x=link.get_attribute("href")
                    y=link.get_attribute("id")
                    #print 'link is',x
                    if 'google' not in x:
                        x=str(x.encode('utf-8'))
                        if x==str1 or x==str2:
                            pass
                        else:
                            if x not in news_links:
                                news_links.append(x)
                                domain_name_distri(x)
                    if y=='pnnext':
                        print 'next link is', x"""
                        #next_page_links(x)
                #return n_link
                driver.close()

                #return n_link
    except:
        print 'error'

def next_page_links(link):
    try:
                if len(news_links)>500:
                    return
                driver = webdriver.Firefox()
                driver.get(link)
                elem = driver.find_element_by_name("q")
                links = driver.find_elements_by_xpath("//*[@href]")
                #links=driver.find_element_by_class_name("l _HId")
                #print links
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
                """for link in links:
                    x=link.get_attribute("href")
                    y=link.get_attribute("id")
                    print x
                    if 'google' not in x:
                        x=str(x.encode('utf-8'))
                        if x==str1 or x==str2:
                            pass
                        else:
                            if x not in news_links:
                                news_links.append(x)
                                domain_name_distri(x)
                    if y=='pnnext':
                        print x
                        next_page_links(x)"""
                driver.close()
    except:
        print 'error'
news_links=[]
domain_distribution={}
url_distribution={}
url="http://news.google.co.in/"
z=google_news_links(url)
#next_page_links(z)
#print 'hello'

print len(news_links)
for element in news_links:
    try:
        print element
    except:
        pass
for e in domain_distribution:
    print e,domain_distribution[e]
#for source in url_distribution:
#    print source
