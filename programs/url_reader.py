import os
import csv
def csv_reader(file_obj,filename,url):
    print "in csv_reader"
    reader1 = csv.reader(file_obj,delimiter='\t')
    row=list(reader1)
    print "total records are",len(row)
    #row is a set of rows of the given file
    #url is a hash_map that contains the urls and their count 
    for row1 in row:
        x=len(row1)
        domain_name=row1[x-1]
        #print domain_name
        if url.has_key(domain_name):
            url[domain_name]=url[domain_name]+1
        else:
            url[domain_name]=1
    
    print "date",filename
    print "\ttotal unique urls are",len(url)
    #for element in url:
     #   print element,url[element]

if __name__=="__main__":        
    url={}
    #category={}
    #domain={}

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
        csv_reader(f,ac_date,url)
        f.close()
