import twiter_info_access as social_media

class page_rank:
    def __init__(self,alextra=None,google_page=None,norm_value=None):
        self.alextra_treffic_rank=alextra
        self.google_page_rank=google_page
        self.normalized_alextra=norm_value


global_domain_Score={}
facebook_data={}
twitter_data={}
page_ranks_data={}
alextra_rank_source_information={}

max1=0
facebook_likes=social_media.facebook_like()
for item in facebook_likes:
    #item=item.split(" ")
    if int(item[2])>max1:
        max1=int(item[2])
    try:
        facebook_data[item[0]]=int(item[2])
    except:
        pass
print max1
#print facebook_data
del facebook_likes[:]


max=0
var=""
twitter_folowers=social_media.twitter_info()
for item in twitter_folowers:
    #print item
    #item=item.split(" ")
    if int(item[2])>max:
        max=int(item[2])
        var=item[0]
    try:
        twitter_data[item[0]]=int(item[2])
    except:
        pass
print max
#print var
del twitter_folowers[:]

#pageranks is a list getting all the value of alextra treffic rank and google page rank
page_ranks=social_media.page_rank_info()
for item in page_ranks:
    item=item.split(" ")
    #print item
    #if int(item[1]) not in alextra_rank_source_information:
    #    alextra_rank_source_information[int(item[1])]=alextra_rank_source_information[int(item[1])]+"\n"

    rank_info=page_rank()
    try:
        #print int(item[1])
        rank_info.alextra_treffic_rank=int(item[1])
    except:
         pass
    try:
        rank_info.google_page_rank=int(item[2])
    except:
        pass
    page_ranks_data[item[0]]=rank_info
#del page_ranks[:]

#print page_ranks_data
"""max_alextra=28508631
min=0
score_function={}
for e in page_ranks_data:
    try:
        google=page_ranks_data[e].google_page_rank
        alextra=page_ranks_data[e].alextra_treffic_rank
        #print e,google,alextra
        #print (float(page_ranks_data[e].alextra_treffic_rank)/max_alextra)*10000
        #if google>0 and alextra>=0:

        #alextra treffic is normalized to 10
        normalized_alextra=(float(alextra)/28508631)*10
        #normalized_google=float(google)/10
            #print normalized_alextra
        score_function[e]=google-(normalized_alextra)
        #score_function[e]=google-alextra
            #score_function[e]=(float(alextra)/google)
    except:
        pass
output_sources_list=sorted(score_function, key = lambda item: score_function[item],reverse=True)
score_file_path="D://Thesis//data//domain_name//twitter_information_sources//"
f_score=open(score_file_path+"output_rank_score.txt",'a+')
for e in output_sources_list:
        f_score.write(e+" "+str(page_ranks_data[e].google_page_rank)+" "+str(page_ranks_data[e].alextra_treffic_rank)+" "+str(score_function[e])+"\n")
        print e,page_ranks_data[e].google_page_rank,page_ranks_data[e].alextra_treffic_rank,score_function[e]"""
    #if page_ranks_data[e].alextra_treffic_rank>max_alextra:
    #    max_alextra= page_ranks_data[e].alextra_treffic_rank

#working for facebook likes

fac_file_path="D://Thesis//data//domain_name//twitter_information_sources//"
"""f_book=open(fac_file_path+"normalized_facebook_data.txt","a+")
for element in facebook_data:
    likes=facebook_data[element]
    normalized_value=(float(likes)/80887105)*10
    print element," ",likes," ",normalized_value
    f_book.write(element+" "+str(likes)+" "+str(normalized_value)+"\n")"""


"""f_tweet=open(fac_file_path+"normalized_twitter_follwers.txt","a+")
for ele in twitter_data:
    follower=twitter_data[ele]
    normalized_value=(float(follower)/16288881)*10
    print ele," ",follower," ",normalized_value
    f_tweet.write(ele+" "+str(follower)+" "+str(normalized_value)+"\n")"""


