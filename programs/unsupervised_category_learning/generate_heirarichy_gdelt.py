import os
prev_path='D://Thesis//data//domain_name//gdelt_level_1//'
path='D://Thesis//data//domain_name//gdelt_level_2//'
prev_files=os.listdir(prev_path)
files=os.listdir(path)

path1='D://Thesis//data//domain_name//category_gdelt_valid_source//'
path2='D://Thesis//data//domain_name//not_news_source//name'
for i in range(0,len(files)):
    try:
        result={}
        summary={}
        f_path=path+files[i]
        f=open(f_path,'r')
        x=f.readline()
        summary=eval(f.readline())
        #print summary
        #summary=dict(s)
        #a_dict = dict([summary.strip('{}').split(":"),])
        prev_summary={}
        if files[i] in prev_files:
            prev_f_path=prev_path+files[i]
            f1=open(prev_f_path,'r')
            a=f1.readline()
            prev_summary=eval(f1.readline())        
        if len(prev_summary)>0:
            for e in summary.keys():
                if e in prev_summary:
                    prev_summary[e]=prev_summary[e]+1
                    result[e]=2
                #else:
                #    result[e]=1
            """for e in prev_summary.keys():
                if prev_summary[e]==1:
                    result[e]=1"""
        else:
            if len(summary>0):
                for e in summary.keys():
                    result[e]=1
        if len(summary)==len(prev_summary):
            f=open(path2,'a+')
            f.write(files[i]+'\n')
            f.close()
        else:
            if len(result)>0:
                f1=open((path1+files[i]),'w')
                f1.write(str(result))
                f1.close()
                result.clear()
                print '\n\completed\n',files[i]
                f1.close()
    except:
        print 'EOF exception'
        pass

            
    """for g in summary:
        print g,summary[g]
    print '\n\nnew summary is'
    for z in prev_summary.keys():
        print z,prev_summary[z]"""
    #for key,value in result.items():
        #if value==2:
     #       print key,value         
