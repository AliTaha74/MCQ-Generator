# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 23:30:54 2020

@author: Mina_Youssef
"""
import spacy
nlp = spacy.load('en_core_web_lg')
from textblob import TextBlob
import nltk
from textblob import Word
import sys
from nltk.stem import WordNetLemmatizer
from nltk import tokenize
from nltk import word_tokenize, pos_tag
import re
import RAKE
import operator
import neuralcoref

############### global var###################
keyword_dic_NER = {}  # de feha el kelma w el NER index 0 w mena haydef l POS index 1
keyword_dic_sents = {}  # de feha kol klma w sents bta3tha
keyword_POS_Dic = {}
fillgap_dic = {}
Rakedic = {}
RemoveRake = []
qustions = []

def keywords_Q_FN(txt):
    keyword_dic_NER = {}  # de feha el kelma w el NER index 0 w mena haydef l POS index 1
    keyword_dic_sents = {}  # de feha kol klma w sents bta3tha
    keyword_POS_Dic = {}
    fillgap_dic = {}
    Rakedic = {}
    RemoveRake = []
    qustions = []
    DictionariesList = []

    output = re.sub('([\n\r\t ]{2,})', ' ', txt)
    txt = TextBlob(output)
    rake_object = RAKE.Rake(RAKE.SmartStopList())
    All_keywords = rake_object.run(output, maxWords=2)
    #####################################
    neuralcoref.add_to_pipe(nlp)
    doc = nlp(output)
    output = doc._.coref_resolved  ############# el text elly m3aya dlw2ty m3mol replacy le kol damer
    doc = nlp(output)
    # Extract keywords
    for word in All_keywords:
        if word[1] >= 4.5:
            Rakedic[word[0]] = ["BLA", "NOUN"]


    for ent in doc.ents:
        keyword_dic_NER[ent.text] = [ent.label_]



    for word in doc:
        keyword_POS_Dic[word.text] = [word.pos_]


    #########################
    for word in Rakedic.keys():
        qustions = []
        for sent in doc.sents:
            tmp_sent = str(sent)
            if word in tmp_sent:
                qustions.append(tmp_sent.replace(word, "........"))
        if qustions != []:
            fillgap_dic[word] = qustions
        else:
            RemoveRake.append(word)
    for word in keyword_dic_NER.keys():
        qustions = []
        sents = []
        for sent in doc.sents:
            tmp_sent = str(sent)
            if word in str(tmp_sent):
                tmpword = " " + word + " "
                sents.append(tmp_sent)
                qustions.append(tmp_sent.replace(tmpword, "........"))
        fillgap_dic[word] = qustions
        keyword_dic_sents[word] = sents

    DictionariesList.append(fillgap_dic)  # index 0
    DictionariesList.append(keyword_dic_sents)  # index 1

    ###################
    for w in RemoveRake:
        Rakedic.pop(w)
    #print(Rakedic)

    DictionariesList.append(Rakedic)  # index 2

    # print(keyword_dic_NER)
    # print(keyword_dic_sents)
    # print(qustions)
    # print(answers)
    for key1 in keyword_dic_NER:
        for key2 in keyword_POS_Dic:
            if key1 == key2:
                keyword_dic_NER[key1].append(keyword_POS_Dic[key2][0])

    DictionariesList.append(keyword_dic_NER)  # index 3
# --------------------------------------####################################----------------------
    return DictionariesList

########################################### LISTS #############################################
#############VBN List############## verb to be
VBN1 = ['NNP', 'VHZ', 'VBN']
VBN2 = ['PRP', 'VHZ', 'VBN']
VBN3 = ['NNPS', 'VHP', 'VBN']
VBN4 = ['PRP', 'VHP', 'VBN']
VBN5 = ['NNP', 'VHD', 'VBN']
VBN6 = ['PRP', 'VHD', 'VBN']
VBN7 = ['NNPS', 'VHD', 'VBN']
#############End VBN List##############

### present continous Lists ###
PRC1 = ['NNP', 'VBZ', 'VBG', 'NN']  # Mina is playing football
PRCIN1 = ['NNP', 'VBG', 'VBZ', 'NN', 'IN', 'NN']  # Mina is playing football in club
PRCDT1 = ['NNP', 'VBG', 'VBZ', 'NN', 'IN', 'DT', 'NN']  # Mina is playing football in the club
PRC2 = ['NNPS', 'VBP', 'VBG', 'NN']  # Ali and Hazem  are playing football
PRCIN2 = ['NNPS', 'VBG', 'VBP', 'NN', 'IN', 'NN']  # Mina and Omar are playing football in club
PRCDT2 = ['NNPS', 'VBG', 'VBP', 'NN', 'IN', 'DT', 'NN']  # Mina and Omar are playing football in the club
PRC3 = ['PRP', 'VBZ', 'VBG', 'NN']  # He is playing football
PRCIN3 = ['PRP', 'VBG', 'VBZ', 'NN', 'IN', 'NN']  # He is playing football in club
PRCDT3 = ['PRP', 'VBG', 'VBZ', 'NN', 'IN', 'DT', 'NN']  # He is playing football in the club
PRC4 = ['PRP', 'VBP', 'VBG', 'NN']  # They are playing football
PRCIN4 = ['PRP', 'VBG', 'VBP', 'NN', 'IN', 'NN']  # They are playing football in club
PRCDT4 = ['PRP', 'VBG', 'VBP', 'NN', 'IN', 'DT', 'NN']  # They are playing football in the club
PRC5 = ['NN', 'VBG', 'VBZ', 'NN']  # cat is making voice
PRCIN5 = ['NN', 'VBG', 'VBZ', 'NN', 'IN', 'NN']  # cat is making voice in room
PRCDT5 = ['NN', 'VBG', 'VBZ', 'NN', 'IN', 'DT', 'NN']  # cat is making voice in the room
PRC6 = ['NNS', 'VBG', 'VBP', 'NN']  # cats are making voice
PRCIN6 = ['NNS', 'VBG', 'VBP', 'NN', 'IN', 'NN']  # cats are making voice in room
PRCDT6 = ['NNS', 'VBG', 'VBP', 'NN', 'IN', 'DT', 'NN']  # cats are making voice in the room
### end present continous Lists ###

### past continous Lists ##
PAC1 = ['NNP', 'VBD', 'VBG', 'NN']  # Mina was playing football
PACIN1 = ['NNP', 'VBG', 'VBD', 'NN', 'IN', 'NN']  # Mina was playing football in club
PACDT1 = ['NNP', 'VBG', 'VBD', 'NN', 'IN', 'DT', 'NN']  # Mina was playing football in the club
PAC2 = ['NNPS', 'VBD', 'VBG', 'NN']  # Ali and Hazem  were playing football
PACIN2 = ['NNPS', 'VBG', 'VBD', 'NN', 'IN', 'NN']  # Mina and Omar were playing football in club
PACDT2 = ['NNPS', 'VBG', 'VBD', 'NN', 'IN', 'DT', 'NN']  # Mina and Omar were playing football in the club
PAC3 = ['PRP', 'VBD', 'VBG', 'NN']  # He was playing football
PACIN3 = ['PRP', 'VBG', 'VBD', 'NN', 'IN', 'NN']  # He was playing football in club
PACDT3 = ['PRP', 'VBG', 'VBD', 'NN', 'IN', 'DT', 'NN']  # He was playing football in the club
PAC4 = ['PRP', 'VBD', 'VBG', 'NN']  # They were playing football
PACIN4 = ['PRP', 'VBG', 'VBD', 'NN', 'IN', 'NN']  # They were playing football in club
PACDT4 = ['PRP', 'VBG', 'VBD', 'NN', 'IN', 'DT', 'NN']  # They were playing football in the club
PAC5 = ['NN', 'VBG', 'VBD', 'NN']  # cat was making voice
PACIN5 = ['NN', 'VBG', 'VBD', 'NN', 'IN', 'NN']  # cat was making voice in room
PACDT5 = ['NN', 'VBG', 'VBD', 'NN', 'IN', 'DT', 'NN']  # cat was making voice in the room
PAC6 = ['NNS', 'VBG', 'VBD', 'NN']  # cats were making voice
PACIN6 = ['NNS', 'VBG', 'VBD', 'NN', 'IN', 'NN']  # cats were making voice in room
PACDT6 = ['NNS', 'VBG', 'VBD', 'NN''IN', 'DT', 'NN']  # cats were making voice in the room

### end past continous Lists ##

########## present simple Lists ############
PRS1 = ['NNP', 'VBZ', 'NN']  # Mina plays football
PRSIN1 = ['NNP', 'VBZ', 'NN', 'IN', 'NN']  # Mina plays football in club ---------------momkn Mina plays club XD:
PRSDT1 = ['NNP', 'VBZ', 'NN', 'IN', 'DT', 'NN']  # Mina plays football in the club
PRS2 = ['PRP', 'VBZ', 'NN']  # He plays football
PRSIN2 = ['PRP', 'VBZ', 'NN', 'IN', 'NN']  # He plays football in club
PRSDT2 = ['PRP', 'VBZ', 'NN', 'IN', 'DT', 'NN']  # He plays football in the club
PRS3 = ['NNPS', 'VBP', 'NN']  # Hazem and Noura play football
PRSIN3 = ['NNPS', 'VBP', 'NN', 'IN', 'NN']  # Hazem and Noura play football in club
PRSDT3 = ['NNPS', 'VBP', 'NN', 'IN', 'DT', 'NN']  # Hazem and Noura play football in the club
PRS4 = ['PRP', 'VBP', 'NN']  # They play football
PRSIN4 = ['PRP', 'VBP', 'NN', 'IN', 'NN']  # They play football in club
PRSDT4 = ['PRP', 'VBP', 'NN', 'IN', 'DT', 'NN']  # They play football in the club
PRS5 = ['NN', 'VBZ', 'NN']  # cat makes voice
PRSIN5 = ['NN', 'VBZ', 'NN', 'IN', 'NN']  # cat makes voice in room
PRSDT5 = ['NN', 'VBZ', 'NN', 'IN', 'DT', 'NN']  # cat makes voice in the room
PRS6 = ['NNS', 'VBP', 'NN']  # cats make voice
PRSIN6 = ['NNS', 'VBP', 'NN', 'IN', 'NN']  # cats make voice in room
PRSDT6 = ['NNS', 'VBP', 'NN', 'IN', 'DT',
          'NN']  # cats make voice in the room --------------------------------------------
PRS7 = ['PRP','VBZ','IN','NNP']    # He lives in Alaska
PRS8 = ['NNP','VBZ','IN','NNP']    # Mina lives in Alaska
PRS9 = ['NNPS','VBZ','IN','NNP']   # Ali and Omar live in Alaska
PRS10 = ['PRP','VBZ','IN','NNP']   # They live in Alaska
########### End present simple Lists #########

########### past simple Lists #################
PAS1 = ['NNP', 'VBD', 'NN']  # Mina played football
PASIN1 = ['NNP', 'VBD', 'NN', 'IN', 'NN']  # Mina played football in club ---------------momkn Mina played club XD:
PASDT1 = ['NNP', 'VBD', 'NN', 'IN', 'DT', 'NN']  # Mina played football in the club
PAS2 = ['PRP', 'VBD', 'NN']  # He played football
PASIN2 = ['PRP', 'VBD', 'NN', 'IN', 'NN']  # He played football in club
PASDT2 = ['PRP', 'VBD', 'NN', 'IN', 'DT', 'NN']  # He played football in the club
PAS3 = ['NNPS', 'VBD', 'NN']  # Hazem and Noura played football
PASIN3 = ['NNPS', 'VBD', 'NN', 'IN', 'NN']  # Hazem and Noura played football in club
PASDT3 = ['NNPS', 'VBD', 'NN', 'IN', 'DT', 'NN']  # Hazem and Noura played football in the club
PAS4 = ['PRP', 'VBD', 'NN']  # They played football
PASIN4 = ['PRP', 'VBD', 'NN', 'IN', 'NN']  # They played football in club
PASDT4 = ['PRP', 'VBD', 'NN', 'IN', 'DT', 'NN']  # They played football in the club
PAS5 = ['NN', 'VBD', 'NN']  # cat made voice
PASIN5 = ['NN', 'VBD', 'NN', 'IN', 'NN']  # cat made voice in room
PASDT5 = ['NN', 'VBD', 'NN', 'IN', 'DT', 'NN']  # cat made voice in the room
PAS6 = ['NNS', 'VBD', 'NN']  # cats made voice
PASIN6 = ['NNS', 'VBD', 'NN', 'IN', 'NN']  # cats made voice in room
PASDT6 = ['NNS', 'VBD', 'NN', 'IN', 'DT', 'NN']  # cats made voice in the room

PAS7 = ['PRP','VBD','IN','NNP']     # He lived in Alaska
PAS8 = ['NNP','VBD','IN','NNP']     # Omar lived in Alaska
PAS9 = ['NNPS','VBD','IN','NNP']     # Mina and Ali lived in Alaska
PAS10 = ['PRP','VBD','IN','NNP']     # They lived in Alaska

##########End past simple Lists ############


########### MD Lists ###########
MD1 = ['MD', 'NNP', 'VB','NN']  # Mina will play football
MDIN1 = ['MD', 'NNP', 'VB','NN','IN','NN']  # Mina will play football in club
MDDT1 = ['MD', 'NNP', 'VB','NN','IN','DT','NN']  # Mina will play football in the club
MD2 = ['MD', 'PRP', 'VB','NN']  # He will play football
MDIN2 = ['MD', 'PRP', 'VB','NN','IN','NN']  # He will play football in club
MDDT2 = ['MD', 'PRP', 'VB','NN','IN','DT','NN']  # He will play football in the club
MD3 = ['MD', 'NNPS', 'VB','NN']  # Mina and Omar will play football
MDIN3 = ['MD', 'NNPS', 'VB','NN','IN','NN']  # Mina and Omar will play football in club
MDDT3 = ['MD', 'NNPS', 'VB','NN','IN','DT','NN']  # Mina and Omar will play football in the club
MD4 = ['MD', 'PRP', 'VB','NN']  # They will play football
MDIN4 = ['MD', 'PRP', 'VB','NN','IN','NN']  # They will play football in club
MDDT4 = ['MD', 'PRP', 'VB','NN','IN','DT','NN']  # They will play football in the club
MD5 = ['MD', 'NN', 'VB', 'NN']  # Machine will produce product ----------------------
MDIN5 = ['MD', 'NN', 'VB', 'NN','IN','NN']  # Machine will produce product in factory
MDDT5 = ['MD', 'NN', 'VB', 'NN','IN','DT','NN']  # Machine will produce product in the factory
MD6 = ['MD', 'NNS', 'VB', 'NN']  # Machines will produce product ---------------------------------
MDIN6 = ['MD', 'NNS', 'VB', 'NN','IN','NN']  # Machines will produce product in factory
MDDT6 = ['MD', 'NNS', 'VB', 'NN','IN','DT','NN']  # Machines will produce product in the factory
############End MD Lists #########

####JJ####
JJ1 = ['NNP', 'VBZ', 'JJ']  # Mina is tall
JJ2 = ['NNPS', 'VBP', 'JJ']  # Mina and Ali are tall
JJ3 = ['PRP', 'VBZ', 'JJ']  # He is tall
JJ4 = ['PRP', 'VBP', 'JJ']  # They are tall
JJ5 = ['NN', 'VBZ', 'JJ']  # Tree is tall
JJ6 = ['NNS', 'VBP', 'JJ']  # Trees are tall
########################################### End LISTS #############################################
# questions = list()
answers = []
keyword_Questions_dic = {}
lemmatizer = WordNetLemmatizer()


def Generate_Questions(keyword_dic_sents, dic_NER):
    try:
        # txt = TextBlob(string)
        # for line in txt.sentences:
        for key in keyword_dic_sents.keys():
            """
               outputs question from the given text
               """
            questions = []
            # print(keyword_dic_sents[line])
            #nlp = spacy.load('en_core_web_lg')
            #doc = nlp(key)

            #for entity in doc.ents:
                # print(entity.text, entity.label_)
            if ((dic_NER[key][0] == "NORP") or (dic_NER[key][0] == "PRODUCT") or (dic_NER[key][0] == "WORK_OF_ART") or (
                    dic_NER[key][0] == "EVENT") or (dic_NER[key][0] == "LAW") or (dic_NER[key][0] == "LANGUAGE")):
                answers.append(key)
                print(key)
                for sentence in keyword_dic_sents[key]:
                    # print(sentence)
                    if type(sentence) is str:  # If the passed variable is of type string.
                        line = TextBlob(sentence)  # Create object of type textblob.blob.TextBlob
                    # print(line)

                    bucket = {}  # Create an empty dictionary

                    for i, j in enumerate(line.tags):  # line.tags are the parts-of-speach in English

                        if j[1] not in bucket:
                            bucket[j[1]] = i  # Add all tags to the dictionary or bucket variable

                    question = ''  # Create an empty string
                    print(line.tags)
                    # With the use of conditional statements the dictionary is compared with the list created above
                    ##################################################################### WHAT ##########################################################################################
                    ######################################## VBN ##################################################
                    if all(key in bucket for key in VBN1):  # 'NNP', 'VBZ'  ,'VBN' in sentence.
                        question = 'What' + ' ' + 'has' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + '?'
                        print('VBN1')
                        questions.append(question)

                    elif all(key in bucket for key in VBN2):  # 'PRP', 'VBZ'  ,'VBN' in sentence.
                        question = 'What' + ' ' + 'has' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + '?'
                        print('VBN2')
                        questions.append(question)

                    elif all(key in bucket for key in VBN3):  # 'NNP', 'VBP'  ,'VBN' in sentence.
                        question = 'What' + ' ' + 'have' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + '?'
                        print('VBN3')
                        questions.append(question)

                    elif all(key in bucket for key in VBN4):  # 'PRP', 'VBP'  ,'VBN' in sentence.

                        question = 'What' + ' ' + 'have' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + '?'
                        print('VBN4')
                        questions.append(question)

                    elif all(key in bucket for key in VBN5):  # 'NNP', 'VBD'  ,'VBN' in sentence.
                        question = 'What' + ' ' + 'had' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + '?'
                        print('VBN5')
                        questions.append(question)

                    elif all(key in bucket for key in VBN6):  # 'PRP', 'VBD'  ,'VBN' in sentence.
                        question = 'What' + ' ' + 'had' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + '?'
                        print('VBN6')
                        questions.append(question)

                    elif all(key in bucket for key in VBN7):  # 'NNPS', 'VBD'  ,'VBN' in sentence.
                        question = 'What' + ' ' + 'had' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + '?'
                        print('VBN7')
                        questions.append(question)

                    ########################################### End Adjective ##################################?????????????????????????!!!!!!!!!!!!!!!!!!'''

                    ########################################### present continouse #############################
                    elif all(key in bucket for key in PRCDT1):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'is' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + \
                                       j[0] + '?'
                            print("PRCDT1")
                            questions.append(question)

                    elif all(key in bucket for key in PRCIN1):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'is' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print("PRCIN1")
                            questions.append(question)

                    elif all(key in bucket for key in PRC1):  # 'NNP', 'VBG', 'VBZ', 'IN' in sentence.
                        question = 'What' + ' ' + 'is' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBG']] + '?'
                        print("PRC1")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'are' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + \
                                       j[0] + '?'
                            print("PRCDT2")
                            questions.append(question)

                    elif all(key in bucket for key in PRCIN2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'are' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print("PRCIN2")
                            questions.append(question)

                    elif all(key in bucket for key in PRC2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        question = 'What' + ' ' + 'are' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBG']] + '?'
                        print("PRC2")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'What' + ' ' + 'is' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                               bucket['DT']] + ' ' + \
                                           j[0] + '?'
                                print("PRCDT3")
                                questions.append(question)

                    elif all(key in bucket for key in PRCIN3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'What' + ' ' + 'is' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                                print("PRCIN3")
                                questions.append(question)

                    elif all(key in bucket for key in PRC3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                            question = 'What' + ' ' + 'is' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + '?'
                            print("PRC3")
                            questions.append(question)
                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'What' + ' ' + 'are' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                               bucket['DT']] + ' ' + \
                                           j[0] + '?'
                                print("PRCDT4")
                                questions.append(question)

                    elif all(key in bucket for key in PRCIN4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'What' + ' ' + 'are' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                                print("PRCIN4")
                                questions.append(question)

                    elif all(key in bucket for key in PRC4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                            question = 'What' + ' ' + 'are' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + '?'
                            print("PRC4")
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT5):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'is' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + \
                                       j[0] + '?'
                            print("PRCDT5")
                            questions.append(question)

                    elif all(key in bucket for key in PRCIN5):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'is' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print("PRCIN5")
                            questions.append(question)

                    elif all(key in bucket for key in PRC5):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        question = 'What' + ' ' + 'is' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBG']] + '?'
                        print("PRC5")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT6):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'are' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + \
                                       j[0] + '?'
                            print("PRCDT6")
                            questions.append(question)

                    elif all(key in bucket for key in PRCIN6):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'are' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print("PRCIN6")
                            questions.append(question)

                    elif all(key in bucket for key in PRC6):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        question = 'What' + ' ' + 'are' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBG']] + '?'
                        print("PRC6")
                        questions.append(question)

                    ########################## Past Cont. ###################################

                    elif all(key in bucket for key in PACDT1):
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'was' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + \
                                       j[0] + '?'
                            print("PACDT1")
                            questions.append(question)

                    elif all(key in bucket for key in PACIN1):
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'was' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print("PACIN1")
                            questions.append(question)

                    elif all(key in bucket for key in PAC1):
                        question = 'What' + ' ' + 'was' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBG']] + '?'
                        print("PAC1")
                        questions.append(question)
                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT2):
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'were' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + \
                                       j[0] + '?'
                            print("PACDT2")
                            questions.append(question)

                    elif all(key in bucket for key in PACIN2):
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'were' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print("PACIN2")
                            questions.append(question)

                    elif all(key in bucket for key in PAC2):
                        question = 'What' + ' ' + 'were' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBG']] + '?'
                        print("PAC2")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT3):
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                question = 'What' + ' ' + 'was' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                               bucket['DT']] + ' ' + \
                                           j[0] + '?'
                                print("PACDT3")
                                questions.append(question)

                    elif all(key in bucket for key in PACIN3):
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                question = 'What' + ' ' + 'was' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                                print("PACIN3")
                                questions.append(question)

                    elif all(key in bucket for key in PAC3):
                        if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                            question = 'What' + ' ' + 'was' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + '?'
                            print("PAC3")
                            questions.append(question)
                            # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT4):
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                question = 'What' + ' ' + 'were' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                               bucket['DT']] + ' ' + \
                                           j[0] + '?'
                                print("PACDT4")
                                questions.append(question)

                    elif all(key in bucket for key in PACIN4):
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                question = 'What' + ' ' + 'were' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                                print("PACIN4")
                                questions.append(question)

                    elif all(key in bucket for key in PAC4):
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                            question = 'What' + ' ' + 'were' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + '?'
                            print("PAC4")
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT5):
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'was' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + \
                                       j[0] + '?'
                            print("PACDT5")
                            questions.append(question)

                    elif all(key in bucket for key in PACIN5):
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'was' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print("PACIN5")
                            questions.append(question)

                    elif all(key in bucket for key in PAC5):
                        question = 'What' + ' ' + 'was' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBG']] + '?'
                        print("PAC5")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT6):
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'were' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + \
                                       j[0] + '?'
                            print("PACDT6")
                            questions.append(question)

                    elif all(key in bucket for key in PACIN6):
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'were' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print("PACIN6")
                            questions.append(question)

                    elif all(key in bucket for key in PAC6):
                        question = 'What' + ' ' + 'were' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBG']] + '?'
                        print("PAC6")
                        questions.append(question)

                    ############################## Present Simple ######################################
                    elif all(key in bucket for key in PRSDT1):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'does' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + j[0] + '?'
                            print('PRSDT1')
                            questions.append(question)

                    elif all(key in bucket for key in PRSIN1):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'does' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print('PRSIN1')
                            questions.append(question)

                    elif all(key in bucket for key in PRS1):  # 'NNP', 'VBZ', 'NN' in sentence
                        question = 'What' + ' ' + 'does' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + ' ' + '?'
                        print('PRS1')
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'What' + ' does ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBZ']].singularize() + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                               bucket['DT']] + ' ' + j[0] + '?'
                                print('PRSDT2')
                                questions.append(question)

                    elif all(key in bucket for key in PRSIN2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'What' + ' does ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBZ']].singularize() + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                                print('PRSIN2')
                                questions.append(question)

                    elif all(key in bucket for key in PRS2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                            question = 'What' + ' does ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + '?'
                            print('PRS2')
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT3):  # 'NNPS', 'VBP', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'do' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBP']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + \
                                       j[0] + '?'
                            print('PRSDT3')
                            questions.append(question)

                    elif all(key in bucket for key in PRSIN3):  # 'NNPS', 'VBP', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + 'do' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBP']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print('PRSIN3')
                            questions.append(question)

                    elif all(key in bucket for key in PRS3):  # 'NNPS', 'VBP', 'NN' in sentence
                        question = 'What' + ' ' + 'do' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBP']] + ' ' + '?'
                        print('PRS3')
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'What' + ' do ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBP']] + ' ' + \
                                           line.words[bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                                print('PRSDT4')
                                questions.append(question)

                    elif all(key in bucket for key in PRSIN4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'What' + ' do ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBP']] + ' ' + \
                                           line.words[bucket['IN']] + ' ' + j[0] + '?'
                                print('PRSIN4')
                                questions.append(question)

                    elif all(key in bucket for key in PRS4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                            question = 'What' + ' do ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBP']] + '?'
                            print('PRS4')
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT5):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' does ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + j[0] + '?'
                            print('PRSDT5')
                            questions.append(question)

                    elif all(key in bucket for key in PRSIN5):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' does ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print('PRSIN5')
                            questions.append(question)

                    elif all(key in bucket for key in PRS5):  # 'NNP', 'VBZ' in sentence.
                        question = 'What' + ' does ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + '?'
                        print('PRS5')
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT6):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' do ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBP']] + ' ' + \
                                       line.words[bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                            print('PRSDT6')
                            questions.append(question)

                    elif all(key in bucket for key in PRSIN6):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' do ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBP']] + ' ' + \
                                       line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print('PRSIN6')
                            questions.append(question)

                    elif all(key in bucket for key in PRS6):  # 'NNP', 'VBZ' in sentence.
                        question = 'What' + ' do ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBP']] + '?'
                        print('PRS6')
                        questions.append(question)

                        ########################################### End present simple #################################


                    ##################################################### MD ###########################################
                    elif all(key in bucket for key in MDDT1):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNP']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + line.words[bucket['NN']] + ' ' +'?'
                            print('MDDT1')
                            questions.append(question)

                    elif all(key in bucket for key in MDIN1):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNP']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[bucket['NN']] + ' ' +'?'
                            print('MDIN1')
                            questions.append(question)

                    elif all(key in bucket for key in MD1):  # 'NNP', 'VB' in sentence.
                        question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNP']] + ' ' + \
                                   line.words[
                                       bucket['VB']] + ' ' + '?'
                        print('MD1')
                        questions.append(question)

                    elif all(key in bucket for key in MDDT2):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                           line.words[bucket['DT']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('MDDT2')
                                questions.append(question)

                    elif all(key in bucket for key in MDIN2):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                           line.words[bucket['NN']] + ' ' + '?'
                                print('MDIN2')
                                questions.append(question)

                    elif all(key in bucket for key in MD2):  # 'PRP', 'VB' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                            question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                bucket['PRP']] + ' ' + line.words[
                                           bucket['VB']]+ ' ' + '?'
                            print('MD2')
                            questions.append(question)

                    elif all(key in bucket for key in MDDT3):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNPS']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                       line.words[bucket['DT']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('MDDT3')
                            questions.append(question)

                    elif all(key in bucket for key in MDIN3):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNPS']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                       line.words[bucket['NN']] + ' ' + '?'
                            print('MDIN3')
                            questions.append(question)

                    elif all(key in bucket for key in MD3):  # 'NNPS', 'VB' in sentence.
                        question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                            bucket['NNPS']] + ' ' + line.words[
                                       bucket['VB']] + ' ' + '?'
                        print('MD3')
                        questions.append(question)

                    elif all(key in bucket for key in MDDT4):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                           line.words[bucket['DT']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('MDDT4')
                                questions.append(question)

                    elif all(key in bucket for key in MDIN4):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                           line.words[bucket['NN']] + ' ' + '?'
                                print('MDIN4')
                                questions.append(question)

                    elif all(key in bucket for key in MD4):  # 'NNS', 'VB' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                            question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                bucket['PRP']] + ' ' + line.words[
                                           bucket['VB']] + ' ' + '?'
                            print('MD4')
                            questions.append(question)

                    elif all(key in bucket for key in MDDT5):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NN']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                       line.words[bucket['DT']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('MDDT5')
                            questions.append(question)

                    elif all(key in bucket for key in MDIN5):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NN']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                       line.words[bucket['NN']] + ' ' + '?'
                            print('MDIN5')
                            questions.append(question)

                    elif all(key in bucket for key in MD5):  # 'NNP', 'VB' in sentence.
                        question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NN']] + ' ' + \
                                   line.words[
                                       bucket['VB']] + ' ' + '?'
                        print('MD5')
                        questions.append(question)

                    elif all(key in bucket for key in MDDT6):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNS']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                       line.words[bucket['DT']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('MDDT6')
                            questions.append(question)

                    elif all(key in bucket for key in MDIN6):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNS']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                       line.words[bucket['NN']] + ' ' + '?'
                            print('MDIN6')
                            questions.append(question)

                    elif all(key in bucket for key in MD6):  # 'NNP', 'VB' in sentence.
                        question = 'What' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNS']] + ' ' + \
                                   line.words[
                                       bucket['VB']] + ' ' + '?'
                        print('MD6')
                        questions.append(question)
                        ####################################### End MD ###############################################
                    ###################################### JJ ####################################################
                    elif all(key in bucket for key in JJ1):  # 'NNP', 'VB' in sentence.
                        question = 'What' + ' ' + 'is' + ' ' + line.words[bucket['NNP']] + ' ' + '?'
                        print('JJ1')
                        questions.append(question)

                    elif all(key in bucket for key in JJ2):  # 'PRP', 'VB' in sentence.
                        question = 'What' + ' ' + 'are' + ' ' + line.words[bucket['NNPS']] + ' ' + '?'
                        print('JJ2')
                        questions.append(question)

                    elif all(key in bucket for key in JJ3):  # 'NNPS', 'VB' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                            question = 'What' + ' ' + 'is' + ' ' + line.words[bucket['PRP']] + ' ' + '?'
                            print('JJ3')
                            questions.append(question)

                    elif all(key in bucket for key in JJ4):  # 'NNPS', 'VB' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                            question = 'What' + ' ' + 'are' + ' ' + line.words[bucket['PRP']] + ' ' + '?'
                            print('JJ4')
                            questions.append(question)

                    elif all(key in bucket for key in JJ5):  # 'NNS', 'VB' in sentence.
                        question = 'What' + ' ' + 'is' + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('JJ5')
                        questions.append(question)

                    elif all(key in bucket for key in JJ6):  # 'NNS', 'VB' in sentence.
                        question = 'What' + ' ' + 'are' + ' ' + line.words[bucket['NNS']] + ' ' + '?'
                        print('JJ6')
                        questions.append(question)
                    ####################################### END JJ ###########################################################

                    ########################################### Past simple #################################
                    try:
                        if all(key in bucket for key in PASDT1):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'What' + ' did ' + line.words[
                                    bucket['NNP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['IN']] + ' ' + \
                                           line.words[bucket['DT']] + ' ' + j[0] + '?'
                                print('PASDT1')
                                questions.append(question)

                        elif all(key in bucket for key in PASIN1):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'What' + ' did ' + line.words[
                                    bucket['NNP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['IN']] + ' ' + \
                                           j[0] + '?'
                                print('PASIN1')
                                questions.append(question)

                        elif all(key in bucket for key in PAS1):  # 'NNP', 'VBZ' in sentence.
                            question = 'What' + ' did ' + line.words[bucket['NNP']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + '?'
                            print('PAS1')
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT2):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                    question = 'What' + ' did ' + line.words[
                                        bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                        line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['IN']] + ' ' + \
                                               line.words[bucket['DT']] + ' ' + j[0] + '?'
                                    print('PASDT2')
                                    questions.append(question)

                        elif all(key in bucket for key in PASIN2):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                    question = 'What' + ' did ' + line.words[
                                        bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                        line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['IN']] + ' ' + \
                                               j[0] + '?'
                                    print('PASIN2')
                                    questions.append(question)

                        elif all(key in bucket for key in PAS2):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                question = 'What' + ' did ' + line.words[
                                    bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + '?'
                                print('PAS2')
                                questions.append(question)
                                # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT3):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'What' + ' did ' + line.words[
                                    bucket['NNPS']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['IN']] + ' ' + \
                                           line.words[bucket['DT']] + ' ' + j[0] + '?'
                                print('PASDT3')
                                questions.append(question)

                        elif all(key in bucket for key in PASIN3):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'What' + ' did ' + line.words[
                                    bucket['NNPS']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['IN']] + ' ' + \
                                           j[0] + '?'
                                print('PASIN3')
                                questions.append(question)

                        elif all(key in bucket for key in PAS3):  # 'NNP', 'VBZ' in sentence.
                            question = 'What' + ' did ' + line.words[bucket['NNPS']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + '?'
                            print('PAS3')
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT4):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                    question = 'What' + ' did ' + line.words[
                                        bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                        line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['IN']] + ' ' + \
                                               line.words[bucket['DT']] + ' ' + j[0] + '?'
                                    print('PASDT4')
                                    questions.append(question)

                        elif all(key in bucket for key in PASIN4):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                    question = 'What' + ' did ' + line.words[
                                        bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                        line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['IN']] + ' ' + \
                                               j[0] + '?'
                                    print('PASIN4')
                                    questions.append(question)

                        elif all(key in bucket for key in PAS4):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                question = 'What' + ' did ' + line.words[
                                    bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + '?'
                                print('PAS4')
                                questions.append(question)

                                # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT5):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'What' + ' did ' + line.words[bucket['NN']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['IN']] + ' ' + \
                                           line.words[bucket['DT']] + ' ' + j[0] + '?'
                                print('PASDT5')
                                questions.append(question)

                        elif all(key in bucket for key in PASIN5):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'What' + ' did ' + line.words[bucket['NN']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['IN']] + ' ' + \
                                           j[0] + '?'
                                print('PASIN5')
                                questions.append(question)

                        elif all(key in bucket for key in PAS5):  # 'NNP', 'VBZ' in sentence.
                            question = 'What' + ' did ' + line.words[bucket['NN']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + '?'
                            print('PAS5')
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT6):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'What' + ' did ' + line.words[
                                    bucket['NNS']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['IN']] + ' ' + \
                                           line.words[bucket['DT']] + ' ' + j[0] + '?'
                                print('PASDT6')
                                questions.append(question)

                        elif all(key in bucket for key in PASIN6):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'What' + ' did ' + line.words[
                                    bucket['NNS']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['IN']] + ' ' + \
                                           j[0] + '?'
                                print('PASIN6')
                                questions.append(question)

                        elif all(key in bucket for key in PAS6):  # 'NNP', 'VBZ' in sentence.
                            question = 'What' + ' did ' + line.words[bucket['NNS']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + '?'
                            print('PAS6')
                            questions.append(question)

                    except:
                        print(" ")
                    ############################################### End past simple #####################################
                    # When the tags are generated 's is split to ' and s. To overcome this issue.
                    if 'VBZ' in bucket and line.words[bucket['VBZ']] == "’":
                        question = question.replace(" ’ ", "'s ")

                    # Print the genetated questions as output.
                    if question != '':
                        print('\n', 'Question: ' + question, '\n\n')

            ################################### WHO ######################################################
            if (dic_NER[key][0] == "PERSON"):
                answers.append(key)
                print(key)
                for sentence in keyword_dic_sents[key]:
                    # print(sentence)
                    if type(sentence) is str:  # If the passed variable is of type string.
                        line = TextBlob(sentence)  # Create object of type textblob.blob.TextBlob
                        print(line)
                    bucket = {}  # Create an empty dictionary

                    for i, j in enumerate(line.tags):  # line.tags are the parts-of-speach in English
                        if j[1] not in bucket:
                            bucket[j[1]] = i  # Add all tags to the dictionary or bucket variable
                            print(bucket[j[1]])

                    question = ''  # Create an empty string

                    # With the use of conditional statements the dictionary is compared with the list created above
                    print(line.tags)
                    ##################################################################### WHO ##########################################################################################
                    ######################################## VBN ##################################################
                    if all(key in bucket for key in VBN1):  # 'NNP', 'VBZ'  ,'VBN' in sentence.
                        question = 'Who' + ' ' + 'has' + ' ' + line.words[bucket['NNP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + '?'
                        print('VBN1')
                        questions.append(question)

                    elif all(key in bucket for key in VBN2):  # 'PRP', 'VBZ'  ,'VBN' in sentence.
                        question = 'Who' + ' ' + 'has' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + '?'
                        print('VBN2')
                        questions.append(question)

                    elif all(key in bucket for key in VBN3):  # 'NNP', 'VBP'  ,'VBN' in sentence.
                        question = 'Who' + ' ' + 'have' + ' ' + line.words[bucket['NNPS']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + '?'
                        print('VBN3')
                        questions.append(question)

                    elif all(key in bucket for key in VBN4):  # 'PRP', 'VBP'  ,'VBN' in sentence.

                        question = 'Who' + ' ' + 'have' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + '?'
                        print('VBN4')
                        questions.append(question)

                    elif all(key in bucket for key in VBN5):  # 'NNP', 'VBD'  ,'VBN' in sentence.
                        question = 'Who' + ' ' + 'had' + ' ' + line.words[bucket['NNP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + '?'
                        print('VBN5')
                        questions.append(question)

                    elif all(key in bucket for key in VBN6):  # 'PRP', 'VBD'  ,'VBN' in sentence.
                        question = 'Who' + ' ' + 'had' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + '?'
                        print('VBN6')
                        questions.append(question)

                    elif all(key in bucket for key in VBN7):  # 'NNPS', 'VBD'  ,'VBN' in sentence.
                        question = 'Who' + ' ' + 'had' + ' ' + line.words[bucket['NNPS']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + '?'
                        print('VBN7')
                        questions.append(question)

                    ########################################### End Adjective ##################################?????????????????????????!!!!!!!!!!!!!!!!!!'''
                    ########################################### present continouse #############################
                    elif all(key in bucket for key in PRCDT1):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + 'is' + ' ' + line.words[bucket['VBG']] + ' ' + \
                                       line.words[
                                           bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + \
                                       j[0] + '?'
                            print("PRCDT1")
                            questions.append(question)

                    elif all(key in bucket for key in PRCIN1):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + 'is' + ' ' + line.words[bucket['VBG']] + ' ' + \
                                       line.words[
                                           bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print("PRCIN1")
                            questions.append(question)

                    elif all(key in bucket for key in PRC1):  # 'NNP', 'VBG', 'VBZ', 'IN' in sentence.
                        question = 'Who' + ' ' + 'is' + ' ' + line.words[bucket['VBG']] + ' ' + \
                                   line.words[
                                       bucket['NN']] + '?'
                        print("PRC1")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + 'are' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + \
                                       j[0] + '?'
                            print("PRCDT2")
                            questions.append(question)

                    elif all(key in bucket for key in PRCIN2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + 'are' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print("PRCIN2")
                            questions.append(question)

                    elif all(key in bucket for key in PRC2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        question = 'Who' + ' ' + 'are' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                            bucket['NN']] + '?'
                        print("PRC2")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'Who' + ' ' + 'is' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                    bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                               bucket['DT']] + ' ' + \
                                           j[0] + '?'
                                print("PRCDT3")
                                questions.append(question)

                    elif all(key in bucket for key in PRCIN3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'Who' + ' ' + 'is' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                    bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                                print("PRCIN3")
                                questions.append(question)

                    elif all(key in bucket for key in PRC3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                            question = 'Who' + ' ' + 'is' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                bucket['NN']] + '?'
                            print("PRC3")
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'Who' + ' ' + 'are' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                    bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                               bucket['DT']] + ' ' + \
                                           j[0] + '?'
                                print("PRCDT4")
                                questions.append(question)

                    elif all(key in bucket for key in PRCIN4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'Who' + ' ' + 'are' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                    bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                                print("PRCIN4")
                                questions.append(question)

                    elif all(key in bucket for key in PRC4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                            question = 'Who' + ' ' + 'are' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                bucket['NN']] + '?'
                            print("PRC4")
                            questions.append(question)

                    ########################## Past Cont. ###################################

                    elif all(key in bucket for key in PACDT1):
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + 'was' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + \
                                       j[0] + '?'
                            print("PACDT1")
                            questions.append(question)

                    elif all(key in bucket for key in PACIN1):
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + 'was' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print("PACIN1")
                            questions.append(question)

                    elif all(key in bucket for key in PAC1):
                        question = 'Who' + ' ' + 'was' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                            bucket['NN']] + '?'
                        print("PAC1")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT2):
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + 'were' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                           bucket['DT']] + ' ' + \
                                       j[0] + '?'
                            print("PACDT2")
                            questions.append(question)

                    elif all(key in bucket for key in PACIN2):
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + 'were' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print("PACIN2")
                            questions.append(question)

                    elif all(key in bucket for key in PAC2):
                        question = 'Who' + ' ' + 'were' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                            bucket['NN']] + '?'
                        print("PAC2")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT3):
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                question = 'Who' + ' ' + 'was' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                    bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                               bucket['DT']] + ' ' + \
                                           j[0] + '?'
                                print("PACDT3")
                                questions.append(question)

                    elif all(key in bucket for key in PACIN3):
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                question = 'Who' + ' ' + 'was' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                    bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                                print("PACIN3")
                                questions.append(question)


                    elif all(key in bucket for key in PAC3):
                        if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                            question = 'Who' + ' ' + 'was' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                bucket['NN']] + '?'
                            print("PAC3")
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT4):
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                question = 'Who' + ' ' + 'were' + ' ' + line.words[bucket['VBG']] + ' ' + \
                                           line.words[
                                               bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                               bucket['DT']] + ' ' + \
                                           j[0] + '?'
                                print("PACDT4")
                                questions.append(question)

                    elif all(key in bucket for key in PACIN4):
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                question = 'Who' + ' ' + 'were' + ' ' + line.words[bucket['VBG']] + ' ' + \
                                           line.words[
                                               bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                                print("PACIN4")
                                questions.append(question)

                    elif all(key in bucket for key in PAC4):
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                            question = 'Who' + ' ' + 'were' + ' ' + line.words[bucket['VBG']] + ' ' + line.words[
                                bucket['NN']] + '?'
                            print("PAC4")
                            questions.append(question)

                    ############################## Present Simple ######################################
                    elif all(key in bucket for key in PRSDT1):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[
                                bucket['NN']] + ' ' + \
                                       line.words[bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                            print('PRSDT1')
                            questions.append(question)

                    elif all(key in bucket for key in PRSIN1):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[
                                bucket['NN']] + ' ' + \
                                       line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print('PRSIN1')
                            questions.append(question)

                    elif all(key in bucket for key in PRS1):  # 'NNP', 'VBZ', 'NN' in sentence
                        question = 'Who' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NN']] + '?'
                        print('PRS1')
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'Who' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[
                                    bucket['NN']] + ' ' + \
                                           line.words[bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                                print('PRSDT2')
                                questions.append(question)

                    elif all(key in bucket for key in PRSIN2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'Who' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[
                                    bucket['NN']] + ' ' + \
                                           line.words[bucket['IN']] + ' ' + j[0] + '?'
                                print('PRSIN2')
                                questions.append(question)

                    elif all(key in bucket for key in PRS2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                            question = 'Who' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NN']] + '?'
                            print('PRS2')
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT3):  # 'NNPS', 'VBP', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + line.words[bucket['VBP']] + ' ' + line.words[
                                bucket['NN']] + ' ' + \
                                       line.words[bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                            print('PRSDT3')
                            questions.append(question)

                    elif all(key in bucket for key in PRSIN3):  # 'NNPS', 'VBP', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + line.words[bucket['VBP']] + ' ' + line.words[
                                bucket['NN']] + ' ' + \
                                       line.words[bucket['IN']] + ' ' + j[0] + '?'
                            print('PRSIN3')
                            questions.append(question)

                    elif all(key in bucket for key in PRS3):  # 'NNPS', 'VBP', 'NN' in sentence
                        question = 'Who' + ' ' + line.words[bucket['VBP']] + ' ' + line.words[bucket['NN']] + '?'
                        print('PRS3')
                        questions.append(question)
                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'Who' + ' ' + line.words[bucket['VBP']] + ' ' + line.words[
                                    bucket['NN']] + ' ' + \
                                           line.words[bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                                print('PRSDT4')
                                questions.append(question)

                    elif all(key in bucket for key in PRSIN4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'Who' + ' ' + line.words[bucket['VBP']] + ' ' + line.words[
                                    bucket['NN']] + ' ' + \
                                           line.words[bucket['IN']] + ' ' + j[0] + '?'
                                print('PRSIN4')
                                questions.append(question)

                    elif all(key in bucket for key in PRS4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                            question = 'Who' + ' ' + line.words[bucket['VBP']] + ' ' + line.words[bucket['NN']] + '?'
                            print('PRS4')
                            questions.append(question)

                    ########################################### End present simple #################################

                    ##################################################### MD ###########################################
                    elif all(key in bucket for key in MDDT1):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + line.words[bucket['MD']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + line.words[bucket['NN']] + ' ' +'?'
                            print('MDDT1')
                            questions.append(question)

                    elif all(key in bucket for key in MDIN1):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + line.words[bucket['MD']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[bucket['NN']] + ' ' +'?'
                            print('MDIN1')
                            questions.append(question)

                    elif all(key in bucket for key in MD1):  # 'NNP', 'VB' in sentence.
                        question = 'Who' + ' ' + line.words[bucket['MD']] + ' '  + \
                                   line.words[
                                       bucket['VB']] + ' ' + '?'
                        print('MD1')
                        questions.append(question)

                    elif all(key in bucket for key in MDDT2):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'Who' + ' ' + line.words[bucket['MD']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                           line.words[bucket['DT']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('MDDT2')
                                questions.append(question)

                    elif all(key in bucket for key in MDIN2):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'Who' + ' ' + line.words[bucket['MD']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                           line.words[bucket['NN']] + ' ' + '?'
                                print('MDIN2')
                                questions.append(question)

                    elif all(key in bucket for key in MD2):  # 'PRP', 'VB' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                            question = 'Who' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                           bucket['VB']]+ ' ' + '?'
                            print('MD2')
                            questions.append(question)

                    elif all(key in bucket for key in MDDT3):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + line.words[bucket['MD']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                       line.words[bucket['DT']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('MDDT3')
                            questions.append(question)

                    elif all(key in bucket for key in MDIN3):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Who' + ' ' + line.words[bucket['MD']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                       line.words[bucket['NN']] + ' ' + '?'
                            print('MDIN3')
                            questions.append(question)

                    elif all(key in bucket for key in MD3):  # 'NNPS', 'VB' in sentence.
                        question = 'Who' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                       bucket['VB']] + ' ' + '?'
                        print('MD3')
                        questions.append(question)

                    elif all(key in bucket for key in MDDT4):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                question = 'Who' + ' ' + line.words[bucket['MD']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                           line.words[bucket['DT']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('MDDT4')
                                questions.append(question)

                    elif all(key in bucket for key in MDIN4):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                question = 'Who' + ' ' + line.words[bucket['MD']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                           line.words[bucket['NN']] + ' ' + '?'
                                print('MDIN4')
                                questions.append(question)

                    elif all(key in bucket for key in MD4):  # 'NNS', 'VB' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                            question = 'Who' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                           bucket['VB']] + ' ' + '?'
                            print('MD4')
                            questions.append(question)


                    ####################################### End MD ###############################################
                    ###################################### JJ ####################################################
                    elif all(key in bucket for key in JJ1):  # 'NNP', 'VB' in sentence.
                        question = 'Who' + ' ' + 'is' + ' ' + line.words[bucket['JJ']] + ' ' + '?'
                        print('JJ1')
                        questions.append(question)

                    elif all(key in bucket for key in JJ2):  # 'PRP', 'VB' in sentence.
                        question = 'Who' + ' ' + 'are' + ' ' + line.words[bucket['JJ']] + ' ' + '?'
                        print('JJ2')
                        questions.append(question)

                    elif all(key in bucket for key in JJ3):  # 'NNPS', 'VB' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                            question = 'Who' + ' ' + 'is' + ' ' + line.words[bucket['JJ']] + ' ' + '?'
                            print('JJ3')
                            questions.append(question)

                    elif all(key in bucket for key in JJ4):  # 'NNPS', 'VB' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                            question = 'Who' + ' ' + 'are' + ' ' + line.words[bucket['JJ']] + ' ' + '?'
                            print('JJ4')
                            questions.append(question)

                    ####################################### END JJ ###########################################################
                    ########################################### Past simple #################################
                    try:
                        if all(key in bucket for key in PASDT1):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'Who' + ' ' + line.words[bucket['VBD']] + ' ' + line.words[
                                    bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                               bucket['DT']] + ' ' + j[0] + '?'
                                print('PASDT1')
                                questions.append(question)

                        elif all(key in bucket for key in PASIN1):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'Who' + ' ' + line.words[bucket['VBD']] + ' ' + line.words[
                                    bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                                print('PASIN1')
                                questions.append(question)

                        elif all(key in bucket for key in PAS1):  # 'NNP', 'VBZ' in sentence.
                            question = 'Who' + ' ' + line.words[bucket['VBD']] + ' ' + line.words[
                                bucket['NN']] + '?'
                            print('PAS1')
                            questions.append(question)
                            # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT2):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                    question = 'Who' + ' ' + line.words[bucket['VBD']] + ' ' + line.words[
                                        bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                                   bucket['DT']] + ' ' + j[0] + '?'
                                    print('PASDT2')
                                    questions.append(question)

                        elif all(key in bucket for key in PASIN2):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                    question = 'Who' + ' ' + line.words[bucket['VBD']] + ' ' + line.words[
                                        bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                                    print('PASIN2')
                                    questions.append(question)

                        elif all(key in bucket for key in PAS2):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                question = 'Who' + ' ' + line.words[bucket['VBD']] + ' ' + line.words[
                                    bucket['NN']] + '?'
                                print('PAS2')
                                questions.append(question)
                                # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT3):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'Who' + ' ' + line.words[bucket['VBD']] + ' ' + line.words[
                                    bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                               bucket['DT']] + ' ' + j[0] + '?'
                                print('PASDT3')
                                questions.append(question)

                        elif all(key in bucket for key in PASIN3):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'Who' + ' ' + line.words[bucket['VBD']] + ' ' + line.words[
                                    bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                                print('PASIN3')
                                questions.append(question)

                        elif all(key in bucket for key in PAS3):  # 'NNP', 'VBZ' in sentence.
                            question = 'Who' + ' ' + line.words[bucket['VBD']] + ' ' + line.words[
                                bucket['NN']] + '?'
                            print('PAS3')
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT4):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                    question = 'Who' + ' ' + line.words[bucket['VBD']] + ' ' + line.words[
                                        bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                                   bucket['DT']] + ' ' + j[0] + '?'
                                    print('PASDT4')
                                    questions.append(question)

                        elif all(key in bucket for key in PASIN4):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                    question = 'Who' + ' ' + line.words[bucket['VBD']] + ' ' + line.words[
                                        bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                                    print('PASIN4')
                                    questions.append(question)

                        elif all(key in bucket for key in PAS4):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                question = 'Who' + ' ' + line.words[bucket['VBD']] + ' ' + line.words[
                                    bucket['NN']] + '?'
                                print('PAS4')
                                questions.append(question)




                    except:
                        print(" ")
                    ############################################### End past simple #####################################

                    # When the tags are generated 's is split to ' and s. To overcome this issue.
                    if 'VBZ' in bucket and line.words[bucket['VBZ']] == "’":
                        question = question.replace(" ’ ", "'s ")

                    # Print the genetated questions as output.
                    if question != '':
                        print('\n', 'Question: ' + question, '\n\n')

            ################################### WHERE ########################################################
            if ((dic_NER[key][0] == "ORG") or (dic_NER[key][0] == "GPE") or (dic_NER[key][0] == "LOC") or (
                    dic_NER[key][0] == "FAC")):
                answers.append(key)
                print(key)
                for sentence in keyword_dic_sents[key]:
                    # print(sentence)
                    if type(sentence) is str:  # If the passed variable is of type string.
                        line = TextBlob(sentence)  # Create object of type textblob.blob.TextBlob
                    # print(line)

                    bucket = {}  # Create an empty dictionary

                    for i, j in enumerate(line.tags):  # line.tags are the parts-of-speach in English
                        if j[1] not in bucket:
                            bucket[j[1]] = i  # Add all tags to the dictionary or bucket variable

                    question = ''  # Create an empty string

                    # With the use of conditional statements the dictionary is compared with the list created above
                    # print(line.tags)
                    ##################################################################### WHEN OR WHERE ##########################################################################################
                    ######################################## VBN ##################################################
                    if all(key in bucket for key in VBN1):  # 'NNP', 'VBZ'  ,'VBN' in sentence.
                        question = 'Where' + ' ' + 'has' + ' ' + line.words[bucket['NNP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + '?'
                        print('VBN1')
                        questions.append(question)

                    elif all(key in bucket for key in VBN2):  # 'PRP', 'VBZ'  ,'VBN' in sentence.
                        question = 'Where' + ' ' + 'has' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + '?'
                        print('VBN2')
                        questions.append(question)

                    elif all(key in bucket for key in VBN3):  # 'NNP', 'VBP'  ,'VBN' in sentence.
                        question = 'Where' + ' ' + 'have' + ' ' + line.words[bucket['NNPS']] + ' ' + \
                                   line.words[
                                       bucket['VBN']]  + ' ' + '?'
                        print('VBN3')
                        questions.append(question)

                    elif all(key in bucket for key in VBN4):  # 'PRP', 'VBP'  ,'VBN' in sentence.

                        question = 'Where' + ' ' + 'have' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] +  ' ' + '?'
                        print('VBN4')
                        questions.append(question)

                    elif all(key in bucket for key in VBN5):  # 'NNP', 'VBD'  ,'VBN' in sentence.
                        question = 'Where' + ' ' + 'had' + ' ' + line.words[bucket['NNP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']]  + ' ' + '?'
                        print('VBN5')
                        questions.append(question)

                    elif all(key in bucket for key in VBN6):  # 'PRP', 'VBD'  ,'VBN' in sentence.
                        question = 'Where' + ' ' + 'had' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + '?'
                        print('VBN6')
                        questions.append(question)

                    elif all(key in bucket for key in VBN7):  # 'NNPS', 'VBD'  ,'VBN' in sentence.
                        question = 'Where' + ' ' + 'had' + ' ' + line.words[bucket['NNPS']] + ' ' + \
                                   line.words[
                                       bucket['VBN']]  + ' ' + '?'
                        print('VBN7')
                        questions.append(question)

                    ########################################### End Adjective ##################################?????????????????????????!!!!!!!!!!!!!!!!!!'''

                    ########################################### present continouse #############################
                    elif all(key in bucket for key in PRCDT1):  # 'NNP', 'VBG', 'VBZ', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'is' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCDT1")
                            questions.append(question)

                    elif all(key in bucket for key in PRCIN1):  # 'NNP', 'VBG', 'VBZ', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'is' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCIN1")
                            questions.append(question)

                    elif all(key in bucket for key in PRC1):  # 'NNP', 'VBG', 'VBZ', 'IN' in sentence.
                        question = 'Where' + ' ' + 'is' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PRC1")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'are' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCDT2")
                            questions.append(question)

                    elif all(key in bucket for key in PRCIN2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'are' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCIN2")
                            questions.append(question)

                    elif all(key in bucket for key in PRC2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        question = 'Where' + ' ' + 'are' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PRC2")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'Where' + ' ' + 'is' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PRCDT3")
                                questions.append(question)

                    elif all(key in bucket for key in PRCIN3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'Where' + ' ' + 'is' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PRCIN3")
                                questions.append(question)

                    elif all(key in bucket for key in PRC3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                            question = 'Where' + ' ' + 'is' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRC3")
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'Where' + ' ' + 'are' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PRCDT4")
                                questions.append(question)

                    elif all(key in bucket for key in PRCIN4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'Where' + ' ' + 'are' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PRCIN4")
                                questions.append(question)

                    elif all(key in bucket for key in PRC4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                            question = 'Where' + ' ' + 'are' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRC4")
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT5):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'is' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCDT5")
                            questions.append(question)

                    elif all(key in bucket for key in PRCIN5):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'is' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCIN5")
                            questions.append(question)

                    elif all(key in bucket for key in PRC5):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        question = 'Where' + ' ' + 'is' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PRC5")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT6):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'are' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCDT6")
                            questions.append(question)

                    elif all(key in bucket for key in PRCIN6):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'are' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCIN6")
                            questions.append(question)

                    elif all(key in bucket for key in PRC6):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        question = 'Where' + ' ' + 'are' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PRC6")
                        questions.append(question)

                    ########################## Past Cont. ###################################

                    elif all(key in bucket for key in PACDT1):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'was' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACDT1")
                            questions.append(question)

                    elif all(key in bucket for key in PACIN1):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'was' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACIN1")
                            questions.append(question)

                    elif all(key in bucket for key in PAC1):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        question = 'Where' + ' ' + 'was' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PAC1")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT2):  # 'NNP', 'VBG', 'VBD', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'were' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACDT2")
                            questions.append(question)

                    elif all(key in bucket for key in PACIN2):  # 'NNP', 'VBG', 'VBD', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'were' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACIN2")
                            questions.append(question)

                    elif all(key in bucket for key in PAC2):  # 'NNP', 'VBG', 'VBD', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'were' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PAC2")
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT3):  # 'NNP', 'VBG', 'VBD' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                question = 'Where' + ' ' + 'was' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PACDT3")
                                questions.append(question)

                    elif all(key in bucket for key in PACIN3):  # 'NNP', 'VBG', 'VBD' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                question = 'Where' + ' ' + 'was' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PACIN3")
                                questions.append(question)

                    elif all(key in bucket for key in PAC3):  # 'NNP', 'VBG', 'VBD' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                            question = 'Where' + ' ' + 'was' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PAC3")
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT4):  # 'NNPS', 'VBG', 'VBD' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'Where' + ' ' + 'were' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PACDT4")
                                questions.append(question)

                    elif all(key in bucket for key in PACIN4):  # 'NNPS', 'VBG', 'VBD' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'Where' + ' ' + 'were' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PACIN4")
                                questions.append(question)

                    elif all(key in bucket for key in PAC4):  # 'NNPS', 'VBG', 'VBD' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                            question = 'Where' + ' ' + 'were' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PAC4")
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT5):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'was' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACDT5")
                            questions.append(question)

                    elif all(key in bucket for key in PACIN5):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'was' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACIN5")
                            questions.append(question)

                    elif all(key in bucket for key in PAC5):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        question = 'Where' + ' ' + 'was' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PAC5")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT6):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'was' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACDT6")
                            questions.append(question)

                    elif all(key in bucket for key in PACIN6):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'was' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACIN6")
                            questions.append(question)

                    elif all(key in bucket for key in PAC6):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        question = 'Where' + ' ' + 'was' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PAC6")
                        questions.append(question)

                    ############################## Present Simple ######################################
                    elif all(key in bucket for key in PRSDT1):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'does' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + line.words[bucket['NNP']] + ' ' + '?'
                            print('PRSDT1')
                            questions.append(question)

                    elif all(key in bucket for key in PRSIN1):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'does' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + line.words[bucket['NNP']] + ' ' + '?'
                            print('PRSIN1')
                            questions.append(question)

                    elif all(key in bucket for key in PRS1):  # 'NNP', 'VBZ', 'NN' in sentence
                        question = 'Where' + ' ' + 'does' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + ' ' + line.words[bucket['NNP']] + ' ' + '?'
                        print('PRS1')
                        questions.append(question)


                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'Where' + ' does ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBZ']].singularize() + ' ' + line.words[bucket['NNP']] + ' ' + '?'
                                print('PRSDT2')
                                questions.append(question)

                    elif all(key in bucket for key in PRSIN2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'Where' + ' does ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBZ']].singularize() + ' ' + line.words[bucket['NNP']] + ' ' + '?'
                                print('PRSIN2')
                                questions.append(question)

                    elif all(key in bucket for key in PRS2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                            question = 'Where' + ' does ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + line.words[bucket['NNP']] + ' ' + '?'
                            print('PRS2')
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT3):  # 'NNPS', 'VBP', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'do' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRSDT3')
                            questions.append(question)

                    elif all(key in bucket for key in PRSIN3):  # 'NNPS', 'VBP', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'do' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRSIN3')
                            questions.append(question)

                    elif all(key in bucket for key in PRS3):  # 'NNPS', 'VBP', 'NN' in sentence
                        question = 'Where' + ' ' + 'do' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('PRS3')
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'Where' + ' do ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PRSDT4')
                                questions.append(question)

                    elif all(key in bucket for key in PRSIN4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'Where' + ' do ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PRSIN4')
                                questions.append(question)

                    elif all(key in bucket for key in PRS4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                            question = 'Where' + ' do ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRS4')
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT5):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'does' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRSDT5')
                            questions.append(question)

                    elif all(key in bucket for key in PRSIN5):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'does' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRSIN5')
                            questions.append(question)

                    elif all(key in bucket for key in PRS5):  # 'NNP', 'VBZ', 'NN' in sentence
                        question = 'Where' + ' ' + 'does' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('PRS5')
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT6):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'does' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRSDT6')
                            questions.append(question)

                    elif all(key in bucket for key in PRSIN6):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + 'does' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRSIN6')
                            questions.append(question)

                    elif all(key in bucket for key in PRS6):  # 'NNP', 'VBZ', 'NN' in sentence
                        question = 'Where' + ' ' + 'does' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('PRS6')
                        questions.append(question)

                    elif all(key in bucket for key in PRS7):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                            question = 'Where' + ' ' + 'does' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + '?'
                            print('PRS7')
                            questions.append(question)

                    elif all(key in bucket for key in PRS8):  # 'NNP', 'VBZ', 'NN' in sentence
                        question = 'Where' + ' ' + 'does' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + ' ' + '?'
                        print('PRS8')
                        questions.append(question)
                    elif all(key in bucket for key in PRS9):  # 'NNP', 'VBZ', 'NN' in sentence
                        question = 'Where' + ' ' + 'does' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + ' ' + '?'
                        print('PRS9')
                        questions.append(question)
                    elif all(key in bucket for key in PRS10):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                            question = 'Where' + ' ' + 'does' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + '?'
                            print('PRS10')
                            questions.append(question)

                        ########################################### End present simple #################################

                    ##################################################### MD ###########################################
                    elif all(key in bucket for key in MDDT1):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNP']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['NN']] + ' ' +'?'
                            print('MDDT1')
                            questions.append(question)

                    elif all(key in bucket for key in MDIN1):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNP']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['NN']] + ' ' +'?'
                            print('MDIN1')
                            questions.append(question)

                    elif all(key in bucket for key in MD1):  # 'NNP', 'VB' in sentence.
                        question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNP']] + ' ' + \
                                   line.words[
                                       bucket['VB']] + ' ' + '?'
                        print('MD1')
                        questions.append(question)

                    elif all(key in bucket for key in MDDT2):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VB']]  + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('MDDT2')
                                questions.append(question)

                    elif all(key in bucket for key in MDIN2):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + \
                                           line.words[bucket['NN']] + ' ' + '?'
                                print('MDIN2')
                                questions.append(question)

                    elif all(key in bucket for key in MD2):  # 'PRP', 'VB' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                            question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                bucket['PRP']] + ' ' + line.words[
                                           bucket['VB']]+ ' ' + '?'
                            print('MD2')
                            questions.append(question)

                    elif all(key in bucket for key in MDDT3):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNPS']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('MDDT3')
                            questions.append(question)

                    elif all(key in bucket for key in MDIN3):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNPS']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + \
                                       line.words[bucket['NN']] + ' ' + '?'
                            print('MDIN3')
                            questions.append(question)

                    elif all(key in bucket for key in MD3):  # 'NNPS', 'VB' in sentence.
                        question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                            bucket['NNPS']] + ' ' + line.words[
                                       bucket['VB']] + ' ' + '?'
                        print('MD3')
                        questions.append(question)

                    elif all(key in bucket for key in MDDT4):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('MDDT4')
                                questions.append(question)

                    elif all(key in bucket for key in MDIN4):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                                question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + \
                                           line.words[bucket['NN']] + ' ' + '?'
                                print('MDIN4')
                                questions.append(question)

                    elif all(key in bucket for key in MD4):  # 'NNS', 'VB' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they','I','You','We','They']:
                            question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                bucket['PRP']] + ' ' + line.words[
                                           bucket['VB']] + ' ' + '?'
                            print('MD4')
                            questions.append(question)

                    elif all(key in bucket for key in MDDT5):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NN']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('MDDT5')
                            questions.append(question)

                    elif all(key in bucket for key in MDIN5):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NN']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + \
                                       line.words[bucket['NN']] + ' ' + '?'
                            print('MDIN5')
                            questions.append(question)

                    elif all(key in bucket for key in MD5):  # 'NNP', 'VB' in sentence.
                        question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NN']] + ' ' + \
                                   line.words[
                                       bucket['VB']] + ' ' + '?'
                        print('MD5')
                        questions.append(question)

                    elif all(key in bucket for key in MDDT6):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNS']] + ' ' + \
                                       line.words[
                                           bucket['VB']]  + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('MDDT6')
                            questions.append(question)

                    elif all(key in bucket for key in MDIN6):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNS']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + \
                                       line.words[bucket['NN']] + ' ' + '?'
                            print('MDIN6')
                            questions.append(question)

                    elif all(key in bucket for key in MD6):  # 'NNP', 'VB' in sentence.
                        question = 'Where' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNS']] + ' ' + \
                                   line.words[
                                       bucket['VB']] + ' ' + '?'
                        print('MD6')
                        questions.append(question)

                        ####################################### End MD ###############################################
                    ########################################### Past simple #################################
                    try:
                        if all(key in bucket for key in PASDT1):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'Where' + ' did ' + line.words[
                                    bucket['NNP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASDT1')
                                questions.append(question)

                        elif all(key in bucket for key in PASIN1):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'Where' + ' did ' + line.words[
                                    bucket['NNP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASIN1')
                                questions.append(question)

                        elif all(key in bucket for key in PAS1):  # 'NNP', 'VBZ' in sentence.
                            question = 'Where' + ' did ' + line.words[bucket['NNP']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PAS1')
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT2):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                    question = 'Where' + ' did ' + line.words[
                                        bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                        line.words[bucket['VBD']], pos="v") + ' ' + line.words[
                                                   bucket['NN']] + ' ' + '?'
                                    print('PASDT2')
                                    questions.append(question)

                        elif all(key in bucket for key in PASIN2):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                    question = 'Where' + ' did ' + line.words[
                                        bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                        line.words[bucket['VBD']], pos="v") + ' ' + line.words[
                                                   bucket['NN']] + ' ' + '?'
                                    print('PASIN2')
                                    questions.append(question)

                        elif all(key in bucket for key in PAS2):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                question = 'Where' + ' did ' + line.words[
                                    bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PAS2')
                                questions.append(question)

                                # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT3):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'Where' + ' did ' + line.words[
                                    bucket['NNPS']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASDT3')
                                questions.append(question)

                        elif all(key in bucket for key in PASIN3):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'Where' + ' did ' + line.words[
                                    bucket['NNPS']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASIN3')
                                questions.append(question)

                        elif all(key in bucket for key in PAS3):  # 'NNP', 'VBZ' in sentence.
                            question = 'Where' + ' did ' + line.words[bucket['NNPS']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PAS3')
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT4):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                    question = 'Where' + ' did ' + line.words[
                                        bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                        line.words[bucket['VBD']], pos="v") + ' ' + line.words[
                                                   bucket['NN']] + ' ' + '?'
                                    print('PASDT4')
                                    questions.append(question)

                        elif all(key in bucket for key in PASIN4):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                    question = 'Where' + ' did ' + line.words[
                                        bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                        line.words[bucket['VBD']], pos="v") + ' ' + line.words[
                                                   bucket['NN']] + ' ' + '?'
                                    print('PASIN4')
                                    questions.append(question)

                        elif all(key in bucket for key in PAS4):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'Where' + ' did ' + line.words[
                                    bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PAS4')
                                questions.append(question)

                                # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT5):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'Where' + ' did ' + line.words[
                                    bucket['NN']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASDT5')
                                questions.append(question)

                        elif all(key in bucket for key in PASIN5):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'Where' + ' did ' + line.words[
                                    bucket['NN']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASIN5')
                                questions.append(question)

                        elif all(key in bucket for key in PAS5):  # 'NNP', 'VBZ' in sentence.
                            question = 'Where' + ' did ' + line.words[bucket['NN']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PAS5')
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT6):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'Where' + ' did ' + line.words[
                                    bucket['NNS']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASDT6')
                                questions.append(question)

                        elif all(key in bucket for key in PASIN6):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'Where' + ' did ' + line.words[
                                    bucket['NNS']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASIN6')
                                questions.append(question)

                        elif all(key in bucket for key in PAS6):  # 'NNP', 'VBZ' in sentence.
                            question = 'Where' + ' did ' + line.words[bucket['NNS']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PAS6')
                            questions.append(question)

                        elif all(key in bucket for key in PAS7):  # 'NNP', 'VBZ', 'NN' in sentence
                            question = 'Where' + ' ' + 'did' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBD']] + ' ' + '?'
                            print('PAS7')
                            questions.append(question)

                        elif all(key in bucket for key in PAS8):  # 'NNP', 'VBZ', 'NN' in sentence
                            question = 'Where' + ' ' + 'did' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBD']] + ' ' + '?'
                            print('PAS8')
                            questions.append(question)
                        elif all(key in bucket for key in PAS9):  # 'NNP', 'VBZ', 'NN' in sentence
                            question = 'Where' + ' ' + 'did' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBD']] + ' ' + '?'
                            print('PAS9')
                            questions.append(question)
                        elif all(key in bucket for key in PAS10):  # 'NNP', 'VBZ', 'NN' in sentence
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'Where' + ' ' + 'did' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBD']] + ' ' + '?'
                                print('PAS10')
                                questions.append(question)

                    except:
                        print(" ")
                    ############################################### End past simple #####################################
                    # When the tags are generated 's is split to ' and s. To overcome this issue.
                    if 'VBZ' in bucket and line.words[bucket['VBZ']] == "’":
                        question = question.replace(" ’ ", "'s ")
                        questions.append(question)

                    # Print the genetated questions as output.
                    if question != '':
                        print('\n', 'Question: ' + question)

            ##################################### WHEN ###################################
            if ((dic_NER[key][0] == "DATE") or (dic_NER[key][0] == "TIME")):
                answers.append(key)
                print(key)
                for sentence in keyword_dic_sents[key]:
                    # print(sentence)
                    if type(sentence) is str:  # If the passed variable is of type string.
                        line = TextBlob(sentence)  # Create object of type textblob.blob.TextBlob
                    # print(line)

                    bucket = {}  # Create an empty dictionary

                    for i, j in enumerate(line.tags):  # line.tags are the parts-of-speach in English
                        if j[1] not in bucket:
                            bucket[j[1]] = i  # Add all tags to the dictionary or bucket variable

                    question = ''  # Create an empty string

                    # With the use of conditional statements the dictionary is compared with the list created above
                    # print(line.tags)
                    ##################################################################### WHEN OR WHERE ##########################################################################################
                    ######################################## VBN ##################################################
                    if all(key in bucket for key in VBN1):  # 'NNP', 'VBZ'  ,'VBN' in sentence.
                        question = 'When' + ' ' + 'has' + ' ' + line.words[bucket['NNP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('VBN1')
                        questions.append(question)

                    elif all(key in bucket for key in VBN2):  # 'PRP', 'VBZ'  ,'VBN' in sentence.
                        question = 'When' + ' ' + 'has' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('VBN2')
                        questions.append(question)

                    elif all(key in bucket for key in VBN3):  # 'NNP', 'VBP'  ,'VBN' in sentence.
                        question = 'When' + ' ' + 'have' + ' ' + line.words[bucket['NNPS']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('VBN3')
                        questions.append(question)

                    elif all(key in bucket for key in VBN4):  # 'PRP', 'VBP'  ,'VBN' in sentence.

                        question = 'When' + ' ' + 'have' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('VBN4')
                        questions.append(question)

                    elif all(key in bucket for key in VBN5):  # 'NNP', 'VBD'  ,'VBN' in sentence.
                        question = 'When' + ' ' + 'had' + ' ' + line.words[bucket['NNP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('VBN5')
                        questions.append(question)

                    elif all(key in bucket for key in VBN6):  # 'PRP', 'VBD'  ,'VBN' in sentence.
                        question = 'When' + ' ' + 'had' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('VBN6')
                        questions.append(question)

                    elif all(key in bucket for key in VBN7):  # 'NNPS', 'VBD'  ,'VBN' in sentence.
                        question = 'When' + ' ' + 'had' + ' ' + line.words[bucket['NNPS']] + ' ' + \
                                   line.words[
                                       bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('VBN7')
                        questions.append(question)

                    ########################################### End Adjective ##################################?????????????????????????!!!!!!!!!!!!!!!!!!'''

                    ########################################### present continouse #############################
                    elif all(key in bucket for key in PRCDT1):  # 'NNP', 'VBG', 'VBZ', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'is' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCDT1")
                            questions.append(question)

                    elif all(key in bucket for key in PRCIN1):  # 'NNP', 'VBG', 'VBZ', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'is' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCIN1")
                            questions.append(question)

                    elif all(key in bucket for key in PRC1):  # 'NNP', 'VBG', 'VBZ', 'IN' in sentence.
                        question = 'When' + ' ' + 'is' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PRC1")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'are' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCDT2")
                            questions.append(question)

                    elif all(key in bucket for key in PRCIN2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'are' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCIN2")
                            questions.append(question)

                    elif all(key in bucket for key in PRC2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                        question = 'When' + ' ' + 'are' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PRC2")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'When' + ' ' + 'is' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PRCDT3")
                                questions.append(question)

                    elif all(key in bucket for key in PRCIN3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'When' + ' ' + 'is' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PRCIN3")
                                questions.append(question)

                    elif all(key in bucket for key in PRC3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                            question = 'When' + ' ' + 'is' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRC3")
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'When' + ' ' + 'are' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PRCDT4")
                                questions.append(question)

                    elif all(key in bucket for key in PRCIN4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'When' + ' ' + 'are' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PRCIN4")
                                questions.append(question)

                    elif all(key in bucket for key in PRC4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                            question = 'When' + ' ' + 'are' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRC4")
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT5):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'is' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCDT5")
                            questions.append(question)

                    elif all(key in bucket for key in PRCIN5):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'is' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCIN5")
                            questions.append(question)

                    elif all(key in bucket for key in PRC5):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        question = 'When' + ' ' + 'is' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PRC5")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRCDT6):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'are' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCDT6")
                            questions.append(question)

                    elif all(key in bucket for key in PRCIN6):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'are' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PRCIN6")
                            questions.append(question)

                    elif all(key in bucket for key in PRC6):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                        question = 'When' + ' ' + 'are' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PRC6")
                        questions.append(question)

                    ########################## Past Cont. ###################################

                    elif all(key in bucket for key in PACDT1):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'was' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACDT1")
                            questions.append(question)

                    elif all(key in bucket for key in PACIN1):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'was' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACIN1")
                            questions.append(question)

                    elif all(key in bucket for key in PAC1):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        question = 'When' + ' ' + 'was' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PAC1")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT2):  # 'NNP', 'VBG', 'VBD', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'were' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACDT2")
                            questions.append(question)

                    elif all(key in bucket for key in PACIN2):  # 'NNP', 'VBG', 'VBD', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'were' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACIN2")
                            questions.append(question)

                    elif all(key in bucket for key in PAC2):  # 'NNP', 'VBG', 'VBD', 'IN' in sentence.
                        question = 'When' + ' ' + 'were' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PAC2")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT3):  # 'NNP', 'VBG', 'VBD' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                question = 'When' + ' ' + 'was' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PACDT3")
                                questions.append(question)

                    elif all(key in bucket for key in PACIN3):  # 'NNP', 'VBG', 'VBD' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                question = 'When' + ' ' + 'was' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PACIN3")
                                questions.append(question)

                    elif all(key in bucket for key in PAC3):  # 'NNP', 'VBG', 'VBD' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                            question = 'When' + ' ' + 'was' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PAC3")
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT4):  # 'NNPS', 'VBG', 'VBD' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'When' + ' ' + 'were' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PACDT4")
                                questions.append(question)

                    elif all(key in bucket for key in PACIN4):  # 'NNPS', 'VBG', 'VBD' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'When' + ' ' + 'were' + ' ' + line.words[bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print("PACIN4")
                                questions.append(question)

                    elif all(key in bucket for key in PAC4):  # 'NNPS', 'VBG', 'VBD' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                            question = 'When' + ' ' + 'were' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PAC4")
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT5):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'was' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACDT5")
                            questions.append(question)

                    elif all(key in bucket for key in PACIN5):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'was' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACIN5")
                            questions.append(question)

                    elif all(key in bucket for key in PAC5):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        question = 'When' + ' ' + 'was' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PAC5")
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PACDT6):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'was' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACDT6")
                            questions.append(question)

                    elif all(key in bucket for key in PACIN6):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'was' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print("PACIN6")
                            questions.append(question)

                    elif all(key in bucket for key in PAC6):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                        question = 'When' + ' ' + 'was' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print("PAC6")
                        questions.append(question)

                    ############################## Present Simple ######################################
                    elif all(key in bucket for key in PRSDT1):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'does' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRSDT1')
                            questions.append(question)

                    elif all(key in bucket for key in PRSIN1):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'does' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRSIN1')
                            questions.append(question)

                    elif all(key in bucket for key in PRS1):  # 'NNP', 'VBZ', 'NN' in sentence
                        question = 'When' + ' ' + 'does' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('PRS1')
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'When' + ' does ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PRSDT2')
                                questions.append(question)

                    elif all(key in bucket for key in PRSIN2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'When' + ' does ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PRSIN2')
                                questions.append(question)

                    elif all(key in bucket for key in PRS2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                            question = 'When' + ' does ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRS2')
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT3):  # 'NNPS', 'VBP', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'do' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRSDT3')
                            questions.append(question)

                    elif all(key in bucket for key in PRSIN3):  # 'NNPS', 'VBP', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'do' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                                bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRSIN3')
                            questions.append(question)

                    elif all(key in bucket for key in PRS3):  # 'NNPS', 'VBP', 'NN' in sentence
                        question = 'When' + ' ' + 'do' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('PRS3')
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'When' + ' do ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PRSDT4')
                                questions.append(question)

                    elif all(key in bucket for key in PRSIN4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'When' + ' do ' + line.words[bucket['PRP']] + ' ' + line.words[
                                    bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PRSIN4')
                                questions.append(question)

                    elif all(key in bucket for key in PRS4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                            question = 'When' + ' do ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRS4')
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT5):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'does' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRSDT5')
                            questions.append(question)

                    elif all(key in bucket for key in PRSIN5):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'does' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRSIN5')
                            questions.append(question)

                    elif all(key in bucket for key in PRS5):  # 'NNP', 'VBZ', 'NN' in sentence
                        question = 'When' + ' ' + 'does' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('PRS5')
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PRSDT6):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'does' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRSDT6')
                            questions.append(question)

                    elif all(key in bucket for key in PRSIN6):  # 'NNP', 'VBZ', 'NN' in sentence
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + 'does' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                                bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PRSIN6')
                            questions.append(question)

                    elif all(key in bucket for key in PRS6):  # 'NNP', 'VBZ', 'NN' in sentence
                        question = 'When' + ' ' + 'does' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        print('PRS6')
                        questions.append(question)

                        ########################################### End present simple #################################

                    ##################################################### MD ###########################################
                    elif all(key in bucket for key in MDDT1):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                bucket['NNP']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('MDDT1')
                            questions.append(question)

                    elif all(key in bucket for key in MDIN1):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                bucket['NNP']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('MDIN1')
                            questions.append(question)

                    elif all(key in bucket for key in MD1):  # 'NNP', 'VB' in sentence.
                        question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNP']] + ' ' + \
                                   line.words[
                                       bucket['VB']] + ' ' + '?'
                        print('MD1')
                        questions.append(question)

                    elif all(key in bucket for key in MDDT2):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                    bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('MDDT2')
                                questions.append(question)

                    elif all(key in bucket for key in MDIN2):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                                question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                    bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + \
                                           line.words[bucket['NN']] + ' ' + '?'
                                print('MDIN2')
                                questions.append(question)

                    elif all(key in bucket for key in MD2):  # 'PRP', 'VB' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it', 'He', 'She', 'It']:
                            question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                bucket['PRP']] + ' ' + line.words[
                                           bucket['VB']] + ' ' + '?'
                            print('MD2')
                            questions.append(question)

                    elif all(key in bucket for key in MDDT3):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                bucket['NNPS']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('MDDT3')
                            questions.append(question)

                    elif all(key in bucket for key in MDIN3):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                bucket['NNPS']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + \
                                       line.words[bucket['NN']] + ' ' + '?'
                            print('MDIN3')
                            questions.append(question)

                    elif all(key in bucket for key in MD3):  # 'NNPS', 'VB' in sentence.
                        question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                            bucket['NNPS']] + ' ' + line.words[
                                       bucket['VB']] + ' ' + '?'
                        print('MD3')
                        questions.append(question)

                    elif all(key in bucket for key in MDDT4):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                    bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('MDDT4')
                                questions.append(question)

                    elif all(key in bucket for key in MDIN4):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                    bucket['PRP']] + ' ' + \
                                           line.words[
                                               bucket['VB']] + ' ' + \
                                           line.words[bucket['NN']] + ' ' + '?'
                                print('MDIN4')
                                questions.append(question)

                    elif all(key in bucket for key in MD4):  # 'NNS', 'VB' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                            question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                bucket['PRP']] + ' ' + line.words[
                                           bucket['VB']] + ' ' + '?'
                            print('MD4')
                            questions.append(question)

                    elif all(key in bucket for key in MDDT5):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NN']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('MDDT5')
                            questions.append(question)

                    elif all(key in bucket for key in MDIN5):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NN']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + \
                                       line.words[bucket['NN']] + ' ' + '?'
                            print('MDIN5')
                            questions.append(question)

                    elif all(key in bucket for key in MD5):  # 'NNP', 'VB' in sentence.
                        question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NN']] + ' ' + \
                                   line.words[
                                       bucket['VB']] + ' ' + '?'
                        print('MD5')
                        questions.append(question)

                    elif all(key in bucket for key in MDDT6):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                bucket['NNS']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('MDDT6')
                            questions.append(question)

                    elif all(key in bucket for key in MDIN6):  # 'NNP', 'VB' in sentence.
                        if line.words[bucket['NN']] != j[0]:
                            question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[
                                bucket['NNS']] + ' ' + \
                                       line.words[
                                           bucket['VB']] + ' ' + \
                                       line.words[bucket['NN']] + ' ' + '?'
                            print('MDIN6')
                            questions.append(question)

                    elif all(key in bucket for key in MD6):  # 'NNP', 'VB' in sentence.
                        question = 'When' + ' ' + line.words[bucket['MD']] + ' ' + line.words[bucket['NNS']] + ' ' + \
                                   line.words[
                                       bucket['VB']] + ' ' + '?'
                        print('MD6')
                        questions.append(question)

                        ####################################### End MD ###############################################
                    ########################################### Past simple #################################
                    try:
                        if all(key in bucket for key in PASDT1):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'When' + ' did ' + line.words[
                                    bucket['NNP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASDT1')
                                questions.append(question)

                        elif all(key in bucket for key in PASIN1):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'When' + ' did ' + line.words[
                                    bucket['NNP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASIN1')
                                questions.append(question)

                        elif all(key in bucket for key in PAS1):  # 'NNP', 'VBZ' in sentence.
                            question = 'When' + ' did ' + line.words[bucket['NNP']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PAS1')
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT2):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                    question = 'When' + ' did ' + line.words[
                                        bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                        line.words[bucket['VBD']], pos="v") + ' ' + line.words[
                                                   bucket['NN']] + ' ' + '?'
                                    print('PASDT2')
                                    questions.append(question)

                        elif all(key in bucket for key in PASIN2):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                    question = 'When' + ' did ' + line.words[
                                        bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                        line.words[bucket['VBD']], pos="v") + ' ' + line.words[
                                                   bucket['NN']] + ' ' + '?'
                                    print('PASIN2')
                                    questions.append(question)

                        elif all(key in bucket for key in PAS2):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['PRP']] in ['he', 'she', 'it','He','She','It']:
                                question = 'When' + ' did ' + line.words[
                                    bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PAS2')
                                questions.append(question)

                                # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT3):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'When' + ' did ' + line.words[
                                    bucket['NNPS']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASDT3')
                                questions.append(question)

                        elif all(key in bucket for key in PASIN3):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'When' + ' did ' + line.words[
                                    bucket['NNPS']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASIN3')
                                questions.append(question)

                        elif all(key in bucket for key in PAS3):  # 'NNP', 'VBZ' in sentence.
                            question = 'When' + ' did ' + line.words[bucket['NNPS']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PAS3')
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT4):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                    question = 'When' + ' did ' + line.words[
                                        bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                        line.words[bucket['VBD']], pos="v") + ' ' + line.words[
                                                   bucket['NN']] + ' ' + '?'
                                    print('PASDT4')
                                    questions.append(question)

                        elif all(key in bucket for key in PASIN4):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                    question = 'When' + ' did ' + line.words[
                                        bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                        line.words[bucket['VBD']], pos="v") + ' ' + line.words[
                                                   bucket['NN']] + ' ' + '?'
                                    print('PASIN4')
                                    questions.append(question)

                        elif all(key in bucket for key in PAS4):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they', 'I', 'You', 'We', 'They']:
                                question = 'When' + ' did ' + line.words[
                                    bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PAS4')
                                questions.append(question)

                                # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT5):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'When' + ' did ' + line.words[bucket['NN']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASDT5')
                                questions.append(question)

                        elif all(key in bucket for key in PASIN5):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'When' + ' did ' + line.words[bucket['NN']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASIN5')
                                questions.append(question)

                        elif all(key in bucket for key in PAS5):  # 'NNP', 'VBZ' in sentence.
                            question = 'When' + ' did ' + line.words[bucket['NN']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PAS5')
                            questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                        elif all(key in bucket for key in PASDT6):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'When' + ' did ' + line.words[
                                    bucket['NNS']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASDT6')
                                questions.append(question)

                        elif all(key in bucket for key in PASIN6):  # 'NNP', 'VBZ' in sentence.
                            if line.words[bucket['NN']] != j[0]:
                                question = 'When' + ' did ' + line.words[
                                    bucket['NNS']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                                print('PASIN6')
                                questions.append(question)

                        elif all(key in bucket for key in PAS6):  # 'NNP', 'VBZ' in sentence.
                            question = 'When' + ' did ' + line.words[bucket['NNS']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            print('PAS6')
                            questions.append(question)


                    except:
                        print(" ")
                    ############################################### End past simple #####################################
                    # When the tags are generated 's is split to ' and s. To overcome this issue.
                    if 'VBZ' in bucket and line.words[bucket['VBZ']] == "’":
                        question = question.replace(" ’ ", "'s ")
                        questions.append(question)

                    # Print the genetated questions as output.
                    if question != '':
                        print('\n', 'Question: ' + question)

        keyword_Questions_dic[key] = questions




    except:
        print("No WH Questions Generated for that Keyword")
        keyword_Questions_dic[key] = "No WH Questions Generated for that Keyword"

    return keyword_Questions_dic


def Retuen_Q_Dic():
    return keyword_Questions_dic


def Return_NER_POS():
    return keyword_dic_NER


def Return_Rake():
    return Rakedic

'''
def main():
    # text = ( """ Word Thousands of demonstrators have marched through London to protest the war in Iraq and demand the withdrawal of British troops from that country . Families of soldiers killed in the conflict joined the protesters who carried banners with such slogans as " Bush Number One Terrorist " and " Stop the Bombings . " They marched from the Houses of Parliament to a rally in Hyde Park . Police put the number of marchers at "10 while organizers claimed it was "1 . The protest comes on the eve of the annual conference of Britain 's ruling Labor Party in the southern English seaside resort of Brighton . The party is divided over Britain 's participation in the Iraq conflict and the continued deployment of "8 British troops in that country . The London march came ahead of anti-war protests today in other cities " including Rome " Paris " and Madrid . The International Atomic Energy Agency is to hold second day of talks in Vienna Wednesday on how to respond to Iran 's resumption of low-level uranium conversion . Iran this week restarted parts of the conversion process at its Isfahan nuclear plant . Iranian officials say they expect to get access to sealed sensitive parts of the plant Wednesday " after an IAEA surveillance system begins functioning . The step will allow the facility to operate at full capacity . The European Union " with U.S. backing " has threatened to refer Iran to the U.N. Security Council " which could impose sanctions if it finds Tehran has violated the Nuclear Non-Proliferation treaty . Iran 's new President Mahmoud Ahmadinejad said Tuesday that European incentives aimed at persuading Iran to end its nuclear fuel program are an insult to the Iranian nation . Two Germans and four Nigerian oil workers were kidnapped by armed militants during a raid on a boat in Nigeria 's southern oil-rich Delta region . An official with the German firm Bilfinger Berger " Thomas Horbach " said the gunmen stopped the supply boat Wednesday as it sailed from Delta State to Bayelsa State to inspect an offshore oil field owned by Royal-Dutch Shell . The German firm works as a sub-contractor for Shell . Militant groups frequently attack oil operations in the Niger Delta to demand social services and better job opportunities from multinational companies . Poor residents often complain they have been cheated out of the huge riches extracted from their tribal lands - where the bulk of Nigeria 's 2.3 million barrels of petroleum are pumped daily . Suspected Islamist rebels have fired mortar shells at the palace used by Somalia 's interim President Abdullahi Yusuf Ahmad . It was not immediately clear if the president was in the palace in Mogadishu when the attack occurred or if anyone was hurt . Local news reports said at least five mortar shells hit the palace compound and other mortars were fired elsewhere in Mogadishu Wednesday . The attacks occurred after the government said it will go ahead with a reconciliation conference to which more than "1 Somali elders " warlords and politicians are invited . Iraqi military officials say tanks and troops have arrived in the northern city Mosul for a new offensive against al Qaida in Iraq fighters . Officials will not say how many troops have arrived in the Sunni Arab and Kurdish city " where bombings last week killed at least 34 people and wounded more than 200 . U.S. commanders have not explained how American forces will participate in the offensive . Officials say al Qaida in Iraq fighters have fled successful campaigns against them in Anbar province and Baghdad to other northern provinces . Mosul is the largest city north of Baghdad and has long been a stronghold of Sunni militant fighters . In other violence " U.S. officials said one American soldier was killed while on patrol in Baghdad Sunday . Egyptian police have arrested at least 16 members of the opposition Muslim Brotherhood as parts of the country prepare for parliamentary runoff elections Saturday . The arrests occurred Friday in Alexandria . A spokesman for the Brotherhood said the arrests are an attempt to cut the Brotherhood off from its supporters and punishment for winning parliamentary seats in earlier elections . """ )

    # gen_Who_Question(keyword_dic_sents)
    # gen_Where_Question(keyword_dic_sents)
    # gen_What_Question(keyword_dic_sents)
    # gen_When_Question(keyword_dic_sents)
    #Generate_Questions(keyword_dic_sents)
    # print(keyword_Questions_dic)
    # print(keyword_WHOQuestions_dic)
    # print(keyword_WHATQuestions_dic)
    # print(keyword_WHEREQuestions_dic)
    # print(keyword_WHENQuestions_dic)
    #print(Retuen_Q_Dic())
    #print(len(Retuen_Q_Dic()))
    # write_WH_qustions(questions)
    # write_WH_answers(answers)
    #print(fillgap_dic)
    #print(len(fillgap_dic))
    #print(Generate_Questions(keyword_dic_sents))
    lo = keywords_Q_FN("""Once upon a time . . . a widow had an only son whose name was Aladdin. They were very poor and lived from hand to mouth, though Aladdin did what he could to earn some pennies, by picking bananas in faraway places. One day, as he was looking for wild figs in a grove some way from the town, Aladdin met a mysterious stranger. This smartly dressed dark-eyed man with a trim black beard and a splendid sapphire in his turban, asked Aladdin an unusual question: "Come here, boy," he ordered. "How would you like to earn a silver penny?" "A silver penny!" exclaimed Aladdin. "Sir, I'd do anything for that kind of payment." "I'm not going to ask you to do much. Just go down that manhole. I'm much too big to squeeze through myself. If you do as I ask, you'll have your reward." The stranger helped Aladdin lift the manhole cover, for it was very heavy. Slim and agile as he was, the boy easily went down. His feet touched stone and he carefully made his way down some steps . . . and found himself in a large chamber. It seemed to sparkle, though dimly lit by the flickering light of an old oil lamp. When Aladdin's eyes became used to the gloom, he saw a wonderful sight: trees dripping with glittering jewels, pots of gold and caskets full of priceless gems. Thousands of precious objects lay scattered about. It was a treasure trove! Unable to believe his eyes, Aladdin was standing dazed when he heard a shout behind him. "The lamp! Put out the flame and bring me the lamp!" Surprised and suspicious, for why should the stranger, out of all such a treasure want only an old lamp, Aladdin wondered. Perhaps he was a wizard. He decided to be on his guard. Picking up the lamp, he retraced his steps up to the entrance. "Give me the lamp," urged the wizard impatiently. "Hand it over," he began to shout, thrusting out his arm to grab it, but Aladdin cautiously drew back. "Let me out first . . ." "Too bad for you," snapped the stranger, slamming down the manhole cover, never noticing that, as he did so, a ring slid off his finger. A terrified Aladdin was left in pitch darkness, wondering what the wizard would do next. Then he trod on the ring. Aimlessly putting it on his finger, he twisted it round and round. Suddenly the room was flooded with a rosy light and a great genie with clasped hands appeared on a cloud. "At your command, sire," said the genie. Now astoundede, Aladdin could only stammer: "I want to go home!" In a flash he was back in his own home, though the door wa tightly shut. "How did you get in?" called his mother from the kitchen stove, the minute she set eyes on him. Excitedly, her son told her of his adventures. "Where's the silver coin?" his mother asked. Aladdin clapped a hand to his brow. For all he had brought home was the old oil lamp "Oh, mother! I'm so sorry. This is all I've got." "Well, let's hope it works. It's so dirty . . ." and the widow began to rub the lamp. Suddenly out shot another genie, in a cloud of smoke. "You've set me free, after centuries! I was a prisoner in the lamp, waiting to be freed by someone rubbing it. Now, I'm your obedient servant. Tell me your wishes." And the genie bowed respectfully, awaiting Aladdin's orders. The boy and his mother gaped wordlessly at this incredible apparition, then the genie said with a hint of impatience in his voice. "I'm here at your command. Tell me what you want. Anything you like!" Aladdin gulped, then said: "Bring us . . . bring . . ." His mother not having yet begun to cook the dinner, went on to say: ". . . a lovely big meal." From that day on, the widow and her son had everything they could wish for: food, clothes and a fine home, for the genie of the lamp granted them everything they asked him. Aladdin grew into a tall handsome young man and his mother felt that he ought to find himself a wife, sooner or later. One day, as he left the market, Aladdin happened to see the Sultan's daughter Halima in her sedan chair being carried through the streets. He only caught a fleeting glimpse of the princess, but it was enough for him to want to marry her. Aladdin told his mother and she quickly said: "I'll ask the Sultan for his daughter's hand. He'll never be able to refuse. Wait and see!" And indeed, the Sultan was easily persuaded by a casket full of big diamonds to admit the widow to the palace. However, when he learned why she had come, he told the widow that her son must bring proof of his power and riches. This was mostly the Chamberlain's idea, for he himself was eager to marry the beautiful black-eyed Sultan's daughter. "If Aladdin wants to marry Halima,' said the Sultan, "he must send me forty slaves tomorrow.Every slave must bring a box of precious stones. And forty Arab warriors must escort the treasure." Aladdin's mother went sadly home. The genie of the magic lamp had already worked wonders, but nothing like this. Aladdin however,when he heard the news, was not at all dismayed. He picked up the lamp, rubbed it harder than ever and told the genie what he required. The genie simply clapped his hands three times. Forty slaves magically appeared, carrying the gemstones, together with their escort of forty Arab warriors. When he saw all thls the next day, the Sultan was taken aback. He never imagined such wealth could exist. Just as he was about to accept Aladdin as his daughter's bridegroom, the envious Chamberlain broke in with a question. "Where wlll they live?" he asked. The Sultan pondered for a moment, then allowlng greed to get the better of hlm, he told Aladdin to build a great, splendid palace for Halima. Aladdin went straight home and, in what was once a wilderness, the genie built him a palace. The last obstacle had been overcome. The wedding tbok place with great celebrations and the Sultan was especially happy at finding such a rich and powerful son-in-law. News of Aladdin's sudden fortune and wealth spread like wildfire, until.... one day, a strange merchant stopped beneath the palace window. "Old lamps for new," he called to the princess, standing on the balcony. Now, Aladdin had always kept his secret to himself. Only his mother knew it and she had never told a soul. Halima, alas, had been kept in the dark. And so, now, wanting to give Alladin a surprise as well as make a good bargain, she fetched the old oil lamp she had seen Aladdin tuck away, and gave it to the merchant in exchange for a new one. The merchant quickly began to rub it . . . and the genie was now at the service of the wizard who had got his magic lamp back. In a second he whisked away all Aladdin's possessions and magically sent the palace and the princess to an unknown land. Aladdin and the Sultan were at their wits' end. Nobody knew what had happened. Only Aladdin knew it had something to do with the magic lamp. But as he wept over the lost genie of the lamp, he remembered the genie of the ring from the wizard's finger. Slipping the ring on his finger, Aladdin twisted it round and round. "Take me to the place where the wizard has hidden my wife," he ordered the genie. In a flash, he found himself inside his own palace, and peeping from behind a curtain, he saw the wizard and the princess, now his servant. "Psst! Psst!" hissed Aladdin. "Aladdin! It's you . . .!" "Ssh. Don't let him hear you. Take this powder and put it into his tea. Trust me." The powder quickly took effect and the wizard fell into a deep sleep. Aladdin hunted for the lamp high and low, but it was nowere to be seen. But it had to be there. How, otherwise, had the wizard moved the palace? As Aladdin gazed at his sleeping enemy, he thought of peering underneath the pillow. "The lamp! At last," sighed Aladdin, hastily rubbing it. "Welcome back, Master!" exclaimed the genie. "Why did you leave me at another's service for so long?" "Welcome," replied Aladdin. "I'm glad to see you again. I've certainly missed you! It's just as well I have you by me again." "At your command," smiled the genie. "First, put this wicked wizard in chains and take him far away where he'll never be found again." The genie grinned with pleasure, nodded his head, and the wizard vanished. Halima clutched Aladdin in fear: "What's going on? Who is that genie?" "Don't worry, everything is all right," Aladdin reassured her, as he told his wife the whole story of how he had met the wizard and found the magic lamp that had enabled him to marry her. Everything went back to normal and the happy pair hugged each other tenderly. "Can we return to our own kingdom?" the princess asked timidly, thinking of her father, so far away. Aladdin glanced at her with a smile. "The magic that brought you here will take you back, but with me at your side, forever." The Sultan was almost ill with worry. His daughter had disappeared along with the palace, and then his son-in-law had vanished too. Nobody knew where they were, not even the wise men hastily called to the palace to divine what had happened. The jealous Chamberlain kept on repeating: "I told you Aladdin's fortune couldn't last." Everyone had lost all hope of ever seeing the missing pair again, when far away, Aladdin rubbed the magic lamp and said to the genie, "Take my wife, myself and the palace back to our own land, as fast as you can." "In a flash, Sire," replied the genie. At the snap of a finger, the palace rose into the air and sped over the Sultan's kingdom, above the heads of his astonished subjects. It gently floated down to earth and landed on its old site. Aladdin and Halima rushed to embrace the Sultan. To this very day, in that distant country, you can still admire the traces of an ancient palace which folk call the palace that came from the skies.""")
    #print(lo[0])
    #print(lo[1])
    #print(lo[2])
    #print(lo[3])
    #dicm = Generate_Questions(lo[1],lo[3])
    #print(dicm)

if __name__ == "__main__":
    main()

'''