import csv
import MySQLdb
import re
import wikipedia
import difflib
import networkx as nx
#import matplotlib.pyplot as plt
class node_info:
    def __init__(self):
        self.similiar=[]
        self.child={}
class unused_node:
    def __init__(self):
        self.similiar=[]
class sub_cat_node:
    def __init__(self):
        self.similiar=[]
        self.parent=[]
        self.children={}
def loose_match(s1,s2):
    seq = difflib.SequenceMatcher()
    try:
        seq.set_seqs(s1, s2)
        d=seq.ratio()*100
        d=int(d)
        return d
    except:
        return 0
def loose_match1(s1,s2):
    if s1<s2:
        x=len(s1)
        x=x*0.8
        x=(int)(x)
        st=s1[0:x]
        if st in s2:
            return True
    elif s2<s1:
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
def model_graph(parent,root,g):    
    if len(root.child)>0:
        for c in root.child:
            x=root.child[c]
            g.add_node(c)
            g.add_edge(parent,c,weight=x)
            
            #g.add_nodes_from([n_name,child])
        #for level in root.references:
         #   obj=category[level]
           # model_graph(obj,g)
        
def graph_plot():
    for node_check in main_cat:
        v=main_cat[node_check]
        model_graph(node_check,v,g)
def external_updation(main_wiki,sub_wiki,unidentified,main_sum,cat_sum):
    i=0
    if len(main_wiki)>0:
        for element in main_wiki:
            d=((float)(element[1]))/main_sum[0]
            main_cat[element[0]].child[unidentified]=d
            if unidentified in sub_cat:
                sub_cat[unidentified].parent.append(element[0])       
            else:
                x=sub_cat_node()
                x.parent.append(element[0])
                sub_cat[unidentified]=x
            i=i+1
            if i>=5:
                break
    i=0
    if len(sub_wiki)>0:
        for ch in sub_wiki:
            di=((float)(ch[1]))/cat_sum[0]
            sub_cat[ch[0]].children[unidentified]=di
            if unidentified in latest_entities:
                latest_entities[unidentified].parent.append(ch[0])       
            else:
                x=sub_cat_node()
                x.parent.append(ch[0])
                x.distribution=di
                latest_entities[unidentified]=x
            i=i+1
            if i>3:
                break
def wiki_check(cat):
    cat_distri_list=[]
    
    try:
        wiki_text=wikipedia.summary(cat)
        #ny = wikipedia.page(cat)
        #paragraph=ny.content.split('\n\n')
        cat_distri={}
        main_distri={}
        #x=len(paragraph)
        #for i in range(0,1):
   # print paragraph[i].strip('\n')
        #wiki_text=ny.content
        #print wiki_text
            #elements=paragraph[i]
            #print elements
        elements=wiki_text.split(" ")
        #print elements
        
        count=0
        for e in elements:
        #for e in elements.split(" "):
            e=e.lower()
            e=clean(e)
            #print e
            for ele in main_cat:
                if loose_match(ele,e)>=80:
                    #print ele
                    count=count+1
                    if main_distri.has_key(ele):
                        main_distri[ele]=main_distri[ele]+1
                    else:
                        main_distri[ele]=1
                #print main_distri
            for m in sub_cat:
                if loose_match(m,e)>=80:
                    count=count+1
                    if cat_distri.has_key(m):
                        cat_distri[m]=cat_distri[m]+1
                    else:
                        cat_distri[m]=1
                """parents=sub_cat[m]
                for p in parents:
                     if p in main_distri:
                         main_distri[p]=main_distri[p]+1
                     else:
                         main_distri[p]=1"""
        """print "\n distribution in sub category is"
        for w in sorted(cat_distri, key=cat_distri.get, reverse=True):
            c=sum(cat_distri.values())
            x=((float)(cat_distri[w]))/c
            print w,x,sub_cat[w].parent

        print "\n distribution in main category is"
        cnt=0
        for w in sorted(main_distri, key=main_distri.get, reverse=True):
            co=sum(main_distri.values())
            x=((float)(main_distri[w]))/co
            cnt=cnt+1
            print w,x"""
            

                #print cat,"is related to", el,"as",e
        #x=sorted(cat_distri, key=cat_distri.get, reverse=True)
        main_sum=[]
        sub_sum=[]
        #print sum(cat_distri.itervalues())
        sub_sum.append(sum(cat_distri.values()))
        main_sum.append(sum(main_distri.values()))
        x=sorted(cat_distri.iteritems(), key=lambda (k,v): (v,k),reverse=True)
        y=sorted(main_distri.iteritems(), key=lambda (k,v): (v,k),reverse=True)
        cat_distri_list.append(x)
        cat_distri_list.append(y)
        cat_distri_list.append(main_sum)
        cat_distri_list.append(sub_sum)
    except:
        print "no result"
        #return [[],[]]
    return cat_distri_list
def wiki_check1(cat):
    try:
        wiki_text=wikipedia.summary(cat)
        #print wiki_text
        elements=wiki_text.split(" ")
        #print elements
        print len(elements)
        cat_distri={}
        count=0
        for e in elements:
            e=e.lower()
            e=clean(e)
            #print e            
            for ele in main_cat:
                #print ele
                if loose_match(ele,e)>=80:
                #if loose_match(s1,s2):
                    count=count+1
                    if cat_distri.has_key(ele):
                        cat_distri[ele]=cat_distri[ele]+1
                    else:
                        cat_distri[ele]=1
        #print count

        for c in cat_distri:
                x=cat_distri[c]
                x=(float)(x)
                y=(x/count)*100
                print cat,"is related to", c,"with",y,"%"

                #print cat,"is related to", el,"as",e
    except:
        print "no result"
def check_for_sub_cat_similiar():
    #u_list=[]
    for element in unknown:
        c=clean(element)
        f=1
        for e in sub_cat:
            #if e in c or c in e:
            if loose_match1(e,c):
                t=sub_cat[e].similiar.append(element)
                f=0
                break
        if f==1:
            unresolved.append(element)
    del unknown[:]
    #return u_list
               #unknown.remove(element)
def check_for_parent(child,original):
    if child in main_cat:
        #print "true"
        return
    if child in unused_cat:
        return
    else:
        f=0
        for category in main_cat:
            if child in category or category in child:
            #if loose_match1(child,category):
                value=main_cat[category]
                value.similiar.append(original)
                main_cat[category]=value
                return
        for category1 in unused_cat:
            #if child in category1 or category1 in child:                
            if loose_match1(child,category1):
                value=unused_cat[category1]
                value.similiar.append(original)
                unused_cat[category1]=value
                return
        db = MySQLdb.connect("localhost",user="root",db="news_category_relation")
        cursor = db.cursor()
        sql="select category_name,children.count from category,children where parent_id=category_id and child_name='%s'"%(original)
        parent_list=[]
        try:
            cursor.execute(sql)            
            result=cursor.fetchall()
            parent_list=list(result)
        except:
            print "error in selection"
            #print x
            #if original=='cricket':
                #print result
        
        for row in parent_list:
            #p_name=row[0]            
            if row[1]>15:
                if row[0] in main_cat:
                    value=main_cat[row[0]]
                    value.child[original]=row[1]
                    main_cat[row[0]]=value
                    if original in sub_cat:
                        #ch=sub_cat[original]
                        #ch.append(p_name)
                        sub_cat[original].parent.append(row[0])
                    else:
                        x=sub_cat_node()
                        x.parent.append(row[0])
                        sub_cat[original]=x
                    f=1
                else:
                    for element in main_cat:
                        if row[0] in main_cat[element].similiar:
                            value=main_cat[element]
                            value.child[original]=row[1]
                            main_cat[element]=value
                            #print original,row[0],element
                            f=1
                            break
        if f==0:
            unknown.append(original)
            return
        else:
            return
def clean(ele):
    word=""
    for e in ele:
        if e.isalpha():
            word=word+e
    return word
def check_in_category_net(item):
    f=0
    if item in main_cat:
        print 'simililiar categories are',main_cat[item].similiar
        print 'childrens are',main_cat[item].child
        return 1
    if item in sub_cat:
        for p in sub_cat[item].parent:
            print item ,"belongs to",p,'with',main_cat[p].child[item]
        f=1
        #return 1
    if item in latest_entities:
        for p in latest_entities[item].parent:
            print item ,"belongs to",p,'with',sub_cat[p].children[item],'with',sub_cat[p].parent
        return 1
    else:
        for element in main_cat:
            if loose_match1(element,item):
                print element , main_cat[element].similiar
                return 1
        for element in sub_cat:
            if loose_match1(element,item):
                f=1
                for p in sub_cat[element].parent:
                    print item ,"belongs to",p,'with',main_cat[p].child[item]
                #return 1
        """if len(latest_entities)>0:
            for el in latest_entities:
                if loose_match1(e1,item):
                    for p in latest_entities[e1].parent:
                        print item ,"belongs to",p,'with',sub_cat[p].children[item]
                    return 1"""
    if f==0:
        return 0
    else:
        return 1

main_path="D://Thesis//data//exported_data//latest indian category with count greater than 9"
#path='D://Thesis//data//exported_data//category_count less than 100'
m_path='D://Thesis//data//exported_data//main_category.txt'
unusedcat_path='D://Thesis//data//exported_data//unused.txt'
f=open(main_path+".CSV","rb")
#f2=open(path+".CSV",'rb')
f3=open(m_path,'r')
f_unused=open(unusedcat_path,'r')
main_category=csv.reader(f,delimiter=';')
rows=list(main_category)
#subcategory=csv.reader(f2,delimiter=';')
main_cat={}
unused_cat={}
sub_cat={}
latest_entities={}
unknown=[]
x=f3.readlines()
for cat in x:
    cat=cat.rstrip("\n")
    cat=cat.lower()
    node=node_info()
    main_cat[cat]=node
f3.close()
un_cat=f_unused.readlines()

for u in un_cat:
    u=u.rstrip("\n")
    u=u.lower()
    u_node=unused_node()
    unused_cat[u]=u_node


for row in rows:
    x=row[0].split(";")
    e=clean(x[0])
    #e=x[0].replace("!@#$%^&*()[]{};:,./<>?\|`~-=_+-", "")
    check_for_parent(e,x[0])

"""print "\n\n valid and similiar categories are"
for e in main_cat:
    print e,main_cat[e].similiar

print "\n\nchildrens are"
for e in main_cat:
    print e,main_cat[e].child
    print "\n"""


print "\n\n unused categories are"
for e in unused_cat:
    print e,unused_cat[e].similiar
    print "\n"

#print "unknown categories are\n"
#print unknown
#print len(unknown)
#loose_match('politics','politician')
#print "\n"
#input_cat=raw_input("enter the categories")
#wiki_check('arvind kejriwal')
#print using_wiki[0],using_wiki[1]
unresolved=[]
check_for_sub_cat_similiar()
print 'unresolved categories are'
"""print unresolved
print len(unresolved)"""
"""print "\n\n sub categories and similiar sub categories are"
for e in sub_cat:
    print e,sub_cat[e].similiar
    print "\n"""

while True:
    data=raw_input("enter the category or entity you want to identify\n")
    check_in_category_net(data)
#print "using wiki results are in main category"   

#print sub_cat['election'].parent
"""while 1:
    data=raw_input("enter the category or entity you want to identify\n")
    x=check_in_category_net(data)
    if x==0:
        x=wiki_check(data)
        if len(x)>0:
            print x[1]
            for element in x[0]:
                print element,sub_cat[element[0]].parent
            external_updation(x[1],x[0],data,x[2],x[3])
        else:
            print 'no result'"""
"""g=nx.DiGraph()
graph_plot()
nx.draw(g)
plt.show()
graph_pos=nx.spring_layout(g)
nx.draw_networkx_nodes(g,graph_pos,node_size=2000, 
                           alpha=0.3, node_color='blue')
nx.draw_networkx_edges(g,graph_pos,width=1,
                           alpha=0.3,edge_color='red')
nx.draw_networkx_labels(g, graph_pos,font_size=12,
                            font_family='sans-serif')
#if 'business' in g:
print nx.dfs_successors(g,'business')
plt.show()"""

