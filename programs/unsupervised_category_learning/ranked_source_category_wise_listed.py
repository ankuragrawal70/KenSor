import os
import twiter_info_access as t
#files processing on other computer
path="D://Thesis//data//domain_name//main_base_categories_50//"
files=os.listdir(path)

#all files including processing on this computer and other computer
path1="D://Thesis//data//domain_name//main_categories//"
file_lists=os.listdir(path1)

#all source ranked to be put in a file so that based on category we could access them
ranked_source_path="D://Thesis//data//domain_name//news_sources_ranking//ranked_based_on_average_articles//"
f=open(ranked_source_path+"mean_more.txt","r")

#sources_info_mean_std contains information about statistics of sources
sources_info_mean_std=f.read().split("\n")
ranked_sources=[]

for sou in sources_info_mean_std:
    sou=sou.split(" ")[0]
    ranked_sources.append(sou)
print "rankes sources are",len(ranked_sources)

#top 200 news sources
top_200_path="D://Thesis//data//domain_name//news_sources_ranking//based_on_4inm_website//top_200_news_sources_world.txt"
f_path=open(top_200_path,"r")
top_200_sources=f_path.read().split("\n")

#file processing on this computer
for i in range(46,len(file_lists)):
    #map to store ranking information which will be sorted in the end
    ranking_info_map={}
    #accessing each category here
    if file_lists[i] not in files:
        print file_lists[i].rstrip(".txt")
        sources_path=path1+file_lists[i]
        f1=open(sources_path,"r")

        #unranked sources is a list of sources not ranked properly
        unranked_sources=f1.read().split("\n")
        print unranked_sources
        print "sources not ranked are",len(unranked_sources)
        for source in unranked_sources:
            try:
                index=ranked_sources.index(source)
                ranking_info_map[source]=index
            except:
                pass
    output_sources_list=sorted(ranking_info_map, key = lambda item: ranking_info_map[item])
    remaining=[]

    #map for twitter info ranking
    twitter_ranking={}
    #finding twitter file in a row
    sources_twitter_info=t.twitter_info()
    for ele in output_sources_list:

        domain="http://"+ele.split("//")[1].split("/")[0]
        #print domain
        for source in sources_twitter_info:

            if source[0]==domain:
                twitter_ranking[ele]=source[2]
        #if domain in top_200_sources:
            #print ele,sources_info_mean_std[ranking_info_map[ele]]
        #else:
        #    remaining.append(ele+" "+sources_info_mean_std[ranking_info_map[ele]])
    print "\n"
    print twitter_ranking
    #for sou in remaining:
    #    print sou

    output=sorted(twitter_ranking, key = lambda item: int(twitter_ranking[item]),reverse=True)

    for ele in output:
        #domain="http://"+ele.split("//")[1].split("/")[0]
        #if domain in top_200_sources:
        print ele,sources_info_mean_std[ranking_info_map[ele]],twitter_ranking[ele]
    break

