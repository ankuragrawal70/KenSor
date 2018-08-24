import os
def gdelt_source_fetcher():


    gdelt_path='D://Thesis//data//domain_name//category_gdelt_valid_source//'
    file_list=os.listdir(gdelt_path)
    for i in range(1,len(file_list)):
        p=gdelt_path+file_list[i]
        f=open(p,'r')
        c_info=eval(f.read())
        if len(c_info)>0:
            f_name='http://'+file_list[i].rstrip('.txt')
            if f_name not in distribution_name:
                distribution_name[f_name]=1

        f.close()
    gdelt_path='D://Thesis//data//domain_name//gdelt_heuristic_approach_1//'
    file_list=os.listdir(gdelt_path)
    for i in range(0,len(file_list)):
        p=gdelt_path+file_list[i]
        f=open(p,'r')
        category_url=f.read().split('\n')
        f_name='http://'+file_list[i].rstrip('.txt')
        if f_name not  in distribution_name:
            distribution_name[f_name]=1
        i=0

    ranking_path="D://Thesis//data//domain_name//news_sources_ranking//based_on_4inm_website//top_200_news_sources_world.TXT"
    f1=open(ranking_path,'r')
    sources=f1.read().split('\n')
    count=0
    for sou in sources:
        if sou in distribution_name:
            print sou
            count=count+1
    print 'total matched sources are',count

distribution_name={}

gdelt_source_fetcher()
#source_string="\n".join(distribution_name.keys())
#print source_string