from nltk.corpus import wordnet as wn
from nltk import pos_tag
import nltk
syn=wn.synsets('gadget')
print syn
similiar={}
heirarichy={}
lemma_names={}
for e in syn:
    print str(e),e.hyponyms()
    #print "\n"
    print str(e),e.hypernyms()
    print e,e.lemma_names()
    #break
    print "\n"
    #print sorted([lemma.name for e in types_of_car for lemma in e.lemmas])
    #for lemma in e.lemma_names():
    #    print str(lemma)
    #for lemma in e.hypernyms():
     #   print str(lemma)


#print x.sort()
"""jesus=wn.synsets('angry')
god=wn.synsets('furious')
#x='angry'
#y='furious'
print jesus[0].path_similarity(god[2])
#print jesus[0].lch_similarity(god[0])
#print x.path_similarity(y)
print jesus[0].wup_similarity(god[0])
#print wn.synset(jesus[0]).lowest_common_hypernyms(wn.synset(god[0]))"""

#text="Divers retrieved one black box and located the other underwater on Monday from the AirAsia plane that crashed more than two weeks ago"
#text="Black box retrieved from crashed AirAsia Flight"
#t="India using Afghan soil to attack Pakistan"
#tx="64 Indian female workers transferred to shelter in Kuwait"
"""x =nltk.pos_tag(text.split())
y=nltk.pos_tag(t.split())
print nltk.pos_tag(tx.split())
print nltk.ne_chunk(x)"""
#print wn.synsets("workers")[0].path_similarity(wn.synsets("transfer")[0])
#print wn.synsets("workers")[0].lch_similarity(wn.synsets("transfer")[0])

#print wn.synsets("Black box")[0].path_similarity(wn.synsets("crash")[0])
#print wn.synsets("Black box")[0].lch_similarity(wn.synsets("crash")[0])
