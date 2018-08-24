import urllib2
import MySQLdb
import datetime
import socket
from time import gmtime, strftime
from bs4 import BeautifulSoup

def check_validity(h_link,domain_name,level):
    if domain_name in h_link:
            level[h_link]=1
    else:
        if h_link[0]=='/':
            level[domain_name+h_link]=1
def find_links(domain_name,level):
    try :      
        web_page = urllib2.urlopen(domain_name,timeout=4)
        soup = BeautifulSoup(web_page)
        c=soup.find_all('a')
        for e in c:
            #print e
            try:
                l=e['href']
                if l!=domain_name:
                    check_validity(l,domain_name,level)
            except:
                print 'error after parsing links'
                pass
   
    except:
        print 'error in main link'
        pass

def fill_level1(d_name,a):
    db = MySQLdb.connect("localhost",user="root",db="unsupervised_category_identfication")
    cursor = db.cursor()
    for source in level1:
        #print source
        sql="select * from level_1 where category_link='%s'"%(source)
        try:
            cursor.execute(sql)
            result=cursor.fetchone()
            #r=list(result)
            if result:
                c=result[2]+1
                sql1="update level_1 set count='%s' where category_link='%s'"%(c,source)
                try:
                    cursor.execute(sql1)
                    db.commit()
                except:
                    print 'error in updation'
                    db.rollback()
            else:
                c=1
                sql1=("INSERT INTO level_1(domain_name,category_link,count,start_time) VALUES('%s','%s','%s','%s')" %(d_name, source,c,a))
                try:
                    cursor.execute(sql1)
                    db.commit()
                except:
                    print 'error in updation'
                    db.rollback()
            #parent_list=list(result)
        except:
            print "error in selection"
def fill_level2(d_name,l1_link,a):
    db = MySQLdb.connect("localhost",user="root",db="unsupervised_category_identfication")
    cursor = db.cursor()
    for source in level2:
        sql="select * from level_2 where category_link='%s'"%(source)
        try:
            cursor.execute(sql)            
            result=cursor.fetchone()
            if result:
                print 'finding in database'
                c=result[1]+1
                sql1="update level_2 set count='%s' where category_link='%s'"%(c,source)
                try:
                    cursor.execute(sql1)
                    db.commit()
                except:
                    print 'error in updation'
                    db.rollback()
            else:
                c=1
                sql1=("INSERT INTO level_2(category_link,count,start_time,level_1_source,domain_name) VALUES('%s','%s','%s','%s','%s')" %(source,c,a,l1_link,d_name))
                try:
                    cursor.execute(sql1)
                    db.commit()
                except:
                    print 'error in updation'
                    db.rollback()
            #parent_list=list(result)
        except:
            print "error in selection"
    
"""def fill_level3(d_name,l2_name,a):
    db = MySQLdb.connect("localhost",user="root",db="unsupervised_category_identfication")
    cursor = db.cursor()
    for source in level3:
        sql="select * from level_3 where category_link='%s'"%(source)
        try:
            cursor.execute(sql)            
            result=cursor.fetchone()
            if result:
                print 'in updation'
                c=result[1]+1
                sql1="update level_3 set count='%s' where category_link='%s'"%(c,source)
                try:
                    cursor.execute(sql1)
                    db.commit()
                except:
                    print 'error in updation'
                    db.rollback()
            else:
                c=1
                print 'in insert'
                sql1=("INSERT INTO level_3(category_link,count,start_time,level_1_source,domain_name) VALUES('%s','%s','%s','%s','%s')" %(source,c,a,l2_name,d_name))
                try:
                    cursor.execute(sql1)
                    db.commit()
                except:
                    print 'error in updation'
                    db.rollback()
            #parent_list=list(result)
        except:
            print "error in selection"""
level1={}
#global_level2={}
level2={}
global_level_3={}
level3={}
domain_name="http://au.news.yahoo.com"
find_links(domain_name,level1)
a=strftime("%Y-%m-%d %H:%M:%S", gmtime())
fill_level1(domain_name,a)
for e in level1:
    if domain_name not in e:
        l1_link=domain_name+e
    else:
        l1_link=e
    print 'link is',l1_link
    find_links(l1_link,level2)
    #a = datetime.datetime.strptime('my date', "%b %d %Y %H:%M")
    a=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    fill_level2(domain_name,l1_link,a)
    #print 'length of level 2 is',len(level2)
    #break
    #global_level2.update(level2)
    #print 'length of global_level 2 is',len(global_level2)
    level2.clear()
    #print 'length of level 2 after deletion is',len(level2)

"""for el in global_level2:
#for el in level1:
    if domain_name not in el:
        l2_link=domain_name+el
    else:
        l2_link=el
    print 'level 2 link is',l2_link
    find_links(l2_link,level3)
    #a = datetime.datetime.strptime('my date', "%b %d %Y %H:%M")
    a=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    fill_level3(domain_name,l2_link,a)
    level3.clear()"""


