import struct
import sys
import urllib
import urllib2
import httplib
import re
import os
import time
import xml.etree.ElementTree
import fileinput
import threading
import MySQLdb

class RankProvider(object):
    """Abstract class for obtaining the page rank (popularity)
from a provider such as Google or Alexa.

"""
    def __init__(self, host, proxy=None, timeout=30):
        """Keyword arguments:
host -- toolbar host address
proxy -- address of proxy server. Default: None
timeout -- how long to wait for a response from the server.
Default: 30 (seconds)

"""
        self._opener = urllib2.build_opener()
        if proxy:
            self._opener.add_handler(urllib2.ProxyHandler({"http": proxy}))

        self._host = host
        self._timeout = timeout

    def get_rank(self, url):
        """Get the page rank for the specified URL

Keyword arguments:
url -- get page rank for url

"""
        raise NotImplementedError("You must override get_rank()")


class AlexaTrafficRank(RankProvider):
    """ Get the Alexa Traffic Rank for a URL

"""
    def __init__(self, host="xml.alexa.com", proxy=None, timeout=30):
        """Keyword arguments:
host -- toolbar host address: Default: joolbarqueries.google.com
proxy -- address of proxy server (if required). Default: None
timeout -- how long to wait for a response from the server.
Default: 30 (seconds)

"""
        super(AlexaTrafficRank, self).__init__(host, proxy, timeout)

    def get_rank(self, url):
        """Get the page rank for the specified URL

Keyword arguments:
url -- get page rank for url

"""
        query = "http://%s/data?%s" % (self._host, urllib.urlencode((
            ("cli", 10),
            ("dat", "nsa"),
            ("ver", "quirk-searchstatus"),
            ("uid", "20120730094100"),
            ("userip", "192.168.0.1"),
            ("url", url))))

        response = self._opener.open(query, timeout=self._timeout)
        if response.getcode() == httplib.OK:
            data = response.read()

            element = xml.etree.ElementTree.fromstring(data)
            for e in element.iterfind("SD"):
                popularity = e.find("POPULARITY")
                if popularity is not None:
                    return int(popularity.get("TEXT"))


class GooglePageRank(RankProvider):
    """ Get the google page rank figure using the toolbar API.
Credits to the author of the WWW::Google::PageRank CPAN package
as I ported that code to Python.

"""
    def __init__(self, host="toolbarqueries.google.com", proxy=None, timeout=30):
        """Keyword arguments:
host -- toolbar host address: Default: toolbarqueries.google.com
proxy -- address of proxy server (if required). Default: None
timeout -- how long to wait for a response from the server.
Default: 30 (seconds)

"""
        super(GooglePageRank, self).__init__(host, proxy, timeout)
        self._opener.addheaders = [("User-agent", "Mozilla/4.0 (compatible; \
GoogleToolbar 2.0.111-big; Windows XP 5.1)")]

    def get_rank(self, url):
        # calculate the hash which is required as part of the get
        # request sent to the toolbarqueries url.
        ch = '6' + str(self._compute_ch_new("info:%s" % (url)))

        query = "http://%s/tbr?%s" % (self._host, urllib.urlencode((
            ("client", "navclient-auto"),
            ("ch", ch),
            ("ie", "UTF-8"),
            ("oe", "UTF-8"),
            ("features", "Rank"),
            ("q", "info:%s" % (url)))))

        response = self._opener.open(query, timeout=self._timeout)
        if response.getcode() == httplib.OK:
            data = response.read()
            match = re.match("Rank_\d+:\d+:(\d+)", data)
            if match:
                rank = match.group(1)
                return int(rank)

    @classmethod
    def _compute_ch_new(cls, url):
        ch = cls._compute_ch(url)
        ch = ((ch % 0x0d) & 7) | ((ch / 7) << 2);

        return cls._compute_ch(struct.pack("<20L", *(cls._wsub(ch, i * 9) for i in range(20))))

    @classmethod
    def _compute_ch(cls, url):
        url = struct.unpack("%dB" % (len(url)), url)
        a = 0x9e3779b9
        b = 0x9e3779b9
        c = 0xe6359a60
        k = 0

        length = len(url)

        while length >= 12:
            a = cls._wadd(a, url[k+0] | (url[k+1] << 8) | (url[k+2] << 16) | (url[k+3] << 24));
            b = cls._wadd(b, url[k+4] | (url[k+5] << 8) | (url[k+6] << 16) | (url[k+7] << 24));
            c = cls._wadd(c, url[k+8] | (url[k+9] << 8) | (url[k+10] << 16) | (url[k+11] << 24));

            a, b, c = cls._mix(a, b, c)

            k += 12
            length -= 12

        c = cls._wadd(c, len(url));

        if length > 10: c = cls._wadd(c, url[k+10] << 24)
        if length > 9: c = cls._wadd(c, url[k+9] << 16)
        if length > 8: c = cls._wadd(c, url[k+8] << 8)
        if length > 7: b = cls._wadd(b, url[k+7] << 24)
        if length > 6: b = cls._wadd(b, url[k+6] << 16)
        if length > 5: b = cls._wadd(b, url[k+5] << 8)
        if length > 4: b = cls._wadd(b, url[k+4])
        if length > 3: a = cls._wadd(a, url[k+3] << 24)
        if length > 2: a = cls._wadd(a, url[k+2] << 16)
        if length > 1: a = cls._wadd(a, url[k+1] << 8)
        if length > 0: a = cls._wadd(a, url[k])

        a, b, c = cls._mix(a, b, c);

        # integer is always positive
        return c

    @classmethod
    def _mix(cls, a, b, c):
        a = cls._wsub(a, b); a = cls._wsub(a, c); a ^= c >> 13;
        b = cls._wsub(b, c); b = cls._wsub(b, a); b ^= (a << 8) % 4294967296;
        c = cls._wsub(c, a); c = cls._wsub(c, b); c ^= b >>13;
        a = cls._wsub(a, b); a = cls._wsub(a, c); a ^= c >> 12;
        b = cls._wsub(b, c); b = cls._wsub(b, a); b ^= (a << 16) % 4294967296;
        c = cls._wsub(c, a); c = cls._wsub(c, b); c ^= b >> 5;
        a = cls._wsub(a, b); a = cls._wsub(a, c); a ^= c >> 3;
        b = cls._wsub(b, c); b = cls._wsub(b, a); b ^= (a << 10) % 4294967296;
        c = cls._wsub(c, a); c = cls._wsub(c, b); c ^= b >> 15;

        return a, b, c

    @staticmethod
    def _wadd(a, b):
        return (a + b) % 4294967296

    @staticmethod
    def _wsub(a, b):
        return (a - b) % 4294967296

def execution(list1,t_id):
    completed_path="D://Thesis//data//domain_name//page_ranks//stats//completed.txt"
    db = MySQLdb.connect("localhost",user="root",db="web_categorization")
    cursor = db.cursor()
    for element in list1:
        try:
            providers = (AlexaTrafficRank(), GooglePageRank(),)
            print("Traffic stats for: %s" % (element))
            Alextra_treffic_rank= providers[0].get_rank(element)
            google_page_rank= providers[1].get_rank(element)
            print str(Alextra_treffic_rank)
            print str(google_page_rank)
            """process_path= "D://Thesis//data//domain_name//page_ranks//sources_page_ranks.CSV"
            f2=open(process_path,'a+')
            w = csv.writer(f2,delimiter=';')
            w.writerow([element,str(google_page_rank),str(Alextra_treffic_rank)])
            #f2.write(element+' '+rank+'\n')
            f2.close()"""

            sql = ("insert into page_rank(url_name,Alextra_treffic_rank,google_page_rank) values('%s','%s','%s')" %(element,Alextra_treffic_rank,google_page_rank))
            try:
                    cursor.execute(sql)
                    print 'hello'
                    db.commit()
                    print 'processed',element,"  ",t_id
                    f_com=open(completed_path,'a+')
                    f_com.write(element+'\n')
                    f_com.close()

            except:
                    print "error in insertion"
                    db.rollback()

        except:
            check_pa="D://Thesis//data//domain_name//page_ranks//stats//not_available.txt"
            f3=open(check_pa,'a+')
            f3.write(element+'\n')
            f3.close()
            print 'not available',element,"   ",t_id
            pass
        time.sleep(1)

if __name__ == "__main__":

    #path for all the categories which are listed
    input_domain_path="D://Thesis//data//domain_name//main_base_categories_50//"
    all_categories=os.listdir(input_domain_path)
    print len(all_categories)
    all_sources=[]
    for catego in all_categories:
        path1=input_domain_path+catego
        f_local=open(path1,'r')
        sources=f_local.read().split("\n")
        all_sources=all_sources+sources
    print len(all_sources)
    """save_path="D://Thesis//data//domain_name//domains_related_to_category_path//"
    f_path=open(save_path+'domain_latest.txt',"a+")"""
    """for sou in all_sources:
        f_path.write(sou+'\n')"""
    """save_path="D://Thesis//data//domain_name//domains_related_to_category_path//"
    for line in fileinput.input(save_path+'domain_path.TXT'):
        print line"""

    """all_sources=[]
    save_path="D://Thesis//data//domain_name//domains_related_to_category_path//"
    f_sa=open(save_path+'domain_path.TXT','r')
    all_sources=f_sa.read().split("\n")"""

    #currently working on these systems
    """all_sources=[]
    #finding page rank of main category sources
    main_path="D://Thesis//data//domain_name//domains_related_to_category_path//main_category//"
    f_path=open(main_path+'file1.txt','r')
    all_sources=f_path.read().split("\n")
    print len(all_sources)"""

    #sorces page rank

    #input_domain="D://Thesis//data//domain_name//category_gdelt_valid_source//"
    #all_sources=os.listdir(input_domain)


    #sources for which page rank is not available
    check_path="D://Thesis//data//domain_name//page_ranks//stats//not_available.txt"
    f=open(check_path,'r')
    temp_list=f.read().split("\n")
    f.close()

    #sources which have been processed
    process_list=[]
    processed="D://Thesis//data//domain_name//page_ranks//stats//completed.txt"
    try:
        """f1=open(processed,'rb')
        reader1 = csv.reader(f,delimiter='\t')
        t_list=list(reader1)
        for e in t_list:
            process_list.append(t_list[0])"""
        f1=open(processed,'r')
        process_list=f1.read().split("\n")
        f1.close()
    except:
        pass
    e=[]
    domain_list=[]
    for f_name in all_sources:
        #element=x.rstrip('.txt')
        #f_name='http://'+f_name.rstrip('.txt')
        if f_name not in temp_list and f_name not in process_list:
            #f_name='http://'+element.rstrip('.txt')
            e.append(f_name)
    print 'remaining to proceed sources', len(e)
    del temp_list[:]
    del all_sources[:]
    del process_list[:]
    i=0
    while 1:
            if (i+2000)<len(e):
               j=i+2000
               list1=e[i:j]
               domain_list.append(list1)
               i=j
            else:
                j=i+len(e)-1
                list1=e[i:j]
                domain_list.append(list1)
                break
    j=0
    index=1
    for b in domain_list:
        print len(b)
        """save_path="D://Thesis//data//domain_name//domains_related_to_category_path//"
        f_path=open(save_path+"domain_10_sources"+str(index)+".txt","a+")
        for ele in b:
            f_path.write(ele+'\n')
            index=index+1"""

    for element in domain_list:
            id1=j+1
            t=threading.Thread(target=execution, args = (element,id1,))
            j=j+1
            #t.daemon=True
            t.start()