class ranking_parameters:
    def __init__(self,traffic_base,social_m,freshness,score):
        self.traffic_imp=traffic_base
        self.social_media=social_m
        self.ar_freshness=freshness
        self.score=score
#source_article_volume contains global source rank score
def all_source_ranking():
    #source article volume contains final_score
    source_article_volume={}

    #source article rank information
    social_media_path="D://Thesis//data//domain_name//twitter_information_sources//"
    f_path=open(social_media_path+"normalized_facebook_data.txt","r")
    facebook=f_path.read().split("\n")
    #facebook score contains score of facebook data
    facebook_score={}
    for element in facebook:
        score=element.split(" ")
        facebook_score[score[0]]=float(score[2])


    t_path=open(social_media_path+"normalized_twitter_follwers.txt","r")
    twitter=t_path.read().split("\n")
    #twitter score contains combined score of twitter data
    twitter_score={}
    for element in twitter:
        score=element.split(" ")
        twitter_score[score[0]]=float(score[2])

    r_path=open(social_media_path+"output_rank_score.txt","r")
    rank_score=r_path.read().split("\n")
    #treffic rank contains combined ranking of alextra treffic rank and google page rank
    treffic_rank={}
    for element in rank_score:
        score=element.split(" ")
        treffic_rank[score[0]]=float(score[3])

    #machine 1 main rnaking of top categories on sahisnu sir's machine
    source_path="D://Thesis//data//domain_name//machine_1_main_categories//domain_stats/mean_std_dev1.txt"
    f=open(source_path,"r")
    source_volume=f.read().split("\n")
    for source in source_volume:
        scores=source.split(" ")
        #print scores
        try:
            #averga articles in a week is normalized to 20 scale
            average_articles_in_a_week=(float(float(scores[3])*7)/2201)*10
            domain="http://"+source.split("http://")[1].split("/")[0]
            #print domain
            if domain in twitter_score and domain in facebook_score and domain in treffic_rank:
                #final_rank=0.4*(average_articles_in_a_week)+0.1*(facebook_score[domain])+0.1*(twitter_score[domain])+0.4*(treffic_rank[domain])
                final_rank=0.4*(average_articles_in_a_week)+0.2*(twitter_score[domain])+0.4*(treffic_rank[domain])
                social_me=(twitter_score[domain]+facebook_score[domain])/2
                rank_info=ranking_parameters(treffic_rank[domain],social_me,average_articles_in_a_week,final_rank)
                #print final_rank
                #source_article_volume[scores[0]]=final_rank
                source_article_volume[scores[0]]=rank_info
        except:
            pass
    #print len(source_article_volume)
    del source_volume[:]

    #handling of special sources on sahinsu sir's machine
    special_domain_path="D://Thesis//data//domain_name//machine_1_special_categories//"
    f_special=open(special_domain_path+"mean_std_dev1.txt","r")
    source_volume=f_special.read().split("\n")
    for source in source_volume:
        scores=source.split(" ")
        #print scores
        try:
            #averga articles in a week is normalized to 20 scale
            average_articles_in_a_week=(float(float(scores[3])*7)/2201)*10
            domain="http://"+source.split("http://")[1].split("/")[0]
            #print domain
            if domain in twitter_score and domain in facebook_score and domain in treffic_rank:
                #final_rank=0.4*(average_articles_in_a_week)+0.1*(facebook_score[domain])+0.1*(twitter_score[domain])+0.4*(treffic_rank[domain])
                final_rank=0.4*(average_articles_in_a_week)+0.2*(twitter_score[domain])+0.4*(treffic_rank[domain])
                social_me=(twitter_score[domain]+facebook_score[domain])/2
                rank_info=ranking_parameters(treffic_rank[domain],social_me,average_articles_in_a_week,final_rank)
                #print final_rank
                #source_article_volume[scores[0]]=final_rank
                source_article_volume[scores[0]]=rank_info
        except:
            pass
    #print len(source_article_volume)
    del source_volume[:]
    #domain on my machine apart from top 50
    my_machine_path="D://Thesis//data//domain_name//news_sources_ranking//ranked_based_on_average_articles//"
    f_my_machine=open(my_machine_path+"mean_std_dev1.txt","r")
    source_volume=f_my_machine.read().split("\n")
    for source in source_volume:
        scores=source.split(" ")
        #print scores
        try:
            #averga articles in a week is normalized to 20 scale
            average_articles_in_a_week=(float(float(scores[3])*7)/2201)*10
            domain="http://"+source.split("http://")[1].split("/")[0]
            #print domain
            if domain in twitter_score and domain in facebook_score and domain in treffic_rank:
                #final_rank=0.4*(average_articles_in_a_week)+0.1*(facebook_score[domain])+0.1*(twitter_score[domain])+0.4*(treffic_rank[domain])
                final_rank=0.4*(average_articles_in_a_week)+0.2*(twitter_score[domain])+0.4*(treffic_rank[domain])
                social_me=(twitter_score[domain]+facebook_score[domain])/2
                rank_info=ranking_parameters(treffic_rank[domain],social_me,average_articles_in_a_week,final_rank)
                #print final_rank
                #source_article_volume[scores[0]]=final_rank
                source_article_volume[scores[0]]=rank_info
        except:
            pass
    del source_volume[:]
    m1_source_large="D://Thesis//data//domain_name//machine1_large_sources//"
    f_large=open(m1_source_large+"mean_std_dev1.txt","r")
    source_volume=f_large.read().split("\n")
    for source in source_volume:
        scores=source.split(" ")
        #print scores
        try:
            #averga articles in a week is normalized to 20 scale
            average_articles_in_a_week=(float(float(scores[3])*7)/2201)*10
            domain="http://"+source.split("http://")[1].split("/")[0]
            #print domain
            if domain in twitter_score and domain in facebook_score and domain in treffic_rank:
                #final_rank=0.4*(average_articles_in_a_week)+0.1*(facebook_score[domain])+0.1*(twitter_score[domain])+0.4*(treffic_rank[domain])
                final_rank=0.4*(average_articles_in_a_week)+0.2*(twitter_score[domain])+0.4*(treffic_rank[domain])
                social_me=(twitter_score[domain]+facebook_score[domain])/2
                rank_info=ranking_parameters(treffic_rank[domain],social_me,average_articles_in_a_week,final_rank)
                #print final_rank
                #source_article_volume[scores[0]]=final_rank
                source_article_volume[scores[0]]=rank_info
        except:
            pass
    del source_volume[:]


    #print len(source_article_volume)
    abhaby_machine_sources="D://Thesis//data//domain_name//machine2_abhay_sources//"
    f_my_machine=open(abhaby_machine_sources+"mean_std_dev1.txt","r")
    source_volume=f_my_machine.read().split("\n")
    for source in source_volume:
        scores=source.split(" ")
        #print scores
        try:
            #averga articles in a week is normalized to 20 scale
            average_articles_in_a_week=(float(float(scores[3])*7)/2201)*10
            domain="http://"+source.split("http://")[1].split("/")[0]
            #print domain
            #if domain in facebook_score and domain in twitter_score and domain in treffic_rank:
            if domain in twitter_score and domain in facebook_score and domain in treffic_rank:
                #final_rank=0.4*(average_articles_in_a_week)+0.1*(facebook_score[domain])+0.1*(twitter_score[domain])+0.4*(treffic_rank[domain])
                final_rank=0.4*(average_articles_in_a_week)+0.2*(twitter_score[domain])+0.4*(treffic_rank[domain])
                social_me=(twitter_score[domain]+facebook_score[domain])/2
                rank_info=ranking_parameters(treffic_rank[domain],social_me,average_articles_in_a_week,final_rank)
                #print final_rank
                #source_article_volume[scores[0]]=final_rank
                source_article_volume[scores[0]]=rank_info
        except:
            pass
    del source_volume[:]
    #print len(source_article_volume)
    #source ranking file contains sources in sorted way
    #source_ranking=sorted(source_article_volume, key = lambda item: source_article_volume[item],reverse=True)
    #for i in range(0,10000):
    #    if "sports" in source_ranking[i]:
    #        print source_ranking[i],twitter_score[source_ranking[i]],source_article_volume[source_ranking[i]]+0.4
    #it return the map without sorting
    return source_article_volume

    #for i in range(0,1000):
        #if "sports"
        #print ranked_list[i],source_article_volume[ranked_list[i]]
    #for element in output_sources_list:
    #    print element,source_article_volume[element]
#all_source_ranking()