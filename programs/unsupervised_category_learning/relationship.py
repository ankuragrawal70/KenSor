import wikipedia
import nltk
import difflib
import operator
from nltk import word_tokenize
from nltk.util import ngrams
from nltk.corpus import stopwords
import common_categories as cat_info
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
"""def similiar_cat():
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
                    break"""
def similiar_cat(c_list):
    similiar_list=[0]*len(c_list)
    check_list=[0]*len(c_list)
    for i in range(0,len(c_list)-1):
        max1=0
        temp=''
        index=0
        flag=0
        for j in range(i+1,len(c_list)):
            if c_list[j] in c_list[i] or c_list[i] in c_list[j]:
                flag=1
                if check_list[j]!=0:
                    similiar_list[j].append(c_list[i])
                else:
                    check_list[j]=-1
                    similiar_list[j]=[c_list[j],c_list[i]]
        if flag==0:
            similiar_list[i]=c_list[i]

    if check_list[len(c_list)-1]==0:
        similiar_list[len(c_list)-1]=c_list[len(c_list)-1]
    #print similiar_list
    y=[]
    y=filter(lambda a: a != 0, similiar_list)
    print len(c_list)
    print len(y)
    print y
    return y
    #for e in y:
    #    print y
    """for j in range(i+1,len(c_list)):
            x=loose_match(c_list[i],c_list[j])
            if x>max1:
                     temp=c_list[j]
                     max1=x
                     index=j
        if temp!='' and max1>80:
            print temp,c_list[i]
            if check_list[index]!=0:
                similiar_list[index].append(c_list[i])
            else:
                list1=[c_list[index],c_list[i]]
                similiar_list[index]=list1
                check_list[index]=-1
        similiar_list[i]=c_list[i]
    print similiar_list"""
        
def wiki_result(cat_name,relatives):
    #text=wikipedia.summary(cat_name)
    ny=wikipedia.page(cat_name)
    text=ny.content
    sentence=nltk.sent_tokenize(text)
    #print sentence
    #token=text.split()
    match_found=[]
    for s in sentence:
        for r in relatives:
            if r in s and r not in match_found:
                print r
                print s+'\n'
                match_found.append(r)
        """else:
                for w in s:
                    if w in r or r in w:
                        print r
                        print w+'\n'
                        if w not in match_found:
                             match_found.append(w)""" 
    print len(relatives)
    print len(match_found)

while True:
    try:
        c=raw_input('enter category')
        parent_child=cat_info.cat_result(c)
        parent=parent_child[0]
        children=parent_child[1]
        c_list=children.keys()
        similiar_cat(c_list)
        wiki_result('business',c_list)
    except:
        print 'no category found'
