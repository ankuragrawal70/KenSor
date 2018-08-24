import csv
import os
import thread
import time
import threading
import geoip2.database
import socket
import MySQLdb
#import gexf
#mport networkx as nx
#import matplotlib.pyplot as plt
import sys

#import enchant

def location(hostname):
        list1=[]
        try:
            addr = socket.gethostbyname(hostname)
            reader = geoip2.database.Reader('D:/Thesis/GeoLite2-City.mmdb/home/tjmather/mm_website/geoip/BuildDatabase/GeoLite2-City.mmdb')
            #reader = geoip2.database.Reader("D:/Thesis/GeoLite2-Country.mmdb/home/tjmather/mm_website/geoip/BuildDatabase/GeoLite2-Country.mmdb")
            response = reader.city(addr)
            if response.country.name is not  None:
                list1.append(response.country.name.encode("utf-8"))
            else:
                list1.append(response.country.name)
            list1.append(response.city.name)
            list1.append(response.postal.code)
            list1.append(response.location.latitude)
            list1.append(response.location.longitude)
        except:
            pass
        
        return list1
class category_node:
    def __init__(self,name):
        self.c_name=name
        self.count=1
        self.parent=[]
        self.references={}
        self.news_sources={}
def check_for_special_char(s):
    for i in s:
        if i.isdigit() or i in " ?.!/;:#":
            return True
            break
    return False
def check_for_category(cat):
    if len(cat)>2 and len(cat)<20 and check_for_special_char(cat)is not True:
        return True
    else:
        return False
def url_category_list(s):
    cat_list=[]
    if s[0]=='/':
        sp=s.split('/')[1:]
    else:
        sp=s.split('/')[1:]
    for i in range(0,len(sp)):
        y=sp[i].strip('-_,. :').lower()
        if check_for_category(y):
             cat_list.append(y)
    #if 'http://www.thehindu.com' in s:
    #     print cat_list
    return cat_list
def traversal(sp,output):
     print "category",sp.c_name
     if len(sp.parent)==0:
         print "news sources in",sp.c_name
         #,"are",sp.news_sources
         #print "sub categories are\n"
         print "sub_category ::"
         for element in sp.references:
             element,sp.references[element]
             #,"\nnews sources are",category[element].news_sources
             print "\n"
     else:
         print "\n parents category are"
         #for element in sp.parent:
         print sp.parent
         #    print element.c_name
         print "\n news sources in",sp.c_name
         #,"category are",sp.news_sources,"\n"
         print "\nsub categories and news sources are\n"
         print "sub_category ::\n"
         for element in sp.references:
             element,sp.references[element]
             #"\nnews sources are",category[element].news_sources
             print "\n"
def url_reader(threadName,url):
    #location of list of urls in the record
    #path= "D://Thesis//data//category_data//url_info2.CSV"
    #b=open(path,"wb")
    #c=csv.writer(b,delimiter='\t')
    #.writerow(["Date   ","total_url   ","total_categories"])
    #input data location
    try:
        path="D://Thesis//data//"
        filename=os.listdir(path)
        for i in range(400,len(filename)-2):
            file1=path+filename[i]
            f=open(file1,"rb")
            date=filename[i][:-11]
            ac_date=date[0:4]+"/"+date[4:6]+"/"+date[6:len(date)]
            reader1 = csv.reader(f,delimiter='\t')
            row=list(reader1)
            f.close()
            #row is a set of rows of the given file
            #url is a hash_map that contains the urls and their count
            for row1 in row:
                x=len(row1)
                domain_name=row1[x-1]
                if url.has_key(domain_name):
                        url[domain_name]=url[domain_name]+1
                else:
                        url[domain_name]=1
                        category_domain_info(domain_name)
                        #loc(domain_name)
            print "\ndate",ac_date
            #print "toal urls\n",len(url)
            #print "\ttotal unique urls are",len(url)
            print "\t file procees are\t",i
    except:
        print 'error'
        pass
def loc(dom_name):
            db = MySQLdb.connect("localhost",user="root",db="category_info")
            cursor = db.cursor()
        #for dom_name in url:
            splitted_url=dom_name.split("/")
            length=len(splitted_url)
            if length>1:
                dom=splitted_url[2] 
                if domain.has_key(dom):
                    #domain[dom]=domain[dom]+1
                    pass
                else:
                    loc_list=location(dom)
                    print "location list is",loc_list
                    domain[dom]=loc_list
                    #for e in loc_lis:
                    #print dom
                    #print loc_list
                    f=0
                    sql="select count(*)from location_info where domain_name='%s'"%(dom)
                    try:
                            cursor.execute(sql)
                            result=cursor.fetchone()
                            f=result[0]
                            db.commit()
                    except:
                            print "error in selection"
                    if f==0:
                            print "no entry found so inserting"
                            if len(loc_list)==5:
                                co=loc_list[0]
                                c=loc_list[1]
                                p=loc_list[2]
                                la=loc_list[3]
                                lo=loc_list[4]
                                #print p
                            
                                sql = ("insert into location_info(domain_name,country,city,postal_address,latitude,longitude) values ('%s','%s','%s','%s','%s','%s')"%(dom,co,c,p,la,lo))
                                try:
                                   # Execute the SQL command
                                   cursor.execute(sql)
                                   # Commit your changes in the database
                                   db.commit()
                                except:
                                    print "error in location"
                                   # Rollback in case there is any error
                                    db.rollback()
                    else:
                            print "entry found so not inserting"
                        
            db.close()
def category_domain_info(element):
        cat_list=url_category_list(element)
        i=0
        while i<len(cat_list)-1:
            if category.has_key(cat_list[i]):
                ref=category[cat_list[i]]
                ref.count=ref.count+1
               # if ref.news_sources.has_key(element):
               #     ref.news_sources[element]=ref.news_sources[element]+1

                #else:
                #    ref.news_sources[element]=1
                temp=ref.references
                if temp.has_key(cat_list[i+1]):
                    temp[cat_list[i+1]]=temp[cat_list[i+1]]+1
                    category[cat_list[i]]=ref
                else:
                    temp[cat_list[i+1]]=1
                category[cat_list[i]]=ref
                if category.has_key(cat_list[i+1]):
                    x=category[cat_list[i+1]]
                    if category[cat_list[i]].c_name not in x.parent:
                        x.parent.append(category[cat_list[i]].c_name)
                    category[cat_list[i+1]]=x
                else:
                    new_c=category_node(cat_list[i+1])
                    if category[cat_list[i]].c_name not in new_c.parent:
                        new_c.parent.append(category[cat_list[i]].c_name)
                    category[cat_list[i+1]]=new_c
            else:
                new_cat=category_node(cat_list[i])
                new_cat.count=1
                #new_cat.news_sources[element]=1
                new_cat.references[cat_list[i+1]]=1
                category[cat_list[i]]=new_cat
                if category.has_key(cat_list[i+1]):
                    x=category[cat_list[i+1]]
                    if category[cat_list[i]].c_name not in x.parent:
                        x.parent.append(category[cat_list[i]].c_name)
                    category[cat_list[i+1]]=x
                else:
                    new_c=category_node(cat_list[i+1])
                    if category[cat_list[i]].c_name not in new_c.parent:
                        new_c.parent.append(category[cat_list[i]].c_name)
                    category[cat_list[i+1]]=new_c
            i=i+1
        #for last element of category list
        if i>0:
                if category.has_key(cat_list[i]):
                    obj=category[cat_list[i]]
                    obj.count=obj.count+1
                    #if obj.news_sources.has_key(element):
                    #        obj.news_sources[element]=obj.news_sources[element]+1
                    #else:
                    #        obj.news_sources[element]=1
                    category[cat_list[i]]=obj
                else:
                      new_cat=category_node(cat_list[0])
                      new_cat.count=1
                      #new_cat.news_sources[element]=1
                      category[cat_list[0]]=new_cat
        #ignore for a cat list containing only single category
        if len(cat_list)==1:
                 #print cat_list
                 if category.has_key(cat_list[0]):
                    obj=category[cat_list[0]]
                    obj.count=obj.count+1
                    #if obj.news_sources.has_key(element):
                    #        obj.news_sources[element]=obj.news_sources[element]+1
                    #else:
                    #        obj.news_sources[element]=1
                    category[cat_list[0]]=obj
                 else:
                      new_cat=category_node(cat_list[0])
                      new_cat.count=1
                     # new_cat.news_sources[element]=1
                      category[cat_list[0]]=new_cat
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
def model_graph(root,g,path_visited,count):    
    n_name=root.c_name
    g.add_node(n_name)
    count=count+1
    if n_name in path_visited:
        return
    if len(root.references)==0:
        return
    if count==3:
        return
    
    else:
        #print "hello"
        for child in root.references:
            list2=path_visited[:]
            g.add_node(child)
            g.add_edge(n_name,child)
            obj=category[child]
            model_graph(obj,g,list2,count)
            #g.add_nodes_from([n_name,child])
        #for level in root.references:
         #   obj=category[level]
           # model_graph(obj,g)
        
def graph_plot(category):
    for node_check in category:
        v=category[node_check]
        if len(v.parent)==0:
            count=0
            path_visited=[]
            print v.c_name
            model_graph(v,g,path_visited,count)
def write_children(category):    
    db = MySQLdb.connect("localhost",user="root",db="news_category_relation")
    cursor = db.cursor()
    #for el in c_info.references:
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
        children=obj.references
        for child in children:
                cnt=children[child]
                print "category and c_id ",e,c_id
                sql = ("INSERT INTO CHILDREN(CHILD_NAME,COUNT,PARENT_ID) VALUES('%s','%s','%s')" %(child, cnt,c_id))
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    print "error in insertion"
                    db.rollback()
        """url_info=obj.news_sources
        for ele in url_info:
            sql = ("INSERT INTO url_info(url,cat_id) VALUES('%s','%s')" %(ele,c_id))
            try:
                cursor.execute(sql)
                print "inserting url"
                db.commit()
            except:
                print "error in insertion"
                db.rollback()"""
    db.close()
def write_to_db(category):
    db = MySQLdb.connect("localhost",user="root",db="news_category_relation")
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
        """children=c_info.references
        #print "hello1",len(children)
        #cn=0
        if len(children)>0:
                for child in children:
                    cnt=children[child]
                    
                    #print "category and c_id ",e,c_id
                    sql = ("INSERT INTO CHILDREN(CHILD_NAME,COUNT,PARENT_ID) VALUES('%s','%s','%s')" %(child, cnt,p_id))
                    try:
                        cursor.execute(sql)
                        #cn=cn+1
                        #print "inserted child"
                        db.commit()
                    except:
                        #print "error in insertion"
                        db.rollback() """

        """printhello2
        url_info=c_info.news_sources
        print "url info is",len(url_info)
        c=0
        for ele in url_info:
            sql = ("INSERT INTO url_info(url,cat_id) VALUES('%s','%s')" %(ele,p_id))
            try:
                cursor.execute(sql)
                c=c+1
                print "url info inserted",c
                db.commit()
            except:
                print "error in insertion"
                db.rollback()"""
       
    db.close()
url={}
category={}
domain={}

#output=""
#d=enchant.Dict("en_US")

#sys.setrecursionlimit(10000)
url_reader("url reader",url)
print 'length of news events are',len(url)
print "length of category is",len(category)
#loc(url)
#print "now removing redundat category and urls"
#remove_redundant_category(category)
print "length of category after removing reduncancy is",len(category)
print "entering to write to db"
#write_to_db(category)
write_children(category)
print "now inserting urls"
print 'total categories are',len(category)

cou=0
for e in category:
    if len(category[e].parent)==0:
       cou=cou+1
print 'total categories on level 1 are',cou
a=0
for x in category:
    if len(category[x].news_sources)>4:
        a=a+1
print 'categpry that occurs with only five news source',a

print 'top 20 categories with frequent counts are'
"""for i in range(0,20):
    print y[i][0],len(y[i][1].news_sources)"""


#write_children(category)
#category.clear()
#print "now inserting location of domain"

#write_url_info(category)
#print "length of the category is",len(category)
#graph_plot(category)

"""c=""
while 1:
    c=raw_input("\n input the category you want to search for\n")
    if category.has_key(c):
        sp=category[c]
        traversal(sp,output)
        path_visited=[]
        count=0
        g=nx.DiGraph()
        model_graph(category[c],g,path_visited,count)
        nx.draw(g)
        plt.show()
        graph_pos=nx.spring_layout(g)
        nx.draw_networkx_nodes(g,graph_pos,node_size=2000, 
                                   alpha=0.3, node_color='blue')
        nx.draw_networkx_edges(g,graph_pos,width=1,
                                   alpha=0.3,edge_color='red')
        nx.draw_networkx_labels(g, graph_pos,font_size=12,
                                    font_family='sans-serif')
        plt.show()
    else:
        print "no category present of this kind"""
"""
ca=""
while ca is not None:
    ca=raw_input("\n input the category you want to search for\n")
    if category.has_key(ca):
        sp=category[ca]
        traversal(sp,output)
    else:
        print "no category present of this kind"""
