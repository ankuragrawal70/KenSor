import MySQLdb
import gexf
import networkx as nx
import wikipedia
import difflib
import operator
import socket
import urllib2, httplib
from bs4 import BeautifulSoup
import heuristic_learning_approach_category_ident as cat_url_list
import matplotlib.pyplot as plt
class category_node:
    def __init__(self,name):
        self.c_name=name
        self.count=1
        self.parent=[]
        self.references={}
        self.news_sources={}
def loose_match(s1,s2):
    seq = difflib.SequenceMatcher()
    try:
        seq.set_seqs(s1, s2)
        d=seq.ratio()*100
        d=int(d)
        return d
    except:
        return 0
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
    #if 'http://www.thehindu.com' in s:c
    #     print cat_list

    return cat_list


def category_domain_info(element,category):
        cat_list=url_category_list(element)
        i=0
        while i<len(cat_list)-1:
            if category.has_key(cat_list[i]):
                ref=category[cat_list[i]]
                ref.count=ref.count+1
                if ref.news_sources.has_key(element):
                    ref.news_sources[element]=ref.news_sources[element]+1

                else:
                    ref.news_sources[element]=1
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
                new_cat.news_sources[element]=1
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
                    if obj.news_sources.has_key(element):
                            obj.news_sources[element]=obj.news_sources[element]+1
                    else:
                            obj.news_sources[element]=1
                    category[cat_list[i]]=obj
                else:
                      new_cat=category_node(cat_list[0])
                      new_cat.count=1
                      new_cat.news_sources[element]=1
                      category[cat_list[0]]=new_cat
        #ignore for a cat list containing only single category
        if len(cat_list)==1:
                 #print cat_list
                 if category.has_key(cat_list[0]):
                    obj=category[cat_list[0]]
                    obj.count=obj.count+1
                    if obj.news_sources.has_key(element):
                            obj.news_sources[element]=obj.news_sources[element]+1
                    else:
                            obj.news_sources[element]=1
                    category[cat_list[0]]=obj
                 else:
                      new_cat=category_node(cat_list[0])
                      new_cat.count=1
                      new_cat.news_sources[element]=1
                      category[cat_list[0]]=new_cat



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

d={}
dom='http://www.globalpost.com'
result=cat_url_list.cat_domains(dom)
for e in result:
    #if e=='http://www.globalpost.com/news/regions/middle-east/iran':
    #    print 'found'
    category_domain_info(e,d)

for v in d:
    #if len(d[v].references)>0:
       print v,d[v].count,d[v].references
       #print d[v].news_sources
       print '\n'
#print d['music'].news_sources
print 'no of categories obtained are',len(d)
# suggessions function to get suggessions for a particular category
def suggest(item):
    suggessions=[]
    for element in d:
        if element!=item:
            if inp in element or element in inp:
                suggessions.append(element)
            else:
                if loose_match(element,inp)>80:
                   suggessions.append(element)
    return suggessions
while True:
    try:
        i=raw_input('enter category\n')
        inp=i.lower()
        print d[inp].count
        if len(d[inp].references)>0 or len(d[inp].parent)>0:
            print 'related categories are'
            if len(d[inp].references)>0:
                print d[inp].references
            if len(d[inp].parent)>0:
                print d[inp].parent
        if len(suggest(inp))>0:
             print 'other similiar categories may be',suggest(inp)
        min1=1000
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
            print d[inp].news_sources.keys()
    except:
        su=suggest(inp)
        if len(su)>0:
            print " Please enter correct one, Suggessions are\n",su
        else:
            print 'no category found. Please enter correct one'
        continue
