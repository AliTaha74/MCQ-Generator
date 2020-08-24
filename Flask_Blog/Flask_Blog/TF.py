import spacy
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic as wn_ic
import random
import copy
from textblob import TextBlob
from textblob import Word
import sys

from Flask_Blog.Flask_Blog import WHQ
from Flask_Blog.Flask_Blog import Distractors

# **************************************************** True , False Question Generation Code ********************************************
def gen_T_F_Question(keyword_dic_sents, dic_dist):
    dicT_F = copy.deepcopy(keyword_dic_sents)
    random_numer = random.randint(0, 2)  # to choose one distractor randomly form 3 distractors

    for i in dicT_F:  # for every key in dic
        old_word = i  # the original keyword
        new_word = dic_dist[i][random_numer]  # randomly choose a distractor
        for x in range(len(dicT_F[i])):
            new_pharse = dicT_F[i][x].replace(old_word, new_word)
            dicT_F[i][x] = [dicT_F[i][x], 'True', new_pharse, 'False']

    return (dicT_F)


# **************************************************** End True , False Question Generation Code ********************************************
def get_TF_and_answers(dicT_F):
    output = []
    for x in dicT_F:
        for sent in dicT_F[x]:
            tq = [sent[0], ["True", "False"], sent[1]]
            output.append(tq)
            fq = [sent[2], ["True", "False"], sent[3]]
            output.append(fq)
    return output

Final_Qestions = []

def Final_Back(dic_ls , str):
    WHQ.content = str
    Final_Qestions = Distractors.WH_Fillgap_Q + dic_ls
    return Final_Qestions

'''def main():
    # print("keyword_dic_NER" ,keyword_dic_NER)
    # print("keyword_dic_sents", keyword_dic_sents)

    print(Distractors.dic_dist)
    dicT_F = gen_T_F_Question(WHQ.keyword_dic_sents, Distractors.dic_dist)
    print(dicT_F)
    TFQ_List = get_TF_and_answers(dicT_F)
    print(" ")
    print("Answer with True Or False :")
    print("__________________________")
    for key in dicT_F:
        for sent in dicT_F[key]:
            print(sent[0])  # 0 gets original sentence , 1 gets "yes" , 2 gets replaceed sentence , 3 gets "false"
            print(sent[2])

    print(" ")
    print("Answers:")
    print("________")
    for key in dicT_F:
        for sent in dicT_F[key]:
            print(sent[1])
            print(sent[3])

    # Printing to File
    # print_file(NL_distractors, test_word)
    Final_Qestions = Distractors.WH_Fillgap_Q + TFQ_List
    print(Final_Qestions)
if __name__ == "__main__":
    main()

'''

