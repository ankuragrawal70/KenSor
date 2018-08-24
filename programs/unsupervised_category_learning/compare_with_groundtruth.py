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

def precision_recall():
    stat_count=0
    avg_prec=0
    avg_rec=0
    sources_length=0
    for ele in global_map:
        temp={}
        # length include length of ground truth map
        try:
            length=len(ground_truth_map[ele])
            sources_length=sources_length+1
            for cat in ground_truth_map[ele]:
                if cat not in temp:
                    temp[cat]=1

            #observed length by web categorization
            observerd_length=len(global_map[ele])
            count=0
            for cat in global_map[ele]:
                if cat in temp:
                    temp[cat]=temp[cat]+1
                    count=count+1
                else:
                    print cat

            precision=float(count)/observerd_length
            avg_prec=avg_prec+precision
            recall=float(count)/length
            avg_rec=avg_rec+recall
            print "file name is",ele
            print "precison is",precision
            print "recall is",recall
            #for e in temp:
            #    if temp[e]==1:
            #        print e
            if  recall>=0.8 or precision>=0.8:
                stat_count=stat_count+1
            print "\n"
        except:
            pass
    print "length of sources is",sources_length
    print "average precision",avg_prec/sources_length
    print "average recall",avg_rec/sources_length
    print "records with high precision and recalls are",stat_count


checked_sources=["www.thehindu.com","timesofindia.indiatimes.com","www.nytimes.com","indianexpress.com"]
#global map contains information from web categorization approach
global_map={}

#ground truth map contains information for ground truth data
ground_truth_map={}

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
            print file_list[i]
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

gdelt_source_fetcher()
#gdelt_source_fetcher_remaining()
ground_source_fetcher()
print len(global_map),len(ground_truth_map)

precision_recall()

