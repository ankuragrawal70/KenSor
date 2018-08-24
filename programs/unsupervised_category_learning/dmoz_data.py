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
import matplotlib.pyplot as plt
class category_node:
    def __init__(self,name):
        self.c_name=name
        self.count=1
        self.parent=[]
        self.references={}
        self.news_sources={}
def clean(ele):
    word=""
    for e in ele:
        if e.isalpha():
            word=word+e
    return word
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
    if len(cat)>2 and len(cat)<20 and check_for_special_char(cat)is not True:
        return True
    else:
        return False
def wiki_check(cat):
    cat_distri={}
    cat=clean(cat)
    try:
        wiki_text=wikipedia.summary(cat)
        #print wiki_text
        elements=wiki_text.split(" ")
        #print elements
        #cat_distri={}
        count=0
        for e in elements:
            e=e.lower()
            #e=clean(e)
            #print e
            for ele in main_cat:
                #print ele
                if loose_match(ele,e)>=80:
                #if loose_match1(ele,e):
                    count=count+1
                    if cat_distri.has_key(ele):
                        cat_distri[ele]=cat_distri[ele]+1
                    else:
                        cat_distri[ele]=1
        for w in sorted(cat_distri, key=cat_distri.get, reverse=True):
            c=sum(cat_distri.values())
            x=((float)(cat_distri[w]))/c
            print w,x,sub_cat[w].parent


    except:
         print "no result"

def url_category_list(s):
    #print s
    cat_list=[]
    if s[0]=='/':
        #if len(s)>1:
            sp=s.split('/')[1:]
    else:
        sp=s.split('/')[1:]
    for i in range(0,len(sp)):
        y=sp[i].strip('-_,. :').lower()
        if check_for_category(y):
             cat_list.append(y)
    #if 'http://www.thehindu.com' in s:
    #print cat_list
    return cat_list
def category_domain_info(element,category,source_domain):
        #print element
        cat_list=url_category_list(element)
        #print cat_list
        #if element=='http://www.dmoz.com/Sports/Baseball/Sports/Baseball/News_and_Media/':
        #    print cat_list
        #print cat_list
        i=0
        while i<len(cat_list)-1:
            if category.has_key(cat_list[i]):
                ref=category[cat_list[i]]
                ref.count=ref.count+1
                if ref.news_sources.has_key(source_domain):
                    ref.news_sources[source_domain]=ref.news_sources[source_domain]+1
                
                else:
                    ref.news_sources[source_domain]=1
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
                new_cat.news_sources[source_domain]=1
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
                    if obj.news_sources.has_key(source_domain):
                            obj.news_sources[source_domain]=obj.news_sources[source_domain]+1
                    else:
                            obj.news_sources[source_domain]=1
                    category[cat_list[i]]=obj
                else:
                      new_cat=category_node(cat_list[0])
                      new_cat.count=1
                      new_cat.news_sources[source_domain]=1
                      category[cat_list[0]]=new_cat
        #ignore for a cat list containing only single category
        if len(cat_list)==1:
                 #print cat_list
                 if category.has_key(cat_list[0]):
                    obj=category[cat_list[0]]
                    obj.count=obj.count+1
                    if obj.news_sources.has_key(source_domain):
                            obj.news_sources[source_domain]=obj.news_sources[source_domain]+1
                    else:
                            obj.news_sources[source_domain]=1
                    category[cat_list[0]]=obj
                 else:
                      new_cat=category_node(cat_list[0])
                      new_cat.count=1
                      new_cat.news_sources[source_domain]=1
                      category[cat_list[0]]=new_cat
def check_validity(h_link,domain_name,level):
    
    if domain_name in h_link:
            level[h_link.encode('utf-8')]=1
    else:
        if h_link[0]=='/':
            if domain_name[len(domain_name)-1]!='/':
                
                    #print domain_name+h_link
                level[(domain_name+h_link).encode('utf-8')]=1
            else:
                l=len(domain_name)-1
                x=domain_name[:l]
                level[(x+h_link).encode('utf-8')]=1


def find_links(domain_name,level):
    #print domain_name
    try :      
        web_page = urllib2.urlopen(domain_name,timeout=4)
        soup = BeautifulSoup(web_page)
        c=soup.find_all('a')
        for e in c:
            #print e
            try:
                l=e['href']
                if l!=domain_name:
                    check_validity(l,domain_name,level)
            except:
                print 'error after parsing links'
                pass
   
    except:
        print 'error in main link'
        pass
"""level1={}
level2={}
find_links('http://www.dmoz.com',level1)
path='D://Thesis//data//Dmoz data//download//'
path1=path+'level1.txt'
f=open(path1,'a+')
for e in level1:
    #print e
    f.write(e+'\n')
    print 'level 1',e
f.close()
category={}
for ele in level1:
    #print ele    find_links(ele,level2)
    #category_domain_info(ele,category)

    #category_domain_info(e,category)

path2=path+'level2.txt'
#print sorted(category.keys())
f1=open(path2,'a+')
print 'level 2 categories are\n'
for l2 in level2:
    f1.write(l2+'\n')
    print 'level2',l2
l2.close()
    #category_domain_info(l2,category)"""

"""for e in category:
    if len(category[e].parent)==0:
        print e,category[e].references
while True:
    x=raw_input('enter category')
    try:
        print category[x].parent
        print category[x].references
    except:
        print 'no category found'
        pass"""
def dmoz_source():
    """dmoz_path='D://Thesis//data//Dmoz data//download//'
    file_list=os.listdir(dmoz_path)
    #category={}
    for i in range(0,len(file_list)):
    #for i in range(0,100):
        p=dmoz_path+file_list[i]
        f=open(p,'r')
        c_info=f.read().split('\n')
        if len(c_info)>0:
            #f_name='http://'+file_list[i].rstrip('.txt')
            #print f_name
            for e in c_info:
                #print e
                category_domain_info(e,dmoz_cat,'http://www.dmoz.com')
        f.close()"""
    dmoz_path='D://Thesis//data//domain_name//sources_in_dmoz//'
    file_list=os.listdir(dmoz_path)
    for i in range(0,len(file_list)):
        #print file_list[i]
    #for i in range(0,100):
        #if file_list[i]=='indianexpress.com':
        #    print 'exiusts'
        p=dmoz_path+file_list[i]
        f=open(p,'r')
        c_info=f.read().split('\n')
        cat={}
        if len(c_info)>0:
            f_name='http://'+file_list[i].rstrip('.txt')
            #print f_name
            i=0
            for e in c_info:
                #print e
                category_domain_info(e,cat,f_name)
                i=i+1
                # to store info about a news source and category
                dmoz_cat[f_name]=cat
                if i==len(c_info)-1:
                    break
                
        f.close()
def gdelt_source_fetcher():
    gdelt_path='D://Thesis//data//domain_name//category_gdelt_valid_source//'
    file_list=os.listdir(gdelt_path)
    for i in range(0,len(file_list)):
    #for i in range(0,500):
        p=gdelt_path+file_list[i]
        f=open(p,'r')
        c_info=eval(f.read())
        cat={}
        if len(c_info)>0:
            f_name='http://'+file_list[i].rstrip('.txt')
            #print f_name
            for e in c_info:
                category_domain_info(e,cat,f_name)
                gdelt_cat[f_name]=cat
        f.close()
        #break
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
        cat={}
        for e in category_url:
                category_domain_info(e,cat,f_name)
                i=i+1
                gdelt_cat[f_name]=cat
                if i==len(category_url)-1:
                    break
        f.close()"""
"""def gdelt_event_fetcher():
        db = MySQLdb.connect("localhost",user="root",db="news_category_relation")
        cursor = db.cursor()
        sql="select category_name from category"
        c_list=[]
        try:
            cursor.execute(sql)            
            result=cursor.fetchall()
            c_list=list(result)
        except:
            print "error in selection"
        for e in c_list:
            if e[0] not in gdelt_event_cat:
                gdelt_event_cat[e[0]]=1"""
dmoz_cat={}
gdelt_cat={}
#gdelt_event_cat={}
#dmoz_source()
#print len(dmoz_cat)
gdelt_source_fetcher()
#gdelt_event_fetcher()
#y=sorted(category.items(), key=lambda kv: len(kv[1].news_sources), reverse=True)

"""for e in y:
    print e[0],len(e[1].news_sources)"""
"""print 'total categories are',len(category)

cou=0
for e in category:
    if len(category[e].parent)==0:
       cou=cou+1
print 'total categories on level 1 are',cou
a=0
for x in category:
    if len(category[x].news_sources)==1:
        a=a+1
print 'categpry that occurs with only one news source',a

print 'top 20 categories with frequent counts are'"""
"""for i in range(0,20):
    print y[i][0],y[i][1].count"""
"""for e in category:
    if len(category[e].news_sources)"""

"""count=0
count1=0
count2=0
for c in dmoz_cat:
    if c in gdelt_cat:
        count=count+1
    else:
        for x in gdelt_cat:
            if x in c or c in x:
                #print x,c
                count2=count2+1
                break
        else:
            count1=count1+1
print len(dmoz_cat)
print len(gdelt_cat)
print 'no of common categories in dmoz and gdlt are',count
print count2
print 'no of categories not found are',count1"""
"""count=0
count1=0
count2=0
for c in dmoz_cat:
    if c in gdelt_cat:
        count=count+1
    else:
        for x in gdelt_cat:
            if x in c or c in x:
                #print x,c
                count2=count2+1
                break
        else:
            count1=count1+1
print len(dmoz_cat)
print len(gdelt_cat)
print 'no of common categories in dmoz and gdlt are',count
print count2
print 'no of categories not found are',count1"""

"""statistics={}
dmoz_sources=0
dmoz_category_count=0
gdelt_sources=0
gdelt_category_count=0
for source in dmoz_cat:
    
    dmoz_info=dmoz_cat[source]
    dmoz_category_count=dmoz_category_count+len(dmoz_info)

    gdelt_info=[]
    if gdelt_cat.has_key(source):
        gdelt_info=gdelt_cat[source]
        gdelt_sources=gdelt_sources+1
        dmoz_sources=dmoz_sources+1
        gdelt_category_count=gdelt_category_count+len(gdelt_info)
    d_match=0
    count1=0
    in_match=0
    for c in dmoz_info:
        if c in gdelt_info:
            d_match=d_match+1
        else:
            for x in gdelt_info:
                if x in c or c in x:
                    #print x,c
                    in_match=in_match+1
                    break
            else:
                count1=count1+1
    
    #print 'no of common categories in dmoz and gdlt are',d_match
    #print 'indirect match',in_match
    match=d_match+in_match
    
    #print source,len(dmoz_info),' ',len(gdelt_info),' ',match,' ',formula
    list1=[len(dmoz_info),len(gdelt_info),match]
    statistics[source]=list1"""

"""print 'based on maximum in dmoz'
y=sorted(statistics.items(), key=lambda kv: kv[1][0], reverse=True)
for i in range(0,20):
    print y[i]
print '\n\n based on minimum in dmoz'
y=sorted(statistics.items(), key=lambda kv: kv[1][0])
for i in range(0,20):
    print y[i]
print '\n\n based on maximum difference based on dmoz in gdelt for a news source'
x=sorted(statistics.items(), key=lambda kv: (kv[1][0]-kv[1][1]), reverse=True)
for i in range(0,30):
    print x[i]

print '\n\n based on maximum difference based on gdeltfor a news source'
z=sorted(statistics.items(), key=lambda kv: (kv[1][1]-kv[1][0]),reverse=True)

print '\n\n based on maximum difference based on matched'
z=sorted(statistics.items(), key=lambda kv: (kv[1][2]-kv[1][0]),reverse=True)
for i in range(0,30):
    print z[i]

# average category per
x=len(dmoz_cat)
y=len(gdelt_cat)


print 'dmoz sources',dmoz_sources
print 'gdelt sources',gdelt_sources
print 'average in matched dmoz',float(dmoz_category_count)/dmoz_sources
print 'average matched in gdelt',float(gdelt_category_count)/gdelt_sources
print x
print y
c=0
for e in dmoz_cat:
    c=c+len(dmoz_cat[e])
print 'total category in dmoz',c
d=0
for g in gdelt_cat:
    d=d+len(gdelt_cat[g])
print 'total category in dmoz',d
print 'average in dmoz',float(c)/x
print 'average in gdelt',float(d)/x"""
def model_graph(parent,root,g):
    if len(root.references)>0:
        for c in root.references:
            x=root.references[c]
            g.add_node(c)
            g.add_edge(parent,c,weight=x)

            #g.add_nodes_from([n_name,child])
        #for level in root.references:
         #   obj=category[level]
           # model_graph(obj,g)
main_cat=gdelt_cat["http://www.thehindu.com"]
#wiki_check('Arvind Kejriwal')
def graph_plot(node_check):
        #node_check="business"
    #for node_check in main_cat:
        try:
            v=main_cat[node_check]
            model_graph(node_check,v,g)
        except:
            print 'no category found'



g=nx.DiGraph()

while True:
    c=raw_input("enter category")

    #nx.draw(g)
    #plt.show()
    try:
        print main_cat[c].references
        print main_cat[c].parent

        graph_plot(c)
        graph_pos=nx.spring_layout(g)
        nx.draw_networkx_nodes(g,graph_pos,node_size=3000,
                                   alpha=0.3, node_color='green')
        nx.draw_networkx_edges(g,graph_pos,width=1,
                                   alpha=0.3,edge_color='red')
        nx.draw_networkx_labels(g, graph_pos,font_size=12,
                                   font_family='sans-serif')
        #if 'business' in g:
        print nx.dfs_successors(g,c)
        plt.show()
    except:
        print 'invalid'
        pass


"""while True:
    source=raw_input('enter source')
    try:
        dmoz_info=dmoz_cat[source]
        gdelt_info=[]
        if gdelt_cat.has_key(source):
            gdelt_info=gdelt_cat[source]
        d_match=0
        count1=0
        in_match=0
        for c in dmoz_info:
            if c in gdelt_info:
                d_match=d_match+1
            else:
                for x in gdelt_info:
                    if x in c or c in x:
                        #print x,c
                        in_match=in_match+1
                        break
                else:
                    count1=count1+1
        match=d_match+in_match
        print source,len(dmoz_info),' ',len(gdelt_info),' ',match
        print 'categories using dmoz are'
        for element in dmoz_info:
            print element,dmoz_info[element].parent,dmoz_info[element].references

        print '\n\n\ncategories using gdelt projects are'
        for ele in gdelt_info:
            print ele,gdelt_info[ele].parent,gdelt_info[ele].references
    except:
        pass"""
    #print 'no of common categories in dmoz and gdlt are',d_match"""
