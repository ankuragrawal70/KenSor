#import MySQLdb
import gexf
import networkx as nx
import wikipedia
import difflib
import operator
import socket
import MySQLdb
import os
import urllib2, httplib
import category_from_urls as cat_class
import wiki_classification_cat_relation as wiki
from bs4 import BeautifulSoup
#import matplotlib.pyplot as plt
def loose_match(s1,s2):
    seq = difflib.SequenceMatcher()
    try:
        seq.set_seqs(s1, s2)
        d=seq.ratio()*100
        d=int(d)
        return d
    except:
        return 0

"""def source_fetcher():
    db = MySQLdb.connect("localhost",user="root",db="temporary_category_classification")
    cursor = db.cursor()
    sql="select * from level_1" 
    url_list=[]
    try:
        cursor.execute(sql)            
        result=cursor.fetchall()
        url_list=list(result)
        
    except:
        print "error in selection"
    db.close()
    print len(url_list)
    for e in url_list:
        if e[2]>=3:
            #if e[1]=='http://timesofindia.indiatimes.com/techspeciallisting/35626913.cms':
            #    print 'yes'
            u=e[1]
            
            #cat_list=url_category_list(u)
            #print u,cat_list
            if domain.has_key(e[0]):
                info=domain[e[0]]
                category_domain_info(u,info)
                domain[e[0]]=info
            else:
                info={}
                category_domain_info(u,info)
                domain[e[0]]=info"""
def gdelt_source_fetcher():
    gdelt_path='D://Thesis//data//domain_name//category_gdelt_valid_source//'
    file_list=os.listdir(gdelt_path)
    for i in range(1,len(file_list)):
        p=gdelt_path+file_list[i]
        f=open(p,'r')
        c_info=eval(f.read())
        if len(c_info)>0:
            f_name='http://'+file_list[i].rstrip('.txt')
            #print f_name
            for e in c_info:
                cat_class.category_domain_info(e,f_name,category)


        f.close()
    """gdelt_path='D://Thesis//data//domain_name//gdelt_heuristic_approach_1//'
    file_list=os.listdir(gdelt_path)
    for i in range(0,len(file_list)):
    #for i in range(0,500):
        p=gdelt_path+file_list[i]
        f=open(p,'r')
        category_url=f.read().split('\n')
        f_name='http://'+file_list[i].rstrip('.txt')
            #print f_name
        i=0
        for e in category_url:
                cat_class.category_domain_info(e,f_name,category)
                i=i+1
                #gdelt_cat[f_name]=cat
                if i==len(category_url)-1:
                    break
        f.close()"""
    """gdelt_path='D://Thesis//data//domain_name//special_sources_not_in_gdelt//output//'
    file_list=os.listdir(gdelt_path)
    for i in range(0,len(file_list)):
        #for i in range(0,500):
            p=gdelt_path+file_list[i]
            f=open(p,'r')
            category_url=f.read().split('\n')
            f_name='http://'+file_list[i].rstrip('.txt')
                #print f_name
            i=0
            for e in category_url:
                    cat_class.category_domain_info(e,f_name,category)
                    i=i+1
                    #gdelt_cat[f_name]=cat
                    if i==len(category_url)-1:
                        break
            f.close()"""


def wiki_check(cat):
    #print len(list1)
    cat_distri={}
    cat=clean(cat)
    try:
        #ny = wikipedia.page(cat)
        wiki_text=wikipedia.summary(cat)
        elements=wiki_text.split(" ")
        count=0
        for e in elements:
            e=e.lower()
            e=e.encode('utf-8')

            try:
                for ele in list2:
                    ele=ele.encode('utf-8')
                    ele=ele.lower()
                    #print ele

                    if loose_match(ele,e)>=80:
                    #if loose_match1(ele,e):

                        #print 'hello'
                        count=count+1
                        if cat_distri.has_key(ele):
                            cat_distri[ele]=cat_distri[ele]+1
                        else:
                            f=0
                            for ca in cat_distri:
                                if ca in ele or ele in ca:
                                    f=1
                                    cat_distri[ca]=cat_distri[ca]+1
                                    if ca=='chile':
                                        print 'elemenmt is' ,ele
                                else:
                                    if loose_match(ca,ele)>=80:
                                        f=1
                                        cat_distri[ca]=cat_distri[ca]+1
                            if f==0:
                                cat_distri[ele]=1
            except:
                pass
        print 'delhi in cat does not exists\n delhi',cat_distri['delhi']
        print cat_distri
        ch=len(elements)
        x=sorted(cat_distri.iteritems(), key=lambda (k,v): (v,k),reverse=True)
        """for w in sorted(cat_distri, key=cat_distri.get, reverse=True):
            c=sum(cat_distri.values())
            print c
            x=((float)(cat_distri[w]))/c
            print w,x,sub_cat[w].parent"""
        k=0
        for re in x:
            print re[0], float(re[1])/ch
            k=k+1
            if k>6:
                break
    except:
         print "no result"

def check_validity(h_link,domain_name,level):
    if domain_name in h_link:
            level.append(h_link)
    else:
        if h_link[0]=='/':
            if domain_name[len(domain_name)-1]!='/':
                level.append(domain_name+h_link)
            else:
                l=len(domain_name)-1
                x=domain_name[:l]
                level.append(x+h_link)
def top_news_articles(d_name):
    level=[]
    try :
        web_page = urllib2.urlopen(d_name,timeout=4)
        soup = BeautifulSoup(web_page)
        c=soup.find_all('a')
        for e in c:
            #print e
            try:
                l=e['href']
                if l!=d_name:
                    check_validity(l,d_name,level)
            except:
                #print 'error after parsing links'
                pass
    #return level
        return level
    except:
        print 'error in main link'
        #return level
        return level
        pass
def remove_redundant_category(category):
    for cat in (category.keys()):
            cat_object=category[cat]
            #print cat,cat_object
            #for ele in (cat_object.references.keys()):
                #if cat_object.references[ele]<=2:
            if len(category[cat].news_sources)<6:
                cat_delete=category[cat]
                if len(cat_delete.parent)>0:
                    for ele in cat_delete.parent:
                        del category[ele].references[cat]
                if len(cat_delete.references)>0:
                    for e in cat_delete.references:
                        category[e].parent.remove(cat)
                del category[cat]
#category={}
def write_to_db(category):
    db = MySQLdb.connect("localhost",user="root",db="web_categorization")
    cursor = db.cursor()
    p_id=0
    for e in (category.keys()):
        c_info=category[e]
        name=c_info.c_name
        c=c_info.count
        p_id=p_id+1
        length=len(category[name].news_sources)
        sql = ("insert into category(category_name,count,sources_count) values ('%s','%s','%s')"%(name,c,length))
        try:
           # Execute the SQL command
           cursor.execute(sql)
           db.commit()
           print 'inserted category is',name, pid
        except:
            print "error in main"
           # Rollback in case there is any error
            db.rollback()
    db.close()

def write_children(category):
    db = MySQLdb.connect("localhost",user="root",db="web_categorization")
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
def write_sources(category):
    db = MySQLdb.connect("localhost",user="root",db="web_categorization")
    cursor = db.cursor()
    for element in category:
        sou=category[element].news_sources
        for child in sou:
                print "category and source ",element,child
                sql = ("INSERT INTO DOMAIN_CATEGORY_PATH(CATEGORY_NAME,DOMAIN_PATH) VALUES('%s','%s')" %(element,child))
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    print "error in insertion"
                    db.rollback()
    db.close()
domain={}
category={}
#source_fetcher()
gdelt_source_fetcher()
remove_redundant_category(category)


#print 'length of the category is',len(category),"\n".join(category.keys())
#write_sources(category)
#write_to_db(category)
#write_children(category)
#y=sorted(domain.items(), key=lambda kv: len(kv[1]), reverse=True)
"""for i in range(0,20):
    print y[i][0],len(y[i][1])"""
#source_fetcher2()
#print domain.keys()

#write sources category_wise
#path="D://Thesis//data//domain_name//domains_related_to_category_all_5//"
#source_file="D://Thesis//data//domain_name//special_sources_not_in_gdelt//sources.txt"
#file_o=open(source_file,"a+")
#code to find domains for categories
"""exist=os.listdir(path)
for e in category:
    if len(category[e].news_sources)>1:
        cat=e+'.txt'
        #if cat not in exist:
            #print e
        path1=path+cat
        try:
                sources=category[e].news_sources
                f1=open(path1,'w')
                str1="\n".join(sources.keys())
                f1.write(str1)
                file_o.write("\n"+str1)
                f1.close()
        except:
                pass
        else:
            path2=path+cat
            print e
            sources=category[e].news_sources
            str2="\n".join(sources.keys())
            f2=open(path2,'a+')
            f2.write(str2)
            f2.close()
#used for wikipedia distribution identification"""
"""list1=os.listdir(path)
list2=[]
for e in list1:
    path1=path+e
    f=open(path1,'r')
    sources=f.read().split("\n")
    if len(sources)>9:
        list2.append(e.rstrip('.txt'))"""
"""while True:
    categ=raw_input("input category")
    if categ+'.txt' in list1:
        path1=path+categ+'.txt'
        f1=open(path1,'r')
        sources=f1.read().split("\n")
        for s in sources:
           print s
        print len(sources)
    else:
        print 'category not found'"""
#wiki_check('Arvind Kejriwal')
def suggest(inp):
    suggessions=""
    for element in category:
        if element!=inp:
            if inp in element or element in inp:
                suggessions=suggessions+element+'\n'
            else:
                if loose_match(element,inp)>80:
                   suggessions=suggessions+element+'\n'
    return suggessions

"""while True:
    try:
        sou=raw_input('enter source')
        #d=domain[sou]
        for v in d:
                        #if len(d[v].references)>0:
                 print v,d[v].count,d[v].references
                           #print d[v].news_sources
                 print '\n'
                    #print d['music'].news_sources
        print 'no of categories obtained are',len(d)
    except:
        pass"""


# suggessions function to get suggessions for a particular category
# working synario"""

def result(c_name):
        d=category
        output=[[],[],[],[]]
    #while True:
        try:
            #i=raw_input('enter category\n')
            #inp=i.lower()
            inp=c_name.lower()
            print d[inp].count
            if len(d[inp].references)>0 or len(d[inp].parent)>0:
                print 'related categories are'
                if len(d[inp].references)>0:
                    #children sorted in reverse order of count
                    print 'childrens are',len(d[inp].references)
                    x=sorted(d[inp].references.iteritems(), key=lambda (k,v): (v,k),reverse=True)
                    rel=""
                    for r in x:
                        #print r[0]
                        rel=rel+r[0]+'\n'
                    output[0]=rel
                    #output[0]="\n".join(x)

                if len(d[inp].parent)>0:
                    print 'parents',len(d[inp].parent)
                    #reverse sorted the map
                    map={}
                    p_list=""
                    for e in d[inp].parent:
                        map[e]=category[e].references[inp]

                    y=sorted(map.iteritems(), key=lambda (k,v): (v,k),reverse=True)
                    #ou= d[inp].parent
                    #print 'parents info is',y
                    for el in y:
                    #output[1]="\n".join(ou)
                        p_list=p_list+el[0]+'\n'
                    output[1]=p_list
                    #print p_list

                j=0
            print 'total sources published in the categories are',len(d[inp].news_sources)
            str1=""
            for ns in d[inp].news_sources:
                    str1=str1+ ns+'\n'
                    j=j+1
                    #if j>20:
                    #    break
            output[2]=str1
            #x=suggest(inp)
            #print 'other categories)',len(x)
            #if len(x)>0:
            #     print 'other similiar categories may be\n',x

            #print 'news sources are\n'
            """min1=1000
            source=''
            for e in d[inp].news_sources.keys():
                if len(e)<min1:
                    source=e
                    min1=len(e)
            if source !='':
                sour=source.split(inp)[0]+inp+'/'
                print 'category path is',sour
                x=top_news_articles(sour)
                # x containes list of links specified by the path
                x.sort(key = lambda s: len(s),reverse=True)
                if len(x)>0:
                    print 'latest news events are '

                    for i in range(0,5):
                        print x[i]
                #print source
            else:
                print d[inp].news_sources.keys()"""

            su=suggest(inp)
            #sug="\n".join(su)
            output[3]=su
            #if len(su)>0:
            #    print " Please enter correct one, Suggessions are\n",su
            #else:
            #    print 'no category found. Please enter correct one'
            #continue
        except:
            s=suggest(inp)
            output[3]=s
        return output

def wiki_result(c_name):
        result=wiki.wiki_check(c_name,category)
        return result

#function is used to rank news sources based on global ranking of top 200 news sources
def sources_based_on_ranking():
    world_ranking="D://Thesis//data//domain_name//news_sources_ranking//based_on_4inm_website//"
    direc=os.listdir(world_ranking)
    print direc
    r_sources=[]
    ranked_sources=[]
    for i in range(14,15):
        print direc[i]
        f=open(world_ranking+direc[i],'r')

    #ranked_sources are 200 sources containing global ranking
        r_sources.append(f.read().split("\n"))
        print r_sources
    for sou in r_sources:
        ranked_sources=ranked_sources+sou
    print '200 ranked sources are',ranked_sources
    f.close()
    while True:
        try:
            cat=raw_input("Please enter the category")

            #category specific sources
            print 'related categories are',category[cat].references.keys()
            print category[cat].parent
            category_sources=category[cat].news_sources.keys()
            print 'length of category sources is',len(category_sources)
            print 'sources without rankings are',category_sources

            #sorting index is used to sort category mnews sources
            sorting_index=[0]*len(category_sources)
            count=0
            for i in range(0,len(category_sources)):
                domain_name='http://'+(category_sources[i].split("//")[1]).split('/')[0]
                if domain_name in ranked_sources:
                    index=ranked_sources.index(domain_name)
                    count=count+1

                    #print index
                    sorting_index[i]=index
                else:
                    sorting_index[i]=50000
            #sort category specific source based on ranks of top 200 news sources
            #print sorting_index
            print 'sources is top 200 are',count
            category_sources.sort(key=dict(zip(category_sources, sorting_index)).get)
            #[x for (y,x) in sorted(zip(sorting_index,category_sources))]
            print "\n sources after rankings are\n"
            for source in category_sources:
                print source
        except:
            pass
#sources_based_on_ranking()