import urllib2
import MySQLdb
import datetime
import socket
#import thread
import threading
from multiprocessing import Process
from time import gmtime, strftime
from bs4 import BeautifulSoup

def add_in_dict(d,level):
    if d not in level:
        level[d]=1
    else:
        pass
def check_validity(h_link,domain_name,level):
    if domain_name in h_link:
            level[h_link]=1
    else:
        if h_link[0]=='/':
            if domain_name[len(domain_name)-1]!='/':
                #level[domain_name+h_link]=1
                d=domain_name+h_link
                add_in_dict(d,level)
            else:
                l=len(domain_name)-1
                x=domain_name[:l]
                #level[x+h_link]=1
                d=x+h_link
                add_in_dict(d,level)
def find_links(domain_name,level):
    #print domain_name
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

def fill_level1(d_name,a,level1):
    db = MySQLdb.connect("localhost",user="root",db="temporary_category_classification")
    cursor = db.cursor()
    for source in level1:
        #print source
        sql="select * from level_1 where category_link='%s'"%(source)
        try:
            cursor.execute(sql)
            result=cursor.fetchone()
            #r=list(result)
            if result:
                print "finding in database level1"
                c=result[2]+1
                sql1="update level_1 set count='%s',recrawl_time='%s' where category_link='%s'"%(c,a,source)
                try:
                    cursor.execute(sql1)
                    db.commit()
                except:
                    print 'error in updation at level 1'
                    db.rollback()
            else:
                c=1
                sql1=("INSERT INTO level_1(domain_name,category_link,count,start_time) VALUES('%s','%s','%s','%s')" %(d_name, source,c,a))
                try:
                    cursor.execute(sql1)
                    db.commit()
                except:
                    print 'error in insertion at level 1'
                    db.rollback()
            #parent_list=list(result)
        except:
            print "error in selection level 1"
            pass
def fill_level2(d_name,l1_link,a,level2):
    db = MySQLdb.connect("localhost",user="root",db="temporary_category_classification")
    cursor = db.cursor()
    for source in level2:
        sql="select * from level_2 where category_link='%s'and level_1_source='%s'"%(source,l1_link)
        try:
            cursor.execute(sql)            
            result=cursor.fetchone()
            if result:
                print 'finding in database level2'
                c=result[1]+1
                sql1="update level_2 set count='%s',recrawl_time='%s' where category_link='%s' and level_1_source='%s'"%(c,a,source,l1_link)
                try:
                    cursor.execute(sql1)
                    db.commit()
                except:
                    print 'error in updation level 2'
                    db.rollback()
            else:
                c=1
                sql1=("INSERT INTO level_2(category_link,count,start_time,level_1_source,domain_name) VALUES('%s','%s','%s','%s','%s')" %(source,c,a,l1_link,d_name))
                try:
                    cursor.execute(sql1)
                    db.commit()
                except:
                    print 'error in insertion level 2'
                    db.rollback()
            #parent_list=list(result)
        except:
            print "error in selection level 2"
            pass
    
"""def fill_level3(d_name,l2_name,a):
    db = MySQLdb.connect("localhost",user="root",db="unsupervised_category_identification")
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

def execution(domains):
    c_path="D://Thesis//data//domain_name//completed2.txt"
    f1=open(c_path,'a+')
    for domain_name in domains:
        level1={}
        level2={}
        find_links(domain_name,level1)
        a=strftime("%Y-%m-%d %H:%M:%S")
        fill_level1(domain_name,a,level1)
        for e in level1:
            if domain_name not in e:
                l1_link=domain_name+e
            else:
                l1_link=e
            if len(l1_link)<=100:
                print 'link is',l1_link
                find_links(l1_link,level2)
                a=strftime("%Y-%m-%d %H:%M:%S")
                fill_level2(domain_name,l1_link,a,level2)
                level2.clear()
        level1.clear()
        f1.write(domain_name+"\n")
    f1.close()
    #print 'ending ',threadname

if __name__== '__main__':
    path="D://Thesis//data//domain_name//completed1.txt"
    f=open(path,'r')
    domain_list=[]
    domain_list=f.read().split('\n')
    list1=domain_list[0:2]
    list2=domain_list[2:4]
    t1=threading.Thread(target=execution,args=(list1,))
    t2=threading.Thread(target=execution,args=(list2,))
    try:
        t1.start()
        t2.start()
    except:
        print 'error in starting thread'
        #print len(domain_list)
    #i=0
    #while i<len(list1):
        #j=len(list1)
    """list1=domain_list[0:200]
    list2=domain_list[200:400]
    list3=domain_list[400:600]
    list4=domain_list[600:800]
    list5=domain_list[800:1000]
    list6=domain_list[1000:1200]
    list7=domain_list[1200:1400]
    list8=domain_list[1400:1600]
    list9=domain_list[1600:1800]
    list10=domain_list[1800:len(domain_list)]"""
    #list1=domain_list[0:4]
    #list2=domain_list[8:12]
    #print list1
    #list3=domain_list[8:12]
    #list4=domain_list[12:16]
    #print list2
    #print len(domain_list)
    #execution(list_a)
    #process=[]
    #p1 = Process(target=execution, args=('list1',))
    #p2= Process(target=execution,args=('list2',))
    #p3= Process(target=execution,args=('list3',))
    #p4= Process(target=execution,args=('list4',))

    #p1.start()
    #p1.join()
    #p2.start()
#print len(domain_list)
#i=0
#while i<len(list1):
    #j=len(list1)
"""list1=domain_list[0:200]
list2=domain_list[200:400]
list3=domain_list[400:600]
list4=domain_list[600:800]
list5=domain_list[800:1000]
list6=domain_list[1000:1200]
list7=domain_list[1200:1400]
list8=domain_list[1400:1600]
list9=domain_list[1600:1800]
list10=domain_list[1800:len(domain_list)]"""
"""list1=domain_list[0:5]
list2=domain_list[5:10]
list3=domain_list[10:15]
list4=domain_list[15:20]"""
#print list2
#print len(domain_list)
#list1=['http://www.thehindu.com','http://forbesindia.com']
#execution(list1)


