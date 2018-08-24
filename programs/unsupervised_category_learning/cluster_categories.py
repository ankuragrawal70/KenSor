import gexf
import networkx as nx
import wikipedia
import difflib
import operator
import socket
import os
import urllib2, httplib
#import category_from_urls as cat_class
from bs4 import BeautifulSoup
class category_node:
    def __init__(self,name):
        self.c_name=name
        self.count=1
        self.parent=[]
        self.similiar=[]
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
def clean(ele):
    word=""
    for e in ele:
        if e.isalpha():
            word=word+e
    return word
def check_for_special_char(s):
    for i in s:
        if i.isdigit() or i in " ?.!/;:#&+~=@":
            return True
            break
    return False
def check_for_category(cat):
    if len(cat)>2 and len(cat)<18 and check_for_special_char(cat)is not True:
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

def similiar_cat(cat_item,parent,temp):
    for item in category:
        if item in cat_item or cat_item in item:
            category[item].similiar.append(cat_item)
            temp.append(item)
            if parent!="":
                category[item].parent.append(parent)
            return True
        elif loose_match(cat_item,item)>=90:
            category[item].similiar.append(cat_item)
            temp.append(item)
            if parent!="":
                category[item].parent.append(parent)
            return True

def cluser_categories(item):
    f=0
    for element in category:
        if element in item or item in element:
            f=1
            category[element].similiar.append(item)
        else:
            if loose_match(item,element)>80:
                f=1
                category[element].similiar.append(item)
    if f==1:
        return True
    else:
        return False
"""def similiar_categories(cat_item):
    for item in category:
        if item in cat_item or cat_item in item:
                category[item].similiar.append(cat_item)
                if parent!="":
                    category[item].parent.append(parent)
                    temp=category[parent].references
                    if temp.has_key(item):
                        temp[item]=temp[item]+1
                        category[item]=ref
                    else:
                        temp[item]=1
                    category[parent]=ref
                return True
        elif loose_match(cat_item,item)>=90:
                category[item].similiar.append(cat_item)
                if parent!="":
                    category[item].parent.append(parent)
                    temp=category[parent].references
                    if temp.has_key(item):
                        temp[item]=temp[item]+1
                        category[item]=ref
                    else:
                        temp[item]=1
                    category[parent]=ref
                return True
    return False"""

def category_domain_info(element,f_name,category):
        cat_list=url_category_list(element)
        i=0
        temp_item=[]
        while i<len(cat_list)-1:
            if len(temp_item)>0:
                cat_list[i]=temp_item[0]
            if category.has_key(cat_list[i]):
                ref=category[cat_list[i]]
                ref.count=ref.count+1
                if ref.news_sources.has_key(element):
                    ref.news_sources[element]=ref.news_sources[element]+1
                else:
                    ref.news_sources[element]=1
                # temporary add if any similiar category is found
                temp_item=[]
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

                # check similiar categories if any
                elif similiar_cat(cat_list[i+1],cat_list[i],temp_item):
                    pass
                else:
                    new_c=category_node(cat_list[i+1])
                    if category[cat_list[i]].c_name not in new_c.parent:
                        new_c.parent.append(category[cat_list[i]].c_name)
                    category[cat_list[i+1]]=new_c

            elif cluser_categories(cat_list[i]):
                pass
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
                elif cluser_categories(cat_list[i+1]):
                    pass
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
                elif cluser_categories(cat_list[i]):
                    pass
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
                 elif cluser_categories(cat_list[0]):
                    pass
                 else:
                      new_cat=category_node(cat_list[0])
                      new_cat.count=1
                      new_cat.news_sources[element]=1
                      category[cat_list[0]]=new_cat


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
                category_domain_info(e,f_name,category)
        f.close()

category={}
gdelt_source_fetcher()
print 'length of category is', len(category)
for e in category:
    print e
    print category[e].references
    print category[e].parent
    print category[e].similiar
    print '\n'

