import os
import statistics
import operator
class stats:
    def __init__(self,total_articles_weekly,mean,sdev,score):
        self.total_fresh=total_articles_weekly
        self.mean=mean
        self.stdev=sdev
        self.score=score
#comparisoin files contains urls on different time stamp
comparison=[]

def static_links(comparison_folders):
    all_files=len(comparison)


#path for all the folders of
crawled_folders_path="C://Python27//special//crawler_output//"

#all sources contains all sources available
all_sources=os.listdir(crawled_folders_path)


#source to be checked
path1="C://Python27//special//sources.txt"
f_path=open(path1,"r")
checked_sources=f_path.read().split("\n")

#rank path to store the result
rank_path="C://Python27//special//"
f_rank=open(rank_path+"mean_std_dev1.txt","a+")

global_info_match={}
element_count=0
max_total=0
day=0
for i in range(0,len(checked_sources)):
    compare_sources={}
    #source path contains path to each sources
    #finding actual domain name
    matching_element=""
    try:
        categoty_name=checked_sources[i].split("/")[-1]
        if "http://" in checked_sources[i]:
            matching_element=(checked_sources[i].split("http://")[1]).replace("/","#")
        #print element
        else:
            matching_element=checked_sources[i].replace["/","#"]
        element_count=element_count+1
    except:
        pass
    #print element_count

    if matching_element in all_sources:
        #source_path_file contains all files based on temporal information
        source_path=crawled_folders_path+matching_element
        source_path_files=os.listdir(source_path)
        
        #print source_path_files
        global_count_of_domain=0
        different_count_set=[]

        #total_files=
        #now accessing each file based on different time
        for file1 in source_path_files:
            path1=source_path+"//"+file1
            f=open(path1,"r")
            crawled_urls=f.read().split("\n")
            comparison.append(crawled_urls)
            count=0
            for url in crawled_urls:
                #if categoty_name.lower() in url.lower():
                if url not in compare_sources:
                        compare_sources[url]=1
                        count=count+1
                else:
                        compare_sources[url]=compare_sources[url]+1
            #print "time is",file,"  ",count
            global_count_of_domain=global_count_of_domain+count
            different_count_set.append(count)
       
        try:
            print "total number of times crawled",len(source_path_files)
            total_article=sum(different_count_set[1:])
            if total_article>max_total:
                max_total=total_article
                day=len(source_path_files)
            print "total fresh articles produced are",total_article
            mean=statistics.mean(different_count_set[1:])
            print "average fresh articles produced are",mean
            stdev=statistics.stdev(different_count_set[1:])
            score=mean-stdev
            print "standrad deviation is",stdev
            #if stdev>0:
                #score=mean/stdev
            #else:
            #    score=mean
            f_rank.write(checked_sources[i]+" "+str(len(source_path_files))+" "+str(total_article)+" "+str(mean)+" "+str(stdev)+"\n")
            print score,"\n"
            global_info_match[checked_sources[i]]=stats(total_article,mean,stdev,score)
            
        except:
            pass
    print "maximum articles and days are",max_total,"     ",day 

#x=sorted(global_info_match.iteritems(), key=lambda (k,v): (v,k),reverse=True)
    #x=sorted(global_info_match, key=operator.attrgetter('mean'),reverse=True)
#rank_path="C://Python27//main_base_categories_50//domain_stats//"
#f_rank=open(rank_path+"mean_std_dev.txt","a+")
"""x=sorted(global_info_match, key = lambda item: global_info_match[item].score,reverse=True)
for element in x:
    print element," ",str(global_info_match[element].mean)," ",str(global_info_match[element].stdev)," "+str(global_info_match[element].score)
    f_rank.write(element+" "+str(global_info_match[element].mean)+" "+str(global_info_match[element].stdev)+" "+str(global_info_match[element].score)+"\n")
f_rank.close()
    #print "\n\n"""
"""for i in range(0,len(comparison)):
    for url in comparison[i]:
        if url not in compare_sources:
                compare_sources[url]=1
        else:
            compare_sources[url]=compare_sources[url]+1"""
#for element,var in compare_sources.items():
#    print element,var
