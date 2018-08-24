import csv
def twitter_info():
    file_path="D://Thesis//data//domain_name//twitter_information_sources//twitter_info.csv"
    f=open(file_path,"rb")
    reader1 = csv.reader(f,delimiter=',')
    rows=list(reader1)
    return rows
def page_rank_info():
    file_path="D://Thesis//data//domain_name//twitter_information_sources//page_ranks_stats.txt"
    f=open(file_path,"r")
    #reader1 = csv.reader(f,delimiter=' ')
    rows=f.read().split("\n")
    return rows
def facebook_like():
    file_path="D://Thesis//data//domain_name//twitter_information_sources//facebook_likes.csv"
    f=open(file_path,"rb")
    reader1 = csv.reader(f,delimiter=';')
    rows=list(reader1)
    return rows
