#import MySQLdb
import gexf
import networkx as nx
import wikipedia
import difflib
import operator
import socket
import os
import urllib2, httplib
import category_from_urls as cat_class
from nltk.corpus import stopwords
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
def clean(ele):
    word=""
    for e in ele:
        if e.isalpha():
            word=word+e
    return word
def wiki_check(cat,category):
    #print len(list1)
    #print cat
    stop = stopwords.words('english')
    cat_distri={}
    output_str1=""
    #cat=clean(cat)
    try:
        ny = wikipedia.page(cat)
        #wiki_text=wikipedia.summary(cat)
        wiki_text=ny.content
        #print wiki_text
        elements=wiki_text.split(" ")
        #print elements
        #print elements
        #cat_distri={}
        count=0
        for e in elements:
            e=e.lower()
            e=clean(e)
            e=e.encode('utf-8')
            try:
                if e not in stop:
                    if e in category:
                        count=count+1
                #
                        if cat_distri.has_key(e):
                            cat_distri[e]=cat_distri[e]+1
                        else:
                            cat_distri[e]=1

            except:
                pass
        #print 'delhi in cat does not exists\n delhi',cat_distri['delhi']
        print cat_distri
        ch=len(elements)
        x=sorted(cat_distri.iteritems(), key=lambda (k,v): (v,k),reverse=True)
        """for w in sorted(cat_distri, key=cat_distri.get, reverse=True):
            c=sum(cat_distri.values())
            print c
            x=((float)(cat_distri[w]))/c
            print w,x,sub_cat[w].parent"""

        for re in x:
            print re[0], float(re[1])/ch
            output_str1=output_str1+re[0]+'\n'
    except:
         print "no result"
    return output_str1
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

                """if f_name in domain:
                    info=domain[f_name]
                    category_domain_info(e,info)
                else:
                    info={}
                    category_domain_info(e,info)
                    domain[f_name]=info"""

        f.close()
def remove_redundant_category(category):
    for cat in (category.keys()):
            cat_object=category[cat]
            #print cat,cat_object
            #for ele in (cat_object.references.keys()):
                #if cat_object.references[ele]<=2:
            if len(category[cat].news_sources)<=2:
                cat_delete=category[cat]
                if len(cat_delete.parent)>0:
                    for ele in cat_delete.parent:
                        del category[ele].references[cat]
                if len(cat_delete.references)>0:
                    for e in cat_delete.references:
                        category[e].parent.remove(cat)
                del category[cat]
"""category={}
#source_fetcher()
gdelt_source_fetcher()
remove_redundant_category(category)
while True:
    input=raw_input('\n enter entity name\n')
    try:
        wiki_check(input,category)
    except:
        print 'no information obtained'"""