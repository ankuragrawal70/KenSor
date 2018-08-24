import csv
import MySQLdb
import re
import wikipedia
import difflib
import operator
#import networkx as nx
#import matplotlib.pyplot as plt
class children:
    def __init__(self):
        self.count=0
        self.similiar={}
        self.children={}
        self.parent=[]

def loose_match(s1,s2):
    seq = difflib.SequenceMatcher()
    try:
        seq.set_seqs(s1, s2)
        d=seq.ratio()*100
        d=int(d)
        return d
    except:
        return 0
def length_diff(s1,s2):
    if len(s1)>len(s2):
        p=(float)(len(s1)-len(s2))/len(s1)
    elif len(s1)<len(s2):
        p=(float)(len(s1)-len(s2))/len(s2)
    return p
def loose_match1(s1,s2):
    if len(s1)<len(s2):
        x=len(s1)
        x=x*0.8
        x=(int)(x)
        st=s1[0:x]
        if st in s2:
            return True
    elif len(s2)<len(s1):
        x=len(s1)*0.8
        x=(int)(x)
        st=s2[0:x]
        if st in s1:
            return True
    else:
        seq = difflib.SequenceMatcher()
        try:
            seq.set_seqs(s1, s2)
            d=seq.ratio()*100
            d=int(d)
            if d>=80:
                return True
        except:
            return False
    return False

import csv
def clean(ele):
    word=""
    for e in ele:
        if e.isalpha():
            word=word+e
    return word
def similiar_cat():
    key_list=main_cat.keys()
    for e in key_list:
        x=clean(e)
        for check in main_cat.keys():
            y=clean(check)
            if x!=y :
                if (x in y or y in x) and length_diff(x,y)<=0.60:
                #if loose_match(x,y)>90:
                    v=children()
                    if len(main_cat[e].similiar)==0 and len(main_cat[check].similiar)==0:
                        if main_cat[e].count<main_cat[check].count:
                            v.count=main_cat[check].count
                            main_cat[e].similiar[check]=v
                            #main_cat[e].similiar[check]=main_cat[check].count
                            del main_cat[check]
                            key_list.remove(check)
                        elif main_cat[e].count>main_cat[check].count:
                            v.count=main_cat[e].count
                            main_cat[check].similiar[e]=v
                            #main_cat[check].similiar[e]=main_cat[e].count
                            del main_cat[e]
                            key_list.remove(e)
                    elif len(main_cat[e].similiar)==0:
                        v.count=main_cat[e].count
                        main_cat[check].similiar[e]=v
                        #main_cat[check].similiar[e]=main_cat[e].count
                        del main_cat[e]
                        key_list.remove(e)
                    elif len(main_cat[check].similiar)==0:
                        v.count=main_cat[check].count
                        main_cat[e].similiar[check]=v
                        #main_cat[e].similiar[check]=main_cat[check].count
                        del main_cat[check]
                        key_list.remove(check)
                    break
def parent_relation():
    for c in main_cat.keys():
        
        db = MySQLdb.connect("localhost",user="root",db="news_category_relation")
        cursor = db.cursor()
        sql="select category_name,children.count from category,children where parent_id=category_id and child_name='%s'"%(c)
        parent_list=[]
        try:
            cursor.execute(sql)            
            result=cursor.fetchall()
            parent_list=list(result)
        except:
            print "error in selection"
        for row in parent_list:  
            if row[1]>2:
                if row[0] in main_cat:
                    #if child=='cricket':
                    #    print row[0]
                    #value=main_cat[row[0]]
                    #value.children[child]=row[1]
                    main_cat[row[0]].children[c]=row[1]
                    main_cat[c].parent.append(row[0])
                else:
                    for e in main_cat:
                        if row[0] in main_cat[e].similiar:
                            value=main_cat[e].similiar[row[0]]
                            value.children[c]=row[1]
                            main_cat[e].similiar[row[0]]=value
                            main_cat[c].parent.append(row[0])
                            break
        for child in main_cat[c].similiar:
            db = MySQLdb.connect("localhost",user="root",db="news_category_relation")
            cursor = db.cursor()
            sql="select category_name,children.count from category,children where parent_id=category_id and child_name='%s'"%(child)
            parent_list=[]
            try:
                cursor.execute(sql)            
                result=cursor.fetchall()
                parent_list=list(result)
            except:
                print "error in selection"
            for row in parent_list:              
                if row[1]>9:
                    if row[0] in main_cat:
                        #if child=='cricket':
                        #    print row[0]
                        #value=main_cat[row[0]]
                        #value.children[child]=row[1]
                        main_cat[row[0]].children[child]=row[1]
                        main_cat[c].similiar[child].parent.append(row[0])
                    else:
                        for e in main_cat:       
                            if row[0] in main_cat[e].similiar:
                                value=main_cat[e].similiar[row[0]]
                                #if child=='cricket':
                                #    print 'in similiar',e, row[0]
                                #value=main_cat[e]
                                value.children[child]=row[1]
                                main_cat[e].similiar[row[0]]=value
                                main_cat[c].similiar[child].parent.append(row[0])
                                break
"""def parent_relation():
    for child in main_cat.keys():
        #for child in main_cat[c].similiar:
            db = MySQLdb.connect("localhost",user="root",db="news_category_relation")
            cursor = db.cursor()
            sql="select category_name,children.count from category,children where parent_id=category_id and child_name='%s'"%(child)
            parent_list=[]
            try:
                cursor.execute(sql)            
                result=cursor.fetchall()
                parent_list=list(result)
            except:
                print "error in selection"
            for row in parent_list:            
                if row[1]>2:
                    if row[0] in main_cat:
                        value=main_cat[row[0]]
                        value.children[child]=row[1]
                        main_cat[row[0]]=value
                        main_cat[child].parent.append(row[0])"""

main_path="D://Thesis//data//exported_data//sorted indian category with count greater than 9"
f=open(main_path+".CSV","rb")
main_category=csv.reader(f,delimiter=';')
rows=list(main_category)
main_cat={}
for row in rows:
    #print row
    #x=row[0].split(";")
    ch=children()
    ch.count=row[1]
    #if row[0]=='cricket':
    main_cat[row[0]]=ch
similiar_cat()
parent_relation()
print len(main_cat)
while True:
    v=raw_input('\n enter the category\n')
    if v in main_cat:
            print main_cat[v].count
            print '\n similiar categories are'
            for e in main_cat[v].similiar:
                print e  
            print '\nchildrens are\n'
            print main_cat[v].children
            print "\n parents are\n"
            print main_cat[v].parent
    else:
        f=0
        for element in main_cat:
            if v in main_cat[element].similiar:
                f=1
                print v ,"\n is similiar to\n", element
                print '\n similiar categories are'
                for e in main_cat[element].similiar:
                    print e
                #print main_cat[v].count
                print main_cat[element].similiar[v].count
                print '\nchildrens are\n'
                print main_cat[element].similiar[v].children
                print "\n parents are\n"
                print main_cat[element].similiar[v].parent
                break
        if f==0:
            cat=''
            main=''
            max1=0
            for c in main_cat:
                #print c
                x=loose_match(c,v)
                if x>80:
                    if x>=max1:
                        max1=x
                        cat=c
                        main=c
                for s in main_cat[c].similiar:
                    x=loose_match(v,s)
                    if x>=80:
                        if x>max1:
                            max1=x
                            cat=s
                            main=c
            #print cat
            if cat!='':
                if main!=cat:
                    print '\n\n suggested category is\n',main,"\n"
                    print '\nsimiliar categories are\n'
                    for e in main_cat[main].similiar:
                        print e
                    print main_cat[main].similiar[cat].count
                    print '\nchildrens are\n'
                    print main_cat[main].similiar[cat].children
                    print "\n parents are\n"
                    print main_cat[main].similiar[cat].parent
                else:
                    print '\n\n suggested category is\n',cat,"\n"
                    print '\nsimiliar categories are\n'
                    for e in main_cat[cat].similiar:
                        print e
                    print main_cat[cat].count
                    print '\nchildrens are\n'
                    print main_cat[cat].children
                    print "\n parents are\n"
                    print main_cat[cat].parent
            else:
                print 'no_category_find'
