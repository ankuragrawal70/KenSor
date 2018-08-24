import re
inv_path="D://Thesis//data//domain_name//main_category_crawler//invalid_links.txt"
f_inv=open(inv_path,"a+")
invalid_urls=f_inv.read().split("\n")
f_inv.close()
duplicates={}
inv_cat={}
for x in invalid_urls:
    if x not in duplicates:
        duplicates[x]=1
for u in duplicates:
    elements=u.split("/")
    for e in elements:
        if len(e)>3 and len(e)<20:
            if "." not in e:
            #if re.match(r'?.!/;:#&+~=@', s):
                if e not in inv_cat:
                    inv_cat[e]=1
                else:
                    inv_cat[e]=inv_cat[e]+1
print len(inv_cat)

x=sorted(inv_cat.iteritems(), key=lambda (k,v): (v,k),reverse=True)
for ca in x:
    print ca[0],ca[1]