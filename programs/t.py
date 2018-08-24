import urllib2
from bs4 import BeautifulSoup
import requests
link="http://www.thenation.com"
#web_page = urllib2.urlopen(link,timeout=4)
#domain_name=link.split("http://")[1].split("/")[0]
try:
        #print domain_name
        #web_page = urllib2.urlopen(link,timeout=4)
        r = requests.get(link,timeout=4)
        web_page = r.content
        web_page = web_page.replace(r"<!DOCTYPE>", "")
        soup = BeautifulSoup(web_page)
        c=soup.find_all('a')
        output=""
        follow_element=0
        for e in c:
            #print e
            try:
                l=e['href']
                print l
                #if 'twitter.com' in l:
                #    print l

            except:
                #print 'error after parsing links'
                pass
except:
    pass
