from nltk.tag.stanford import NERTagger
import nltk
#sample = "Delhi elections 2015: Confident of running Delhi govt for next 5 years, Kejriwal says on TOI Hangout"
sample='she is the widow of former Prime Minister'
sentences = nltk.sent_tokenize(sample)
#print sentences
tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
#print tokenized_sentences
tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
#chunked_sentences = nltk.ne_chunk_sents(tagged_sentences)
print tagged_sentences
"""for e in tagged_sentences:
        namedEnt=nltk.ne_chunk(e,binary=True)
        #print namedEnt
        entity_n = [' '.join([y[0] for y in x.leaves()]) for x in namedEnt.subtrees() if x.label() == "NE"]
        print entity_n"""
"""sen=tagged_sentences[0]
for ele in sen:
    #print ele
    if ele[1][0]=='N'or ele[1][0]=='J':
        print ele[0]"""



"""def extract_entity_names(t):
    entity_names = []
    
    if hasattr(t, 'node') and t.node:
        if t.node == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))
                
    return entity_names
 
entity_names = []
for tree in chunked_sentences:
    # Print results per sentence
    # print extract_entity_names(tree)
    
    entity_names.extend(extract_entity_names(tree))
    print entity_names
 
# Print all entity names
#print entity_names
 
# Print unique entity names
#print set(entity_names)
#print chunked_sentences"""
"""from nltk.corpus import wordnet as wn
wn.hypernyms('gadgets')"""
