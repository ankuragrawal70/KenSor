import os
main_cat="D://Thesis//data//domain_name//category_gdelt_valid_source//"
indian_path="D://Thesis//data//domain_name//gdelt_heuristic_approach_1//"
indian_sources=os.listdir(indian_path)
d_path="D://Thesis//data//domain_name//domains_related_to_category_path//"
f1=open(d_path+"all_sources.txt",'a+')

files=os.listdir(main_cat)
"""for e in  files:
    e="http://"+e.rstrip(".txt")
    f1.write(e+"\n")"""
for file in indian_sources:
    if file not in files:
        url="http://"+file.rstrip(".txt")
        f1.write(url+"\n")

f1.close()
all_categories=[]
"""top_path="D://Thesis//data//domain_name//main_base_categories_50//"
top_cat=os.listdir(top_path)
for e in files:
    if e not in top_cat:
        all_categories.append(e)"""

#print len(all_categories)
#input_domain_path="D://Thesis//data//domain_name//main_base_categories_50//"
#all_categories=os.listdir(input_domain_path)
#print len(all_categories)
"""all_sources=[]
for catego in all_categories:
        path1="D://Thesis//data//domain_name//main_categories//"+catego
        f_local=open(path1,'r')
        sources=f_local.read().split("\n")
        all_sources=all_sources+sources
d_path="D://Thesis//data//domain_name//domains_related_to_category_path//main_category_50//domain_file.txt"
f_file=open(d_path,'w')
f_file.write("\n".join(all_sources))
print len(all_sources)"""