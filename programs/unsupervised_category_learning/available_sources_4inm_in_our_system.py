import os


sources={}
path="D://Thesis//data//domain_name//news_sources_ranking//based_on_4inm_website//"
regions=os.listdir(path)
print regions
source_asia=regions[1]
source_europe=regions[2]
asia_coountries=os.listdir(path+source_asia)
europe_countries=os.listdir(path+source_europe)

"""for country in asia_coountries:
    file=path+source_asia+"//"+country
    f=open(file,"r")
    files=f.read().split("\n")
    f.close()
    for e in files:
        if e not in sources:
            sources[e]=1
for country in europe_countries:
    file=path+source_europe+"//"+country
    f=open(file,"r")
    files=f.read().split("\n")
    f.close()
    for e in files:
        if e not in sources:
            sources[e]=1"""


gdelt_path="D://Thesis//data//domain_name//category_gdelt_valid_source//"
gdelt_sources=os.listdir(gdelt_path)
cou=0
for element in gdelt_sources:
    element="http://"+element.rstrip(".txt")
    if element not in sources:
        #print element
        sources[element]=1
        cou=cou+1
print cou

gdelt_path1="D://Thesis//data//domain_name//gdelt_heuristic_approach_1//"
indian=os.listdir(gdelt_path1)
cou=0
for element in indian:
    #element="http://"+element.rstrip(".txt")

    if element not in sources:
        element="http://"+element.rstrip(".txt")
        sources[element]=1
        cou=cou+1
print cou

count=1
"""top_200="D://Thesis//data//domain_name//news_sources_ranking//based_on_4inm_website//"
f1=open(top_200+"top_200_news_sources_world.txt","r")
elements=f1.read().split("\n")
for e in elements:
    if e not in sources:
        #sources[e]=1
        count=count+1
        print e
print count"""

co=0
for i in range(8,len(regions)):
    print regions[i]
    file=path+regions[i]
    f=open(file,"r")
    files=f.read().split("\n")
    f.close()
    coun=0
    for e in files:
        if e not in sources:
            sources[e]=1
            print e
            coun=coun+1
            co=co+1
    print coun
print co,"\n"
count1=0
indian_sources="D://Thesis//data//domain_name//news_sources_ranking//based_on_4inm_website//India.txt"
f2=open(indian_sources,"r")
files=f2.read().split("\n")
for ele in files:
    if ele not in sources:
        print ele
        count1=count1+1
print count1
print co+count1
#print len(sources)




