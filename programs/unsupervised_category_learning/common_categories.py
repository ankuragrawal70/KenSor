#import MySQLdb
import gexf
import networkx as nx
import wikipedia
import difflib
import operator
import socket
import os
import urllib2, httplib
from bs4 import BeautifulSoup
#import matplotlib.pyplot as plt
class category_node:
    def __init__(self,name):
        self.c_name=name
        self.count=1
        self.parent=[]
        self.references={}
        self.news_sources={}
def loose_match(s1,s2):
    s1=s1.encode('utf-8')
    s2=s2.encode('utf-8')
    seq = difflib.SequenceMatcher()
    try:
        seq.set_seqs(s1, s2)
        d=seq.ratio()*100
        d=int(d)
        return d
    except:
        return 0
def clean(ele):
    word=""
    for e in ele:
        if e.isalpha():
            word=word+e
    return word

def check_for_special_char(s):
    for i in s:
        if i.isdigit() or i in " ?.!/;:#":
            return True
            break
    return False
def check_for_category(cat):
    if len(cat)>3 and len(cat)<20 and check_for_special_char(cat)is not True:
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

def wiki_check(cat):
    print len(category)
    cat_distri={}
    cat=clean(cat)
    try:
        #ny = wikipedia.page(cat)
        wiki_text=wikipedia.summary(cat)
        #wiki_text=ny.content
        #print wiki_text
        elements=wiki_text.split(" ")
        print elements
        #cat_distri={}
        count=0
        for e in elements:
            e=e.lower()
            e=e.encode('utf-8')

            #print e
            #e=clean(e)
            #print e
            try:
                for ele in category:
                    ele=ele.encode('utf-8')
                    ele=ele.lower()
                    #print ele

                    if loose_match(ele,e)>=70:
                    #if loose_match1(ele,e):

                        #print 'hello'
                        if category[ele].count>9:
                            count=count+1
                            if cat_distri.has_key(ele):
                                cat_distri[ele]=cat_distri[ele]+1
                            else:
                                cat_distri[ele]=1
            except:
                pass
        print cat_distri
        x=sorted(cat_distri.iteritems(), key=lambda (k,v): (v,k),reverse=True)
        """for w in sorted(cat_distri, key=cat_distri.get, reverse=True):
            c=sum(cat_distri.values())
            print c
            x=((float)(cat_distri[w]))/c
            print w,x,sub_cat[w].parent"""
        print x
    except:
         print "no result"

def category_domain_info(element,source):
        cat_list=url_category_list(element)
        i=0
        while i<len(cat_list)-1:
            if category.has_key(cat_list[i]):
                ref=category[cat_list[i]]
                ref.count=ref.count+1
                
                if ref.news_sources.has_key(source):
                    ref.news_sources[source]=ref.news_sources[source]+1

                else:
                    ref.news_sources[source]=1
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
                new_cat.news_sources[source]=1
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
                    if obj.news_sources.has_key(source):
                            obj.news_sources[source]=obj.news_sources[source]+1
                    else:
                            obj.news_sources[source]=1
                    category[cat_list[i]]=obj
                else:
                      new_cat=category_node(cat_list[0])
                      new_cat.count=1
                      new_cat.news_sources[source]=1
                      category[cat_list[0]]=new_cat
        #ignore for a cat list containing only single category
        if len(cat_list)==1:
                 #print cat_list
                 if category.has_key(cat_list[0]):
                    obj=category[cat_list[0]]
                    obj.count=obj.count+1
                    if obj.news_sources.has_key(source):
                            obj.news_sources[source]=obj.news_sources[source]+1
                    else:
                            obj.news_sources[source]=1
                    category[cat_list[0]]=obj
                 else:
                      new_cat=category_node(cat_list[0])
                      new_cat.count=1
                      new_cat.news_sources[source]=1
                      category[cat_list[0]]=new_cat


def gdelt_source_fetcher():
    gdelt_path='D://Thesis//data//domain_name//category_gdelt_valid_source//'
    file_list=os.listdir(gdelt_path)
    for i in range(0,len(file_list)):
    #for i in range(0,100):
        p=gdelt_path+file_list[i]
        f=open(p,'r')
        c_info=eval(f.read())
        if len(c_info)>0:
            f_name='http://'+file_list[i].rstrip('.txt')
            #print f_name
            for e in c_info:
                category_domain_info(e,f_name)
        f.close()

category={}

#print loose_match('politics','politician')
gdelt_source_fetcher()
print category['delhi'].c_name,category['delhi'].count
#wiki_check('Arvind Kejriwal')
#y=sorted(category.items(), key=lambda kv: len(kv[1].news_sources), reverse=True)

def cat_result(x):
    #while True:
        #x=raw_input('enter category')
        parent_child=[]
        try:
            if x in category:
                #print 'category is',x
                #print category[x].parent
                parent_child.append(category[x].parent)
                #print '\n\n'
                #print category[x].references
                parent_child.append(category[x].references)
                return parent_child
            else:
                for e in category:
                    if x in e:
                        #print 'category is',e
                        #print category[e].parent
                        parent_child.append(category[x].parent)
                        #print '\n\n'
                        #print category[e].references
                        parent_child.append(category[x].references)
                        return parent_child
                        break
        except:
            print 'no category found'
            pass
            return parent_child
cat_result('business')


