from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import threading
import os
def execution(list1,id1):


    for domain_name in list1:

        try:
            driver = webdriver.Firefox()
            driver.get("http://www.dmoz.com")
            name=''
            if 'http://' in domain_name:
                            name=domain_name[7:]
            else:
                            name=domain_name
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
                        path1='D://Thesis//data//domain_name//sources_in_dmoz//'
                        if len(str1)>0:
                            f=open(path1+name+'.txt','w')
                            f.write(str1)
                            f.close()
                            print 'completed',domain_name,id1
                            break
               if flag==1:
                    break
            if flag==0:
                path2='D://Thesis//data//domain_name//source_not_in _dmoz//unavailable_sources.txt'
                f1=open(path2,'a+')
                f1.write(domain_name+'\n')
                f1.close()
                print 'not found in dmoz',domain_name,id1
            #print 'completed ',domain_name,id1
            driver.close()
        except:
            path3='D://Thesis//data//domain_name//source_not_in _dmoz//invalid1.txt'
            f2=open(path3,'a+')
            f2.write(domain_name+'\n')
            f2.close()
            print 'url not valid',domain_name,id1

d_path1="D://Thesis//data//domain_name//category_gdelt_valid_source//"


# now running again as some error occured
path1='D://Thesis//data//domain_name//source_not_in _dmoz//invalid.txt'

"""x=os.listdir(d_path1)
e=[]
for a in x:
    el=a.rstrip('.txt')
    e.append(el)"""
"""for e in dir1:
f=open(d_path1,'r')
e=f.read().split('\n')"""
f=open(path1,'r')
info=f.read().split('\n')
print 'total available',len(info)
"""in_path='D://Thesis//data//domain_name//gdelt_heuristic_approach_1//'
info=os.listdir(in_path)"""
# path to check weather processed in unavailable
temp_path='D://Thesis//data//domain_name//source_not_in _dmoz//unavailable_sources.txt'
f2=open(temp_path,'r')
temp_list=f2.read().split('\n')
print 'not in dmoz till now',len(temp_list)
temp_path1='D://Thesis//data//domain_name//sources_in_dmoz//'
directory=os.listdir(temp_path1)
print 'total processed till now',len(directory)


e=[]
domain_list=[]
for element in info:
    #element=x.rstrip('.txt')
    if element not in directory and element not in temp_list:
        e.append(element)
print 'remaining to proceed sources', len(e)

del temp_list
del directory
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
        t=threading.Thread(target=execution, args = (element,id1,))
        j=j+1
        #t.daemon=True
        t.start()
