import os
path="D://Thesis//data//domain_name//main_base_categories_50//"
files=os.listdir(path)
sources=[]
for f in files:
    path1=path+f
    f_domain=open(path1,'r')
    source_file=f_domain.read().split("\n")
    for sou in source_file:
        sources.append(sou)


print len(sources)

"""path1="D://Thesis//data//domain_name//domains_related_to_a_category_all_10//"
all_cate=os.listdir(path1)

for f in all_cate:
    if f not in files:
        cat_path=path1+f
        f_n=open(cat_path,'r')
        all_sources=f_n.read().split("\n")
        for so in source_file:
            if so not in sources:
                unimportant.append(so)"""
"""unimportant=[]
path2="D://Thesis//data//domain_name//domains_related_to_category_path//"
f2=open(path2+'domain_latest.txt','r')
files1=f2.read().split('\n')
for file in files1:
    if file not in sources:
        unimportant.append(file)"""


"""print len(unimportant)
for i in range(0,len(sources)):
    path1="D://Thesis//data//domain_name//domains_related_to_category_path//main_category//"
    f=open(path1+'file1.txt','a+')
    files=f.write(sources[i]+'\n')
    f.close()"""

"""for i in range(0,100000):
    path1="D://Thesis//data//domain_name//domains_related_to_category_path//unimportant//"
    f=open(path1+'file1.txt','a+')
    files=f.write(unimportant[i]+'\n')
    f.close()"""

"""for i in range(100000,len(unimportant)):
    path1="D://Thesis//data//domain_name//domains_related_to_category_path//unimportant//"
    f=open(path1+'file2.txt','a+')
    files=f.write(unimportant[i]+'\n')
    f.close()"""

"""path1="D://Thesis//data//domain_name//domains_related_to_category_path//unimportant//"
f=open(path1+'file1.txt','a+')
files=f.read().split('\n')
f.close()"""

"""path1="D://Thesis//data//domain_name//domains_related_to_category_path//unimportant//"
f=open(path1+'file1.txt','a+')
files=f.read().split('\n')
f.close()"""