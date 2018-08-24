
import csv
import os
import pygeoip
#import domain_to_location
import socket
#import geoip
import geoip2.database
def location(hostname):
        list1=[]
        try:
            addr = socket.gethostbyname(hostname)
            reader = geoip2.database.Reader('D:/Thesis/GeoLite2-City.mmdb/home/tjmather/mm_website/geoip/BuildDatabase/GeoLite2-City.mmdb')
            #reader = geoip2.database.Reader("D:/Thesis/GeoLite2-Country.mmdb/home/tjmather/mm_website/geoip/BuildDatabase/GeoLite2-Country.mmdb")
            response = reader.city(addr)
            if response.country.name is not  None:
                list1.append(response.country.name.encode("utf-8"))
            else:
                list1.append(response.country.name)
            list1.append(response.city.name)
            list1.append(response.postal.code)
            list1.append(response.location.latitude)
            list1.append(response.location.longitude)
        except:
            pass
        
        return list1
def check_for_special_char(s):
    for i in s:
        if i.isdigit() or i in " ?.!/;:":
            return True
            break
    return False
            
def check_for_category(cat):
    if len(cat)>3 and len(cat)<20 and check_for_special_char(cat)is not True:
        return True
    else:
        return False
    
def csv_reader(file_obj,filename,url,category,domain):
    reader1 = csv.reader(file_obj,delimiter='\t')
    row=list(reader1)
    #row is a set of rows of the given file
    #url is a hash_map that contains the urls and their count 
    for row1 in row:
        x=len(row1)
        domain_name=row1[x-1]
        if url.has_key(domain_name):
            url[domain_name]=url[domain_name]+1
        else:
            url[domain_name]=1
    
    print "for filename",filename
    print "\ttotal unique urls are",len(url)
    for element in url:
        #split each url by / to get category
        splitted_url=element.split("/")
        length=len(splitted_url)
        if length>1:
            dom=splitted_url[2]
            print dom
            if domain.has_key(dom):
                #domain[dom]=domain[dom]+1
                pass
            else:
                category_list=[]
                category_hash={}
                category_list.append(location(dom))
                category_list.append(category_hash)
                domain[dom]=category_list
                # check for each componenet of splitted url weather it is a category or
        #not and update information regarding each url
            domain_info=domain[dom]
            #print dom,"\n",domain_info[0],"\n"
            t=domain_info[1]
            for i in range(3,len(splitted_url)):
                y=splitted_url[i].strip("")
                if check_for_category(y):
                    if category.has_key(y):
                        category[y]=category[y]+1
                    else:
                        category[y]=1
                    if t.has_key(y):
                        t[y]=t[y]+1
                    else:
                        t[y]=1
    d_length=len(domain)
    c_length=len(category)
    #print "\ttotal unique domains are",d_length
    #print "\ttotal unique category are",c_length
    #i=0
    """for inf in domain:
        loc=location(inf)
        
        if i<40:
            print "\n"                
            print inf,"\n",loc[0],"\ncity: ",loc[1],"\npostal:",loc[2],"\nlatitude:",loc[3],"\nlongitude:",loc[4]
            i=i+1
            
        else:
            break"""

        
  
   

url={}
category={}
domain={}

#output path
"""path= "D://Thesis//data//category_data//category.CSV"
b=open(path,"wt")
c=csv.writer(b,delimiter='\t')
c.writerow(["Date   ","total_url   ","total_categories"])"""

#input path
path="D://Thesis//data//"
filename=os.listdir(path)
for i in range(0,2):
    file1=path+filename[i]
    f=open(file1,"rb")
    date=filename[i][:-11]
    ac_date=date[0:4]+"/"+date[4:6]+"/"+date[6:len(date)]
    csv_reader(f,ac_date,url,category,domain)
    f.close()
    print "\n"
#b.close()
#print "domain urls are",len(domain)
path= "D://Thesis//data//category_data//category.CSV"
b=open(path,"wt")
c=csv.writer(b,delimiter='\t')
for e in domain:
        x=domain[e]
        print e,"\n",x[0],"\n",x[1]
        c.writerow([e,x[0],x[1]])
        print "\n"
            

"""print "categories are"
for element in category:
        print element,category[element]"""
