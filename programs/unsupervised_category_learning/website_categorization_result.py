#import MySQLdb
import gexf
import networkx as nx
import wikipedia
import difflib
import operator
import socket
import MySQLdb
import twiter_info_access as social
import os
import urllib2, httplib
import category_from_urls as cat_class
import wiki_classification_cat_relation as wiki
from bs4 import BeautifulSoup

def precision_recall():
    stat_count=0
    avg_prec=0
    avg_rec=0
    sources_length=0
    avg_categories=0
    for ele in ground_truth_map:
        temp={}
        cat_not_in_groundtruth=[]
        cat_not_in_mainalgo=[]
        # length include length of ground truth map
        try:
            if ele in global_map:
                length=len(global_map[ele])
                #length=0
                sources_length=sources_length+1
                for cat in global_map[ele]:
                    if cat not in temp:
                        temp[cat]=1
                        #length=length+1

                #observed length by web categorization
                observerd_length=len(ground_truth_map[ele])
                print observerd_length
                avg_categories=avg_categories+observerd_length
                count=0
                for cat in ground_truth_map[ele]:
                    if cat in temp:
                        temp[cat]=temp[cat]+1
                        count=count+1
                    else:
                        cat_not_in_mainalgo.append(cat)
                for t in temp:
                    if temp[t]==1:
                        if t.lower()+".txt" not in valid_categories or t.lower() not in invalid_categories:
                            length=length-1
                        else:
                            #print t.lower()+".txt"
                            cat_not_in_groundtruth.append(t)
                precision=float(count)/length
                avg_prec=avg_prec+precision
                recall=float(count)/observerd_length
                avg_rec=avg_rec+recall
                print "file name is",ele
                print"categories not in groundtruth\n",cat_not_in_groundtruth

                print "categories not in main algorithms",cat_not_in_mainalgo
                print "precison is",precision
                print "recall is",recall
                #path="D://Thesis//data//domain_name//twitter_information_sources//"
                #f_pre=open(path+"approach1_basic.txt","a+")
                #f_pre.write(ele+" "+str(precision)+" "+str(recall)+" "+str(observerd_length)+"\n")
                #f_pre.close()
                #for e in temp:
                #    if temp[e]==1:
                #        print e
                if  recall<=0.9:
                    stat_count=stat_count+1
                print "\n"
            else:
                print "domain not found in main categories algorithms", ele
        except:
            pass
    print "length of sources is",sources_length
    print "average precision",avg_prec/sources_length
    print "average recall",avg_rec/sources_length
    print "records with high precision and recalls are",stat_count
    print "average categories obtained per news sources are",float(avg_categories)/50



#global map contains information from web categorization approach
global_map={}

#ground truth map contains information for ground truth data
ground_truth_map={}

invalid_categories=['feedback','privacy','homepage','rssfeeds','topic','advertise','aboutus','contactus','password','users','users','subscribe','about-us','contact_us','about_us','contact-us','privacy-policy','sitemap','disclaimer', 'preview', 'copyright', 'terms-service', 'privacy-policy', 'contact', 'careers', 'corrections', 'advertise', 'archive', 'rss','live','pressrelease','tag', 'faq','rss_feeds', 'press','feeds','about','all','faqs','search','register','rss_feeds','logout','login','sitemap','tags','press_release','press_releases']
#for valid URLs
def gdelt_source_fetcher():
    gdelt_path='D://Thesis//data//domain_name//category_gdelt_valid_source//'
    file_list=os.listdir(gdelt_path)
    for i in range(0,len(file_list)):
        #if file_list[i].rstrip(".txt") in checked_sources:
            #print file_list[i]
            p=gdelt_path+file_list[i]
            f=open(p,'r')
            c_info=eval(f.read())
            if len(c_info)>0:

                f_name='http://'+file_list[i].rstrip('.txt')
                #print f_name
                category={}
                for e in c_info:
                    cat_class.category_domain_info(e,f_name,category)
            global_map[f_name]=category
            #ground_truth_map[f_name]=category

#fetched from some indian sources
def gdelt_source_fetcher_remaining():
    gdelt_path='D://Thesis//data//domain_name//gdelt_heuristic_approach//fraesh_processed//'
    file_list=os.listdir(gdelt_path)
    for i in range(0,len(file_list)):
        #if file_list[i].rstrip(".txt") in checked_sources:
            #print file_list[i]
            p=gdelt_path+file_list[i]
            f=open(p,'r')
            c_info=f.read().split("\n")
            if len(c_info)>0:
                f_name='http://'+file_list[i].rstrip('.txt')
                #print f_name
                category={}
                for e in c_info:
                    cat_class.category_domain_info(e,f_name,category)
            global_map[f_name]=category


def ground_source_fetcher():
    g_path='D://Thesis//data//domain_name//category_ground_truth//'
    file_list=os.listdir(g_path)
    for i in range(0,len(file_list)):
            #print file_list[i]
            p=g_path+file_list[i]
            f=open(p,'r')
            category_url=f.read().split('\n')
            f_name='http://'+file_list[i].rstrip('.txt')
            category={}
            for e in category_url:
                    cat_class.category_domain_info(e,f_name,category)
            ground_truth_map[f_name]=category
    """g_path='D://Thesis//data//domain_name//gdelt_heuristic_approach//fraesh_processed//'
    file_list=os.listdir(g_path)
    for i in range(0,len(file_list)):
            #print file_list[i]
            p=g_path+file_list[i]
            f=open(p,'r')
            category_url=f.read().split('\n')
            f_name='http://'+file_list[i].rstrip('.txt')
            category={}
            for e in category_url:
                    cat_class.category_domain_info(e,f_name,category)
            #ground_truth_map[f_name]=category
            global_map[f_name]=category"""

valid_cat_path="D://Thesis//data//domain_name//domains_related_to_category_all_5//"
valid_categories=os.listdir(valid_cat_path)
#gdelt_source_fetcher()
gdelt_source_fetcher_remaining()
ground_source_fetcher()
print len(global_map),len(ground_truth_map)
precision_recall()

"""count_so=0
social_info=social.twitter_info()
present_sources=0
less_popular_sources=[]
for element in ground_truth_map:
    flag=0
    for source in social_info:
        elements=source
        if elements[0]==element:
            flag=1
            present_sources=present_sources+1
            try:
                if int(elements[2])<=500000:
                    print elements[2],element
                    count_so=count_so+1
                    less_popular_sources.append(element)
            except:
                pass
    if flag==0:
        print element
print "available sources",present_sources
print "sources with good page ranks are",count_so

social_info=social.page_rank_info()
present_sources=0
count_so=0
print "less popular sources",len(less_popular_sources)
for element in less_popular_sources:
    flag=0
    for source in social_info:
        elements=source.split(" ")
        if elements[0]==element:
            flag=1
            present_sources=present_sources+1
            try:
                if int(elements[2])>=7:
                    print elements[2]
                    count_so=count_so+1
            except:
                pass
    if flag==0:
        print element
print "available sources",present_sources
print "sources with good page ranks are",count_so"""
