from BeautifulSoup import BeautifulSoup
import urllib
import re
import copy
path="http://data.gdeltproject.org/events/"
testfile = urllib.URLopener()
html_page = urllib.urlopen("http://data.gdeltproject.org/events/index.html")
soup = BeautifulSoup(html_page)
link=soup.findAll('a')
del link[0]
del link[1]
del link[2]
del link[3]
#link2=link[200:]
for i in range(0,101):
    x=link[i]["href"]
    y=path+x
    print y
    testfile.retrieve(y,"D://Thesis//data_gdelt//"+x)



    
#testfile = urllib.URLopener()
