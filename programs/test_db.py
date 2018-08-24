import os
import statistics
import operator
class stats:
    def __init__(self,mean,sdev,score):
        self.mean=mean
        self.stdev=sdev
        self.score=score
#comparisoin files contains urls on different time stamp
comparison=[]

def static_links(comparison_folders):
    all_files=len(comparison)


#path for all the folders of
crawled_folders_path="D://Thesis//data//domain_name//main_category_crawler//"

#all sources contains all sources available
all_sources=os.listdir(crawled_folders_path)


#source to be checked
path1="D://Thesis//data//domain_name//domains_related_to_category_path//main_category_50//domain_file.txt"
f_path=open(path1,"r")
checked_sources=f_path.read().split("\n")


global_info_match={}
element_count=0
for i in range(0,len(checked_sources)):
    compare_sources={}
    #source path contains path to each sources
    #finding actual domain name
    matching_element=checked_sources[i].lstrip("http://").replace("/","#")
    #print element
    if matching_element=="www.nytimes.com#pages#magazine":

        element_count=element_count+1
        #print element_count

        if matching_element in all_sources:
            #source_path_file contains all files based on temporal information
            source_path=crawled_folders_path+matching_element
            source_path_files=os.listdir(source_path)
            #print source_path_files
            global_count_of_domain=0
            different_count_set=[]


            #now accessing each file based on different time
            for file in source_path_files:
                path1=source_path+"//"+file
                f=open(path1,"r")
                crawled_urls=f.read().split("\n")
                comparison.append(crawled_urls)
                count=0
                for url in crawled_urls:
                    #print url
                    if url not in compare_sources:
                        compare_sources[url]=1
                        count=count+1
                    else:
                        compare_sources[url]=compare_sources[url]+1
                #print len(compare_sources)
                print "time is",file,"  ",count
                global_count_of_domain=global_count_of_domain+count
                different_count_set.append(count)
            #statisc_links=0
            """for key in compare_sources:
                try:
                    print key,compare_sources[key]
                    if compare_sources[key]==7:
                        statisc_links=static_links+1
                except:
                    pass
            print statisc_links"""
            try:
                mean=statistics.mean(different_count_set[2:])
                #print "average fresh articles produced are",mean
                stdev=statistics.stdev(different_count_set[2:])
                score=mean-stdev
                #print "standrad deviation is",stdev
                #if stdev>0:
                    #score=mean/stdev
                #else:
                #    score=mean
                print score
                global_info_match[checked_sources[i]]=stats(mean,stdev,score)
            except:
                pass

#x=sorted(global_info_match.iteritems(), key=lambda (k,v): (v,k),reverse=True)
    #x=sorted(global_info_match, key=operator.attrgetter('mean'),reverse=True)
rank_path="D://Thesis//data//domain_name//news_sources_ranking//ranked_based_on_average_articles//mean_std_difference.txt"
f_rank=open(rank_path,"a+")
x=sorted(global_info_match, key = lambda item: global_info_match[item].score,reverse=True)
for element in x:
    print element," ",str(global_info_match[element].mean)," ",str(global_info_match[element].stdev)," "+str(global_info_match[element].score)
    #f_rank.write(element+" "+str(global_info_match[element].mean)+" "+str(global_info_match[element].stdev)+" "+str(global_info_match[element].score)+"\n")
f_rank.close()
    #print "\n\n"




"""for i in range(0,len(comparison)):
    for url in comparison[i]:
        if url not in compare_sources:
                compare_sources[url]=1
        else:
            compare_sources[url]=compare_sources[url]+1"""


#for element,var in compare_sources.items():
#    print element,var




