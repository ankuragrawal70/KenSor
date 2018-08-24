import os
import final_ranking_of_all_sources as ranking
def category_search(category):
    local_ranking={}
    if category+".txt" in categories:
        f=open(c_path+category+".txt","r")
        sources=f.read().split("\n")
        for sou in sources:
            if sou in source_score:
                local_ranking[sou]=source_score[sou]
    if category+".txt" in special_categories:
        f=open(sp_path+category+".txt","r")
        sources=f.read().split("\n")
        for sou in sources:
            if sou in source_score:
                local_ranking[sou]=source_score[sou]

    #local_source_ranking=sorted(local_ranking, key = lambda item: local_ranking[item],reverse=True)
    #return local_source_ranking
    return local_ranking


c_path="D://Thesis//data//domain_name//domains_related_to_a_category_all_10//"
categories=os.listdir(c_path)

sp_path="D://Thesis\data//domain_name//machine_1_special_categories//special_domains_related_to_a_category//special_domains_related_to_a_category//"
special_categories=os.listdir(sp_path)

#source score is a hashmap of score returned by ranking file
source_score=ranking.all_source_ranking()
#print len(source_score)
def find_categories(news_category):
    rank=category_search(news_category)
    #for e in rank:
    #    print e,source_score[e]
    return rank
#vol=find_categories("business")
#source_ranking=sorted(vol, key = lambda item: vol[item].score,reverse=True)
