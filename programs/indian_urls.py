import csv
import os
import thread
import time
import threading
import socket
import sys
import MySQLdb
class category_node:
    def __init__(self,name):
        self.c_name=name
        self.count=1
        self.parent=[]
        self.references={}
        self.news_sources={}
def check_for_special_char(s):
    for i in s:
        if i.isdigit() or i in " ?.!/;:":
            return True
            break
    return False
def check_for_category(cat):
    if len(cat)>4 and len(cat)<20 and check_for_special_char(cat)is not True:
        return True
    else:
        return False
def url_reader(threadName,url):
    path="D://Thesis//data//indian_news_url//"
    filename=os.listdir(path)
    for i in range(0,len(filename)):
        file1=path+filename[i]
        #print file1
        f=open(file1,"rb")
        reader1 = csv.reader(f,delimiter=',')
        row=list(reader1)
        print 'length of url is',len(row)
        f.close()
        for row1 in row:
            if len(row1)==1:
                domain_name=row1[0]
                #print domain_name
                if url.has_key(domain_name):
                        url[domain_name]=url[domain_name]+1
                else:
                    url[domain_name]=1
                    #print domain_name
                    category_domain_info(domain_name)
                    #loc(domain_name)
        #print "\ndate",ac_date
        #print "toal urls\n",len(url)
        #print "\ttotal unique urls are",len(url)
        print "\t file procees are\t",i
    print len(url)
def category_domain_info(element):
        splitted_url=element.split("/")
        length=len(splitted_url)
        if length>2:
            dom=splitted_url[2]
            #print dom
            cat_list=[]
            for i in range(3,len(splitted_url)):
                st=splitted_url[i].strip("")
                try:
                    #if d.check(y):
                        y=st.lower()                        
                        if check_for_category(y):
                            cat_list.append(y)
                except:
                    pass
            #if 'bhopal' in cat_list:
            #print cat_list
            i=0
            while i<len(cat_list)-1:
                if category.has_key(cat_list[i]):
                    ref=category[cat_list[i]]
                    ref.count=ref.count+1
                    #category[cat_list[i]]=ref
                    if i==0:
                        if ref.news_sources.has_key(element):
                            ref.news_sources[element]=ref.news_sources[element]+1
                        
                        else:
                            ref.news_sources[element]=1
                            category[cat_list[i]]=ref
                        
                        
                    temp=ref.references                    
                    if temp.has_key(cat_list[i+1]):
                        temp[cat_list[i+1]]=temp[cat_list[i+1]]+1
                        category[cat_list[i]]=ref
                    else:                        
                        temp[cat_list[i+1]]=1
                        if category.has_key(cat_list[i+1]):
                            x=category[cat_list[i+1]]
                            x.parent.append(category[cat_list[i]].c_name)
                            x.news_sources[element]=1
                            category[cat_list[i+1]]=x
                        else:
                            new_c=category_node(cat_list[i+1])
                            new_c.parent.append(category[cat_list[i]].c_name)
                            new_c.news_sources[element]=1
                            category[cat_list[i+1]]=new_c
                else:
                    new_cat=category_node(cat_list[i])
                    new_cat.news_sources[element]=1
                    category[cat_list[i]]=new_cat
                i=i+1
            if i>0:
                if category.has_key(cat_list[i]):
                    category[cat_list[i]].count=category[cat_list[i]].count+1
def remove_redundant_category(category):
    for cat in (category.keys()):
        try:
            cat_object=category[cat]
            #print cat,cat_object
            for ele in (cat_object.references.keys()):
                if cat_object.references[ele]<4:
                    cat_delete=category[ele]
                    #print "element is",children.c_name
                    #if ele=="workinglife":
                     #   print "child deleted element is",ele,cat_delete.c_name
                    del cat_object.references[ele]
                    p_list=[]
                    p_list=cat_delete.parent
                    try:
                        #if ele=="workinglife":
                         #     print "deleted parent is",cat_object.c_name
                          #    print cat_delete.parent
                        p_list.remove(cat_object.c_name)                    
                    except:
                        pass
                        #print "not in the list"
                    if len(cat_delete.parent)==0:
                        del category[ele]
        except:
            pass

def write_url():    
    db = MySQLdb.connect("localhost",user="root",db="cat_relation_india")
    cursor = db.cursor()
    for e in category:
        #e="business"
        c_id=0
        #print e
        sql="select category_id from category where category_name='%s'"%(e)
        try:
           cursor.execute(sql)
           row=cursor.fetchone()
           c_id=row[0]
           #print "c_id is",c_id
           db.commit()
        except:
            print "error in selection"
            db.rollback()
        obj=category[e]
        url_info=obj.news_sources
        for ele in url_info:
            sql = ("INSERT INTO url_info(url,cat_id) VALUES('%s','%s')" %(ele,c_id))
            try:
                cursor.execute(sql)
                print "inserting url"
                db.commit()
            except:
                print "error in insertion"
                db.rollback()
    db.close()    
def write_to_db():
    db = MySQLdb.connect("localhost",user="root",db="cat_relation_india")
    cursor = db.cursor()
    p_id=0
    for e in (category.keys()):
        c_info=category[e]
        name=c_info.c_name
        c=c_info.count
        p_id=p_id+1
        sql = ("insert into category(category_name,count) values ('%s','%s')"%(name,c))
        try:
           # Execute the SQL command
           cursor.execute(sql)
           db.commit()
           #print "hello"
           # Commit your changes in the database
           db.commit()
        except:
            print "error in main"
           # Rollback in case there is any error
            db.rollback()
        children=c_info.references
        print "hello1",len(children)
        #cn=0
        if len(children)>0:
                for child in children:
                    cnt=children[child]
                    
                    #print "category and c_id ",e,c_id
                    sql = ("INSERT INTO CHILDREN(CHILD_NAME,COUNT,PARENT_ID) VALUES('%s','%s','%s')" %(child, cnt,p_id))
                    try:
                        cursor.execute(sql)
                        #cn=cn+1
                        print "inserted child"
                        db.commit()
                    except:
                        #print "error in insertion"
                        db.rollback()       
    db.close()      
url={}
category={}
domain={}
url_reader("url reader",url)
#print "length of category is",len(category)
#remove_redundant_category(category)
print "length of category is",len(category)

print category['delhi'].count

#write_to_db()
#write_url()
"""if category.has_key('sport'):
    print category['sport'].references
if category.has_key('sports'):
    print category['sports'].references"""
"""for e in category:
    print e,"  ",category[e].count,"   ",len(category[e].references)"""
#print "length of category after removing reduncancy is",len(category)
print "entering to write to db"

print "now inserting urls"

#write_children(category)
