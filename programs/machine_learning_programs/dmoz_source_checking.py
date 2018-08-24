from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import threading
import os
def execution(list1):
    for domain_name in list1:

        try:
            driver = webdriver.Firefox()
            driver.get("http://www.dmoz.com")
            """name=''
            if 'http://' in domain_name:
                            name=domain_name[7:]
            else:
                            name=domain_name"""
            elem = driver.find_element_by_name("q")
            elem.send_keys(domain_name)
            elem.send_keys(Keys.RETURN)
            soup = BeautifulSoup(driver.page_source)
            c=soup.findChildren("ol", { "class" : "dir" })
            str1=""
            for item in c:
               for link in item.find_all('a'):
                   str1=str1+link.get('href')+'\n'

            d=soup.findChildren("ol", { "class" : "site" })
            flag=0
            for i in d:
               for link in i.find_all('a'):
                   x=link.get('href')
                   if domain_name in x or x in domain_name:
                        flag=1
                        #path1='D://Thesis//data//domain_name//sources_in_dmoz//'
                        if len(str1)>0:
                            #f=open(path1+name+'.txt','w')
                            #f.write(str1)
                            #f.close()
                            print str1
                            print 'completed',domain_name
                            break
               if flag==1:
                    break
            if flag==0:
                print 'not found in dmoz',domain_name
            #print 'completed ',domain_name,id1
            driver.close()
        except:

            print 'url not valid',domain_name,id1

list1=["http://www.thehindu.com","http://timesofindia.indiatimes.com","indianexpress.com","businessinsider.com"]
#list1=["sports"]

#list1 contains list of urls which are to be checked if they are present in "http://www,dmoz.org" web directory or not and finding categories for those news sources
execution(list1)
# now running again as some error occured


