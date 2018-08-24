import wikipedia
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from nltk.corpus import stopwords
import os
import category_from_urls as cat_class

#this program identiifes concept for entity by mapping wikipedia text to different categories of category network
#we are breaking wiki text in n grams by removing stop words and then matching whether words of catyegory network are found in n grams


#token=wiki_text.split()
stop = stopwords.words('english')
category={}
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

gdelt_source_fetcher()
remove_redundant_category(category)

def v_text(text):
    t=text.split()
    #print t
    valid_text=" "
    for word in t:
        try:
            if word not in stop:
                valid_text=valid_text+word+" "
        except:
            pass
    #print valid_text
    return valid_text
#if 'delhi' in category:
#    print 'exists'
while True:
    try:
        output=[]
        cat=raw_input('\nEnter Entity Name\n')
        cat=cat.lower()
        concepts={}
        #ny = wikipedia.page(cat)
        #wiki_text=ny.content
        valid_text=wikipedia.summary(cat)
        wiki_text=v_text(valid_text)
            #print token
        #print wiki_text
        sentence=wiki_text.split('.,?:')
        for se in sentence:
            #print se+'\n'
            #if 'was' not in se:
            #    print se
                token=se.split()
                threegrams=ngrams(token,3)
                for element in list(threegrams):
                            # category_found string wil be used to may each concept to different categories of category network
                           category_found=""
                           #print 'three gramp is',element
                    #if '('.encode('utf-8') not in element and ')'.encode('utf-8') not in element:
                        #if element[1].strip('., ?').lower() not in stop and element[3].strip('., ?').lower() not in stop:
                           #print 'valid ones are',element
                           if element[0].strip('., ?').lower().encode("utf-8") in category:
                                   category_found=category_found+element[0]+" ,"#+" ".join(category[element[0]].parent)+" ,"
                                   #print category[(element[0].strip('., ?'))]
                           if  element[1].strip('., ?').lower().encode("utf-8") in category:
                                    category_found=category_found+element[1]+" ,"#+ " ".join(category[element[1]].parent)+" ,"
                                    #print category[(element[1].strip('., ?'))]
                           if  element[2].strip('., ?').lower().encode("utf-8") in category:
                                    category_found=category_found+element[2]+" ,"#+ " ".join(category[element[2]].parent)+" ,"
                                    #print category[(element[2].strip('., ?'))]
                               #print 'found in network',element
                           if len(category_found)>0:
                               item=" ".join(element).encode('utf-8')
                               if item not in concepts:
                                   output.append(item)
                                   concepts[item]=category_found

        for i in range(0,25):
            if '('.encode('utf-8') not in output[i] and ')'.encode('utf-8') not in output[i]:
                print output[i],"                               ",concepts[output[i]]
    except:
        pass


