"""import geoip2.webservice
client = geoip2.webservice.Client(42, 'license_key')
response = client.insights('128.101.101.101')
response.country.name"""
import geoip2.database
import socket
import os
def execution(hostname,id1):
    try:
        hostname=hostname.rstrip('.txt')
        addr = socket.gethostbyname(hostname)
        print addr
        reader = geoip2.database.Reader('D:/Thesis/GeoLite2-City.mmdb/home/tjmather/mm_website/geoip/BuildDatabase/GeoLite2-City.mmdb')
        #reader = geoip2.database.Reader("D:/Thesis/GeoLite2-Country.mmdb/home/tjmather/mm_website/geoip/BuildDatabase/GeoLite2-Country.mmdb")
        response = reader.city(addr)
        loc_info=str(response.country.name)+"\n"+str(response.city.name)+"\n"+str(response.postal.code)+"\n"+str(response.location.latitude)+"\n"+str(response.location.longitude)

        print loc_info
        print reader.isp(addr)
        """path1="D://Thesis//data//domain_name//gdelt_domain_locations//"
        path2=path1+hostname+'.txt'
        f=open(path2,'a+')
        f.write(loc_info)
        f.close()
        print id1,hostname,'completed'"""
    except:
        print 'not found in database',hostname
execution('www.cnn.com',1)

"""files_path="D://Thesis//data//domain_name//category_gdelt_valid_source//"
all_sources=os.listdir(files_path)
check_path="D://Thesis//data//domain_name//gdelt_domain_locations/"
processed=os.listdir(check_path)

e=[]
for item in all_sources:
    if item not in processed:
        e.append(item)
domain_list=[]
#domain_list=[[e[0],e[1]],[e[2],e[3]]]
del all_sources[:]
del processed[:]
i=0
while 1:
    if (i+3000)<len(e):
       j=i+3000
       list1=e[i:j]
       domain_list.append(list1)
       i=j
    else:
        j=i+len(e)-1
        list1=e[i:j]
        domain_list.append(list1)
        break
j=0
for element in domain_list:
    print len(element)"""
"""for element in domain_list:
    id=j+1
    t=threading.Thread(target=type_thread, args = (element,id,))
    j=j+1
    #t.daemon=True
    t.start()"""