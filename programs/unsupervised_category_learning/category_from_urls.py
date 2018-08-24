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
    try:
        if s[0]=='/':
            sp=s.split('/')[1:]
        else:
            sp=s.split('/')[1:]

        for i in range(0,len(sp)):
            y=sp[i].strip('-_,. :')
            if check_for_category(y):
                 cat_list.append(y)
    #if 'http://www.thehindu.com' in s:
    #print cat_list
    except:
        pass
    return cat_list


# remove extra path after a category from element url
def filter_element(element,category):
    #print element
    source=element.split("/"+category)[0]
    #if "timesofindia.indiatimes.com" in element and category=="english":
    #    print element
    #    print source
    #    print category+"\n"
    #print source
    #print category+"\n"
    return source+"/"+category
def category_domain_info(element_url,f_name,category):
        cat_list=url_category_list(element_url)
        i=0
        while i<len(cat_list)-1:
            if category.has_key(cat_list[i].lower()):
                ref=category[cat_list[i].lower()]
                ref.count=ref.count+1
                # split element and remover extra path from it
                element=filter_element(element_url,cat_list[i])
                if ref.news_sources.has_key(element):
                    ref.news_sources[element]=ref.news_sources[element]+1

                else:
                    ref.news_sources[element]=1
                temp=ref.references
                if temp.has_key(cat_list[i+1].lower()):
                    temp[cat_list[i+1].lower()]=temp[cat_list[i+1].lower()]+1
                    category[cat_list[i].lower()]=ref
                else:
                    temp[cat_list[i+1].lower()]=1
                category[cat_list[i].lower()]=ref
                if category.has_key(cat_list[i+1].lower()):
                    x=category[cat_list[i+1].lower()]
                    if category[cat_list[i].lower()].c_name not in x.parent:
                        x.parent.append(category[cat_list[i].lower()].c_name)
                    category[cat_list[i+1].lower()]=x
                else:
                    new_c=category_node(cat_list[i+1].lower())
                    if category[cat_list[i].lower()].c_name not in new_c.parent:
                        new_c.parent.append(category[cat_list[i].lower()].c_name)
                    category[cat_list[i+1].lower()]=new_c
            else:
                new_cat=category_node(cat_list[i].lower())
                new_cat.count=1
                element=filter_element(element_url,cat_list[i])
                new_cat.news_sources[element]=1
                new_cat.references[cat_list[i+1].lower()]=1
                category[cat_list[i].lower()]=new_cat
                if category.has_key(cat_list[i+1].lower()):
                    x=category[cat_list[i+1].lower()]
                    if category[cat_list[i].lower()].c_name not in x.parent:
                        x.parent.append(category[cat_list[i].lower()].c_name)
                    category[cat_list[i+1].lower()]=x
                else:
                    new_c=category_node(cat_list[i+1].lower())
                    if category[cat_list[i].lower()].c_name not in new_c.parent:
                        new_c.parent.append(category[cat_list[i].lower()].c_name)
                    category[cat_list[i+1].lower()]=new_c
            i=i+1
        #for last element of category list
        if i>0:
                if category.has_key(cat_list[i].lower()):
                    obj=category[cat_list[i].lower()]
                    obj.count=obj.count+1
                    element=filter_element(element_url,cat_list[i])
                    if obj.news_sources.has_key(element):
                            obj.news_sources[element]=obj.news_sources[element]+1
                    else:
                            obj.news_sources[element]=1
                    category[cat_list[i].lower()]=obj
                else:
                      new_cat=category_node(cat_list[0].lower())
                      new_cat.count=1
                      element=filter_element(element_url,cat_list[0])
                      new_cat.news_sources[element]=1
                      category[cat_list[0].lower()]=new_cat
        #ignore for a cat list containing only single category
        if len(cat_list)==1:
                 #print cat_list

                 if category.has_key(cat_list[0].lower()):
                    obj=category[cat_list[0].lower()]
                    obj.count=obj.count+1
                    element=filter_element(element_url,cat_list[0])
                    if obj.news_sources.has_key(element):
                            obj.news_sources[element]=obj.news_sources[element]+1
                    else:
                            obj.news_sources[element]=1
                    category[cat_list[0].lower()]=obj
                 else:
                      new_cat=category_node(cat_list[0].lower())
                      new_cat.count=1
                      element=filter_element(element_url,cat_list[0].lower())
                      new_cat.news_sources[element]=1
                      category[cat_list[0].lower()]=new_cat
