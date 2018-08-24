import urllib2, httplib
from BeautifulSoup import BeautifulSoup
import threading
def append_log(message):
    print message

def get_web_page(address,active_domain,thread_id):
    try:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        request = urllib2.Request(address, None, headers)
        response = urllib2.urlopen(request, timeout=20)
        try:
            active_domain[address+'\n']=1
            print 'valid address',address,'    thread id',thread_id
            return response.read()

        finally:
            response.close()
    except urllib2.HTTPError as e:
        error_desc = httplib.responses.get(e.code, '')
        print 'error in request'
        #append_log('HTTP Error: ' + str(e.code) + ': ' +
        #          error_desc + ': ' + address)
    except urllib2.URLError as e:
        #append_log('URL Error: ' + e.reason[1] + ': ' + address)
        print 'error in url'
    except :
        print 'Unknown Error: '

def process_web_page(data):
    if data is not None:
        print BeautifulSoup(data)
    else:
        pass # do something else

#data = get_web_page('http://www.thehindu.com/')
#process_web_page(data)

#data = get_web_page('http://docs.python.org/copyright.html')
#process_web_page(data)
def type_thread(list1,thread_id):
    d_map={}
    for item in list1:
        get_web_page(item,d_map,thread_id)
    d_path2="D://Thesis//data//domain_name//gdelt_valid_domain.txt"
    f=open(d_path2,'a')
    x=d_map.keys()
    s=''.join(x)
    f.write(s)
    f.close()
    print len(d_map)

#active_domain={}
d_path1="D://Thesis//data//domain_name//gdelt_domain1.txt"
f=open(d_path1,'r')
e=f.read().split('\n')
domain_list=[]
#domain_list=[[e[0],e[1]],[e[2],e[3]]]
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
    id=j+1
    t=threading.Thread(target=type_thread, args = (element,id,))
    j=j+1
    #t.daemon=True
    t.start()


"""d_path2="D://Thesis//data//domain_name//gdelt_valid_domain.txt"
f=open(d_path2,'w')
x=actice_domain.keys()
s=''.join(x)
f.write(s)
print len(active_domain)"""