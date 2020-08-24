# Reka
import re
import RAKE
import spacy
import operator
import neuralcoref
import sys
import nltk
from nltk import tokenize
from textblob import Word
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
import random
import copy

# **********************************************************Keyword extraction*****************************************

############### global var###################

keyword_dic_NER = {}  # de feha el kelma w el NER index 0 w mena haydef l POS index 1
keyword_dic_sents = {}  # de feha kol klma w sents bta3tha
qustions = []
answers = []
Rakelist = []
################# get keywords with rake################
# with open("/content/drive/My Drive/Cinderella_story.txt", 'r',encoding = "ISO-8859-1") as f:
# content = f.read()
text = str(
    '''Mina is playing football.Mina reads a story.''')  # /////////////////////////////henamomken t7to l text lly htsht8lo 3leh 3la tol

output = re.sub('([\n\r\t ]{2,})', ' ', text)
rake_object = RAKE.Rake(RAKE.SmartStopList())
All_keywords = rake_object.run(output, maxWords=2)
#####################################
nlp = spacy.load('en_core_web_lg')
neuralcoref.add_to_pipe(nlp)
doc = nlp(output)
output = doc._.coref_resolved  ############# el text elly m3aya dlw2ty m3mol replacy le kol damer
doc = nlp(output)
# Extract keywords
for word in All_keywords:
    if word[1] >= 4:
        Rakelist.append(word[0])
for ent in doc.ents:
    keyword_dic_NER[ent.text] = [ent.label_]
#########################
for word in Rakelist:
    for sent in doc.sents:
        tmp_sent = str(sent)
        if " " not in tmp_sent:
            if word in str(tmp_sent):
                tmpword = " " + word + " "
                qustions.append(tmp_sent.replace(tmpword, "........"))
                answers.append(word)
        else:
            if word in str(tmp_sent):
                qustions.append(tmp_sent.replace(word, "........"))
                answers.append(word)
for word in keyword_dic_NER.keys():
    sents = []
    for sent in doc.sents:
        tmp_sent = str(sent)
        if " " not in tmp_sent:
            if word in str(tmp_sent):
                tmpword = " " + word + " "
                sents.append(tmp_sent)
                qustions.append(tmp_sent.replace(tmpword, "........"))
                answers.append(word)
        else:
            if word in str(tmp_sent):
                sents.append(tmp_sent)
                qustions.append(tmp_sent.replace(word, "........"))
                answers.append(word)
    keyword_dic_sents[word] = sents
###################
# print(Rakelist)
# print(keyword_dic_NER)
# print(keyword_dic_sents)
# print(qustions)
# print(answers)

# **********************************************************End Keyword extraction*****************************************

############################################################################################################################
############################################################################################################################
############################################################################################################################

# **********************************************************  Gen Modal Questions*****************************************
############### global var###################

dic_tmp = {}  # dictionary carries the Modal Questions Generated
dic1 = {}  # Simple dictionary carries simple sentens
keyword_Questions_dic = {}
distractors_dic = {}  # dictionary carries the distractors for each word
Y_N_Question_dic = {}  # dictionary carries finally Yes or No questions
lemmatizer = WordNetLemmatizer()
md_word = 'ad'  # string used in Modal verb below
a = 'a'  # a dummy var used
questions = list()
answers = []
Y_N_Ques = []
Y_N_List = []
filter_list = []
pattern_name = ''

################### End Global Var#########

# Load English tokenizer, tagger, parser, NER and word vectors
# nlp = spacy.load("en_core_web_sm")
########################################### LISTS #############################################
#############VBN List############## verb to have
#############VBN List############## verb to have
VBN1 = ['NNP', 'VBZ', 'VBN', 'NN']  # Noura has played football
VBNIN1 = ['NNP', 'VBZ', 'VBN', 'NN', 'IN', 'NN']  # Noura has played football in club
VBNDT1 = ['NNP', 'VBZ', 'VBN', 'NN', 'IN', 'DT', 'NN']  # Noura has played football in the club
VBN2 = ['PRP', 'VBZ', 'VBN', 'NN']  # she has played football
VBNIN2 = ['PRP', 'VBZ', 'VBN', 'NN', 'IN', 'NN']  # she has played football in club
VBNDT2 = ['PRP', 'VBZ', 'VBN', 'NN', 'IN', 'DT', 'NN']  # she has played football in the club
VBN3 = ['NNPS', 'VBP', 'VBN', 'NN']  # Noura and Rana have played football
VBNIN3 = ['NNPS', 'VBP', 'VBN', 'NN', 'IN', 'NN']  # Noura and Rana have played football in club
VBNDT3 = ['NNPS', 'VBP', 'VBN', 'NN', 'IN', 'DT', 'NN']  # Noura and Rana have played football in the club
VBN4 = ['PRP', 'VBP', 'VBN', 'NN']  # they have played football
VBNIN4 = ['PRP', 'VBP', 'VBN', 'NN', 'IN', 'NN']  # they have played football in club
VBNDT4 = ['PRP', 'VBP', 'VBN', 'NN', 'IN', 'DT', 'NN']  # they have played football in the club
VBN5 = ['NNP', 'VBD', 'VBN', 'NN']  # Noura had played football
VBNIN5 = ['NNP', 'VBD', 'VBN', 'NN', 'IN', 'NN']  # Noura had played football in club
VBNDT5 = ['NNP', 'VBD', 'VBN', 'NN', 'IN', 'DT', 'NN']  # Noura had played football in the club
VBN6 = ['PRP', 'VBD', 'VBN', 'NN']  # he had played football or they had played football
VBNIN6 = ['PRP', 'VBD', 'VBN', 'NN', 'IN', 'NN']  # he had played football in  club or #hey had played football in club
VBNDT6 = ['PRP', 'VBD', 'VBN', 'NN', 'IN', 'DT',
          'NN']  # he had played football in the club or #they had played football in the club
VBN7 = ['NNPS', 'VBD', 'VBN', 'NN']  # Noura and Rana had played football
VBNIN7 = ['NNPS', 'VBD', 'VBN', 'NN', 'IN', 'NN']  # Noura and Rana had played football in club
VBNDT7 = ['NNPS', 'VBD', 'VBN', 'NN', 'IN', 'DT', 'NN']  # Noura and Rana had played football in the club
VBN8 = ['NNS', 'VBP', 'VBN', 'NN']  # cats have eaten fish
VBNIN8 = ['NNS', 'VBP', 'VBN', 'NN', 'IN', 'NN']  # cats have eaten fish in room
VBNDT8 = ['NNS', 'VBP', 'VBN', 'NN', 'IN', 'DT', 'NN']  # cats have eaten fish in the room
VBN9 = ['NN', 'VBZ', 'VBN', 'NN']  # cat has eaten fish
VBNIN9 = ['NN', 'VBZ', 'VBN', 'NN', 'IN', 'NN']  # cat has eaten fish in room
VBNDT9 = ['NN', 'VBZ', 'VBN', 'NN', 'IN', 'DT', 'NN']  # cat has eaten fish in the room

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

##########End past simple Lists ############


########### MD Lists ###########
MD1 = ['MD', 'NNP', 'VB', 'NN']  # Mina will play football
MD2 = ['MD', 'PRP', 'VB', 'NN']  # He will play football
MD3 = ['MD', 'NNPS', 'VB', 'NN']  # Mina and Omar will play football
MD4 = ['MD', 'PRP', 'VB', 'NN']  # They will play football
MD5 = ['MD', 'NN', 'VB']  # Machine will produce product ----------------------
MD6 = ['MD', 'NNS', 'VB', 'NN']  # Machines will produce product ---------------------------------
############End MD Lists #########

####JJ####
JJ1 = ['NNP', 'VBZ', 'JJ']  # Mina is tall
JJ2 = ['NNPS', 'VBP', 'JJ']  # Mina and Ali are tall
JJ3 = ['PRP', 'VBZ', 'JJ']  # He is tall
JJ4 = ['PRP', 'VBP', 'JJ']  # They are tall
JJ5 = ['NN', 'VBZ', 'JJ']  # Tree is tall
JJ6 = ['NNS', 'VBP', 'JJ']  # Trees are tall


########################################### End LISTS #############################################


# *************************************************Generate Modal Questions **************************************************************

def gen_Modal_Question(keyword_dic_sents):
    """
     outputs question from the given text
    """
    try:
        # txt = TextBlob(string)
        # for line in txt.sentences:
        for key in keyword_dic_sents.keys():
            """
               outputs question from the given text
               """
            # print(keyword_dic_sents[line])
            # print(entity.text, entity.label_)

            answers.append(key)
            # print(key)
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
                #####################################################################gen modal ##########################################################################################
                ######################################## VBN ##################################################
                if all(key in bucket for key in VBNDT1):  # 'NNP', 'VBZ'  ,'VBN' , 'IN ,  'DT' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Has' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                   line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'VBNDT1'
                        questions.append(question)

                elif all(key in bucket for key in VBNIN1):  # 'NNP', 'VBZ'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Has' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = 'VBNIN1'
                        questions.append(question)


                elif all(key in bucket for key in VBN1):  # 'NNP', 'VBZ'  ,'VBN' in sentence.
                    question = 'Has' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                        bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'VBN1'
                    questions.append(question)

                # -----------------------------------------------------------------------------------------#
                elif all(key in bucket for key in VBNDT2):  # 'PRP', 'VBZ'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Has' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                   line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'VBNDT2'
                        questions.append(question)

                elif all(key in bucket for key in VBNIN2):  # 'PRP', 'VBZ'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Has' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = 'VBNIN2'
                        questions.append(question)

                elif all(key in bucket for key in VBN2):  # 'PRP', 'VBZ'  ,'VBN' in sentence.
                    question = 'Has' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                        bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'VBN2'
                    questions.append(question)

                # -----------------------------------------------------------------------------------------#
                elif all(key in bucket for key in VBNDT3):  # 'NNP', 'VBP'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Have' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                   line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'VBNDT3'
                        questions.append(question)

                elif all(key in bucket for key in VBNIN3):  # 'NNP', 'VBP'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Have' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = 'VBNIN3'
                        questions.append(question)

                elif all(key in bucket for key in VBN3):  # 'NNP', 'VBP'  ,'VBN' in sentence.
                    question = 'Have' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                        bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'VBN3'
                    questions.append(question)

                # -----------------------------------------------------------------------------------------#
                elif all(key in bucket for key in VBNDT4):  # 'PRP', 'VBP'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Have' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                   line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'VBNDT4'
                        questions.append(question)

                elif all(key in bucket for key in VBNIN4):  # 'PRP', 'VBP'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Have' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = 'VBNIN4'
                        questions.append(question)

                elif all(key in bucket for key in VBN4):  # 'PRP', 'VBP'  ,'VBN' in sentence.
                    question = 'Have' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                        bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'VBN4'
                    questions.append(question)
                # -----------------------------------------------------------------------------------------#
                elif all(key in bucket for key in VBNDT5):  # 'NNP', 'VBD'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Had' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                   line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'VBNDT5'
                        questions.append(question)

                elif all(key in bucket for key in VBNIN5):  # 'NNP', 'VBD'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Had' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = 'VBNIN5'
                        questions.append(question)

                elif all(key in bucket for key in VBN5):  # 'NNP', 'VBD'  ,'VBN' in sentence.
                    question = 'Had' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                        bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'VBN5'
                    questions.append(question)
                # -----------------------------------------------------------------------------------------#
                elif all(key in bucket for key in VBNDT6):  # 'PRP', 'VBD'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Had' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                   line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'VBNDT6'
                        questions.append(question)

                elif all(key in bucket for key in VBNIN6):  # 'PRP', 'VBD'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Had' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = 'VBNIN6'
                        questions.append(question)

                elif all(key in bucket for key in VBN6):  # 'PRP', 'VBD'  ,'VBN' in sentence.
                    question = 'Had' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                        bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'VBN6'
                    questions.append(question)

                # -----------------------------------------------------------------------------------------#
                elif all(key in bucket for key in VBNDT7):  # 'NNPS', 'VBD'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Had' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                   line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'VBNDT7'
                        questions.append(question)

                elif all(key in bucket for key in VBNIN7):  # 'NNPS', 'VBD'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Had' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = 'VBNIN7'
                        questions.append(question)

                elif all(key in bucket for key in VBN7):  # 'NNPS', 'VBD'  ,'VBN' in sentence.
                    question = 'Had' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                        bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'VBN7'
                    questions.append(question)

                # -----------------------------------------------------------------------------------------#
                elif all(key in bucket for key in VBNDT8):  # 'NNPS', 'VBD'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Have' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                   line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'VBNDT8'
                        questions.append(question)

                elif all(key in bucket for key in VBNIN8):  # 'NNPS', 'VBD'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Have' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = 'VBNIN8'
                        questions.append(question)

                elif all(key in bucket for key in VBN8):  # 'NNPS', 'VBD'  ,'VBN' in sentence.
                    question = 'Have' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                        bucket['VBN']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'VBN8'
                    questions.append(question)

                # -----------------------------------------------------------------------------------------#
                elif all(key in bucket for key in VBNDT9):  # 'NNPS', 'VBD'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Has' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + 'anything' + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                       bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'VBNDT9'
                        questions.append(question)

                elif all(key in bucket for key in VBNIN9):  # 'NNPS', 'VBD'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Has' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + 'anything' + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                        pattern_name = 'VBNIN9'
                        questions.append(question)

                elif all(key in bucket for key in VBN9):  # 'NNPS', 'VBD'  ,'VBN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Has' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBN']] + ' ' + j[0] + ' ' + '?'
                        pattern_name = 'VBN9'
                        questions.append(question)

                # -----------------------------------------------------------------------------------------#

                ########################################### End VBN ##################################?????????????????????????!!!!!!!!!!!!!!!!!!'''

                ########################################### present continouse #############################
                elif all(key in bucket for key in PRCDT1):  # 'NNP', 'VBG', 'VBZ', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Is' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[bucket['VBG']] + ' ' + \
                                   line.words[
                                       bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                       bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'PRCDT1'
                        questions.append(question)

                elif all(key in bucket for key in PRCIN1):  # 'NNP', 'VBG', 'VBZ', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Is' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[bucket['VBG']] + ' ' + \
                                   line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                        pattern_name = 'PRCIN1'
                        questions.append(question)


                elif all(key in bucket for key in PRC1):  # 'NNP', 'VBG', 'VBZ', 'IN' in sentence.
                    question = 'Is' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                        bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'PRC1'
                    questions.append(question)

                # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PRCDT2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Are' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[bucket['VBG']] + ' ' + \
                                   line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                       bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = "PRCDT2"
                        questions.append(question)

                elif all(key in bucket for key in PRCIN2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Are' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[bucket['VBG']] + ' ' + \
                                   line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                        pattern_name = "PRCIN2"
                        questions.append(question)

                elif all(key in bucket for key in PRC2):  # 'NNP', 'VBG', 'VBZ' in sentence.
                    question = 'Are' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                        bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = "PRC2"
                    questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PRCDT3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Is' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                   line.words[
                                       bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = "PRCDT3"
                        questions.append(question)

                elif all(key in bucket for key in PRCIN3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Is' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = "PRCIN3"
                        questions.append(question)

                elif all(key in bucket for key in PRC3):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                    question = 'Is' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                        bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = "PRC3"
                    questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PRCDT4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Are' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                   line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = "PRCDT4"
                        questions.append(question)

                elif all(key in bucket for key in PRCIN4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Are' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = "PRCIN4"
                        questions.append(question)

                elif all(key in bucket for key in PRC4):  # 'NNPS', 'VBG', 'VBP' in sentence.
                    question = 'Are' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                        bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = "PRC4"
                    questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PRCDT5):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Is' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + "anything" + ' ' + line.words[
                                       bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = "PRCDT5"
                        questions.append(question)

                elif all(key in bucket for key in PRCIN5):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Is' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + "anything" + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                        pattern_name = "PRCIN5"
                        questions.append(question)

                elif all(key in bucket for key in PRC5):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Is' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + j[0] + ' ' + '?'
                        pattern_name = "PRC5"
                        questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PRCDT6):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Are' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                       bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = "PRCDT6"
                        questions.append(question)

                elif all(key in bucket for key in PRCIN6):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Are' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = "PRCIN6"
                        questions.append(question)


                elif all(key in bucket for key in PRC6):  # 'NNPS', 'VBG', 'VBP', 'IN' in sentence.
                    question = 'Are' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                        bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = "PRC6"
                    questions.append(question)

                ########################## Past Cont. ###################################
                elif all(key in bucket for key in PACDT1):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Was' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                       bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = "PACDT1"
                        questions.append(question)

                elif all(key in bucket for key in PACIN1):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Was' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = "PACIN1"
                        questions.append(question)


                elif all(key in bucket for key in PAC1):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                    question = 'Was' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                        bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = "PAC1"
                    questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PACDT2):  # 'NNP', 'VBG', 'VBD', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Were' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                       bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = "PACDT2"
                        questions.append(question)

                elif all(key in bucket for key in PACIN2):  # 'NNP', 'VBG', 'VBD', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Were' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = "PACIN2"
                        questions.append(question)

                elif all(key in bucket for key in PAC2):  # 'NNP', 'VBG', 'VBD', 'IN' in sentence.
                    question = 'Were' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                        bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = "PAC2"
                    questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PACDT3):  # 'NNP', 'VBG', 'VBD' in sentence.
                    if line.words[bucket['PRP']] in ['he', 'she', 'it']:
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Was' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                           bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                            pattern_name = "PACDT3"
                            questions.append(question)

                elif all(key in bucket for key in PACIN3):  # 'NNP', 'VBG', 'VBD' in sentence.
                    if line.words[bucket['PRP']] in ['he', 'she', 'it']:
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Was' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                       j[0] + '?'
                            pattern_name = "PACIN3"
                            questions.append(question)

                elif all(key in bucket for key in PAC3):  # 'NNP', 'VBG', 'VBD' in sentence.
                    if line.words[bucket['PRP']] in ['he', 'she', 'it']:
                        question = 'Was' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        pattern_name = "PAC3"
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PACDT4):  # 'NNPS', 'VBG', 'VBD' in sentence.
                    if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they']:
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Were' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                           bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                            pattern_name = "PACDT4"
                            questions.append(question)

                elif all(key in bucket for key in PACIN4):  # 'NNPS', 'VBG', 'VBD' in sentence.
                    if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they']:
                        if line.words[bucket['NN']] != j[0]:
                            question = 'Were' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                                bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                       j[0] + '?'
                            pattern_name = "PACIN4"
                            questions.append(question)

                elif all(key in bucket for key in PAC4):  # 'NNPS', 'VBG', 'VBD' in sentence.
                    if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they']:
                        question = 'Were' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        pattern_name = "PAC4"
                        questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PACDT5):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Was' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + "anything" + ' ' + line.words[bucket['IN']] + ' ' + line.words[
                                       bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = "PACDT5"
                        questions.append(question)

                elif all(key in bucket for key in PACIN5):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Was' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + 'anything' + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'
                        pattern_name = "PACIN5"
                        questions.append(question)

                elif all(key in bucket for key in PAC5):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Was' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + j[0] + ' ' + '?'
                        pattern_name = "PAC5"
                        questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PACDT6):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Were' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                   line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = "PACDT6"
                        questions.append(question)

                elif all(key in bucket for key in PACIN6):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Were' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = "PACIN6"
                        questions.append(question)

                elif all(key in bucket for key in PAC6):  # 'PRP', 'VBG', 'VBP', 'IN' in sentence.
                    question = 'Were' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                        bucket['VBG']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = "PAC6"
                    questions.append(question)

                ############################## Present Simple ######################################
                elif all(key in bucket for key in PRSDT1):  # 'NNP', 'VBZ', 'NN' in sentence
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Does' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                       bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'PRSDT1'
                        questions.append(question)

                elif all(key in bucket for key in PRSIN1):  # 'NNP', 'VBZ', 'NN' in sentence
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Does' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                       bucket['IN']] + ' ' + j[0] + '?'
                        pattern_name = 'PRSIN1'
                        questions.append(question)


                elif all(key in bucket for key in PRS1):  # 'NNP', 'VBZ', 'NN' in sentence
                    question = 'Does' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                        bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'PRS1'
                    questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PRSDT2):  # 'NNP', 'VBZ' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Does ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                       bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'PRSDT2'
                        questions.append(question)

                elif all(key in bucket for key in PRSIN2):  # 'NNP', 'VBZ' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Does ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                       bucket['IN']] + ' ' + j[0] + '?'
                        pattern_name = 'PRSIN2'
                        questions.append(question)


                elif all(key in bucket for key in PRS2):  # 'NNP', 'VBZ' in sentence.
                    question = 'Does ' + line.words[bucket['PRP']] + ' ' + line.words[
                        bucket['VBZ']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'PRS2'
                    questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PRSDT3):  # 'NNPS', 'VBP', 'NN' in sentence
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Do' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                       bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'PRSDT3'
                        questions.append(question)

                elif all(key in bucket for key in PRSIN3):  # 'NNPS', 'VBP', 'NN' in sentence
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Do' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                            bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                       bucket['IN']] + ' ' + j[0] + '?'
                        pattern_name = 'PRSIN3'
                        questions.append(question)

                elif all(key in bucket for key in PRS3):  # 'NNPS', 'VBP', 'NN' in sentence
                    question = 'Do' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[
                        bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'PRS3'
                    questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PRSDT4):  # 'NNP', 'VBZ' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Do ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                       bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'PRSDT4'
                        questions.append(question)

                elif all(key in bucket for key in PRSIN4):  # 'NNP', 'VBZ' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Do ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                       bucket['IN']] + ' ' + j[0] + '?'
                        pattern_name = 'PRSIN4'
                        questions.append(question)

                elif all(key in bucket for key in PRS4):  # 'NNP', 'VBZ' in sentence.
                    question = 'Do ' + line.words[bucket['PRP']] + ' ' + line.words[
                        bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'PRS4'
                    questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PRSDT5):  # 'NNP', 'VBZ', 'NN' in sentence
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Does' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + ' ' + "anything" + ' ' + \
                                   line.words[bucket['IN']] + ' ' + line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'PRSDT5'
                        questions.append(question)

                elif all(key in bucket for key in PRSIN5):  # 'NNP', 'VBZ', 'NN' in sentence
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Does' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + ' ' + "anything" + ' ' + \
                                   line.words[bucket['IN']] + ' ' + j[0] + '?'
                        pattern_name = 'PRSIN5'
                        questions.append(question)

                elif all(key in bucket for key in PRS5):  # 'NNP', 'VBZ', 'NN' in sentence
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Does' + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VBZ']].singularize() + ' ' + j[0] + ' ' + '?'
                        pattern_name = 'PRS5'
                        questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#
                elif all(key in bucket for key in PRSDT6):  # 'NNP', 'VBZ', 'NN' in sentence
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Do' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + \
                                   line.words[bucket['DT']] + ' ' + j[0] + '?'
                        pattern_name = 'PRSDT6'
                        questions.append(question)

                elif all(key in bucket for key in PRSIN6):  # 'NNP', 'VBZ', 'NN' in sentence
                    if line.words[bucket['NN']] != j[0]:
                        question = 'Do' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                            bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[
                                       0] + '?'
                        pattern_name = 'PRSIN6'
                        questions.append(question)

                elif all(key in bucket for key in PRS6):  # 'NNP', 'VBZ', 'NN' in sentence
                    question = 'Do' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[
                        bucket['VBP']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'PRS6'
                    questions.append(question)

                    ########################################### End present simple #################################

                ##################################################### MD ###########################################
                elif all(key in bucket for key in MD1):  # 'NNP', 'VB' in sentence.
                    md_word = line.words[bucket['MD']]
                    question = md_word.capitalize() + ' ' + line.words[bucket['NNP']] + ' ' + line.words[
                        bucket['VB']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'MD1'
                    questions.append(question)

                elif all(key in bucket for key in MD2):  # 'PRP', 'VB' in sentence.
                    if line.words[bucket['PRP']] in ['he', 'she', 'it']:
                        md_word = line.words[bucket['MD']]
                        question = md_word.capitalize() + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VB']].singularize() + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        pattern_name = 'MD2'
                        questions.append(question)

                elif all(key in bucket for key in MD3):  # 'NNPS', 'VB' in sentence.
                    md_word = line.words[bucket['MD']]
                    question = md_word.capitalize() + ' ' + line.words[
                        bucket['NNPS']] + ' ' + line.words[bucket['VB']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                    pattern_name = 'MD3'
                    questions.append(question)

                elif all(key in bucket for key in MD4):  # 'NNS', 'VB' in sentence.
                    if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they']:
                        md_word = line.words[bucket['MD']]
                        question = md_word.capitalize() + ' ' + line.words[bucket['PRP']] + ' ' + line.words[
                            bucket['VB']] + ' ' + line.words[bucket['NN']] + ' ' + '?'
                        pattern_name = 'MD4'
                        questions.append(question)

                elif all(key in bucket for key in MD5):  # 'NNP', 'VB' in sentence.
                    if line.words[bucket['NN']] != j[0]:
                        md_word = line.words[bucket['MD']]
                        question = md_word.capitalize() + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                            bucket['VB']].singularize() + ' ' + j[0] + '?'
                    pattern_name = 'MD5'
                    questions.append(question)

                elif all(key in bucket for key in MD6):  # 'NNP', 'VB' in sentence.
                    md_word = line.words[bucket['MD']]
                    question = md_word.capitalize() + ' ' + line.words[
                        bucket['NNS']] + ' ' + line.words[bucket['VB']].singularize() + ' ' + line.words[
                                   bucket['NN']] + ' ' + '?'
                    pattern_name = 'MD6'
                    questions.append(question)
                    ####################################### End MD ###############################################
                    ###################################### JJ ####################################################
                elif all(key in bucket for key in JJ1):  # 'NNP', 'VB' in sentence.
                    question = 'Is' + ' ' + line.words[bucket['NNP']] + ' ' + line.words[bucket['JJ']] + '?'
                    pattern_name = 'JJ1'
                    questions.append(question)

                elif all(key in bucket for key in JJ2):  # 'PRP', 'VB' in sentence.
                    question = 'Are' + ' ' + line.words[bucket['NNPS']] + ' ' + line.words[bucket['JJ']] + '?'
                    pattern_name = 'JJ2'
                    questions.append(question)

                elif all(key in bucket for key in JJ3):  # 'NNPS', 'VB' in sentence.
                    question = 'Is' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[bucket['JJ']] + '?'
                    pattern_name = 'JJ3'
                    questions.append(question)

                elif all(key in bucket for key in JJ4):  # 'NNPS', 'VB' in sentence.
                    question = 'Are' + ' ' + line.words[bucket['PRP']] + ' ' + line.words[bucket['JJ']] + '?'
                    pattern_name = 'JJ4'
                    questions.append(question)

                elif all(key in bucket for key in JJ5):  # 'NNS', 'VB' in sentence.
                    question = 'Is' + ' ' + line.words[bucket['NN']] + ' ' + line.words[bucket['JJ']] + '?'
                    pattern_name = 'JJ5'
                    questions.append(question)

                elif all(key in bucket for key in JJ6):  # 'NNS', 'VB' in sentence.
                    question = 'Are' + ' ' + line.words[bucket['NNS']] + ' ' + line.words[bucket['JJ']] + '?'
                    pattern_name = 'JJ6'
                    questions.append(question)
                ####################################### END JJ ###########################################################
                ########################################### Past simple #################################
                try:
                    if all(key in bucket for key in PASDT1):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0] and line.words[bucket['VBD']] not in ['was', 'were']:
                            question = 'Did' + ' ' + line.words[bucket['NNP']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                           bucket['IN']] + ' ' + \
                                       line.words[bucket['DT']] + ' ' + j[0] + '?'
                            pattern_name = 'PASDT1'
                            questions.append(question)


                    elif all(key in bucket for key in PASIN1):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0] and line.words[bucket['VBD']] not in ['was', 'were']:
                            question = 'Did ' + line.words[bucket['NNP']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                           bucket['IN']] + ' ' + j[0] + '?'
                            pattern_name = 'PASIN1'
                            questions.append(question)

                    elif all(key in bucket for key in PAS1):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['VBD']] not in ['was', 'were']:
                            question = 'Did ' + line.words[bucket['NNP']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'

                            pattern_name = 'PAS1'
                            questions.append(question)

                        # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PASDT2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0] and line.words[bucket['VBD']] not in ['was', 'were', 'had']:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it']:
                                question = 'Did ' + line.words[bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + \
                                           line.words[bucket['IN']] + ' ' + \
                                           line.words[bucket['DT']] + ' ' + j[0] + '?'

                                pattern_name = 'PASDT2'
                                questions.append(question)

                    elif all(key in bucket for key in PASIN2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0] and line.words[bucket['VBD']] not in ['was', 'were', 'had']:
                            if line.words[bucket['PRP']] in ['he', 'she', 'it']:
                                question = 'Did ' + line.words[bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + \
                                           line.words[bucket['NN']] + ' ' + line.words[bucket['IN']] + ' ' + j[0] + '?'

                                pattern_name = 'PASIN2'
                                questions.append(question)

                    elif all(key in bucket for key in PAS2):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['PRP']] in ['he', 'she', 'it']:
                            if line.words[bucket['VBD']] not in ['was', 'were', 'had']:
                                question = 'Did ' + line.words[
                                    bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'

                                pattern_name = 'PAS2'
                                questions.append(question)

                            # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PASDT3):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0] and line.words[bucket['VBD']] not in ['was', 'were', 'had']:
                            question = 'Did ' + line.words[bucket['NNPS']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                           bucket['IN']] + ' ' + \
                                       line.words[bucket['DT']] + ' ' + j[0] + '?'
                            pattern_name = 'PASDT3'
                            questions.append(question)

                    elif all(key in bucket for key in PASIN3):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0] and line.words[bucket['VBD']] not in ['was', 'were', 'had']:
                            question = 'Did ' + line.words[bucket['NNPS']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                           bucket['IN']] + ' ' + j[0] + '?'
                            pattern_name = 'PASIN3'
                            questions.append(question)

                    elif all(key in bucket for key in PAS3):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['VBD']] not in ['was', 'were']:
                            question = 'Did ' + line.words[bucket['NNPS']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'
                            pattern_name = 'PAS3'
                            questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#
                    elif all(key in bucket for key in PASDT4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0] and line.words[bucket['VBD']] not in ['was', 'were', 'had']:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they']:
                                question = 'Did ' + line.words[bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + \
                                           line.words[bucket['IN']] + ' ' + \
                                           line.words[bucket['DT']] + ' ' + j[0] + '?'

                                pattern_name = 'PASDT4'
                                questions.append(question)

                    elif all(key in bucket for key in PASIN4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0] and line.words[bucket['VBD']] not in ['was', 'were', 'had']:
                            if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they']:
                                question = 'Did ' + line.words[bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + \
                                           line.words[bucket['IN']] + ' ' + j[0] + '?'

                                pattern_name = 'PASIN4'
                                questions.append(question)

                    elif all(key in bucket for key in PAS4):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['PRP']] in ['i', 'you', 'we', 'they']:
                            if line.words[bucket['VBD']] not in ['was', 'were']:
                                question = 'Did ' + line.words[bucket['PRP']] + ' ' + lemmatizer.lemmatize(
                                    line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'

                                pattern_name = 'PAS4'
                                questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#
                    ##  PASDT6 before  PASDT5 ##
                    elif all(key in bucket for key in PASDT6):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0] and line.words[bucket['VBD']] not in ['was', 'were', 'had']:
                            question = 'Did ' + line.words[bucket['NNS']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                           bucket['IN']] + ' ' + \
                                       line.words[bucket['DT']] + ' ' + j[0] + ' ' + '?'

                            pattern_name = 'PASDT6'
                            questions.append(question)

                    elif all(key in bucket for key in PASIN6):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0] and line.words[bucket['VBD']] not in ['was', 'were', 'had']:
                            question = 'Did ' + line.words[bucket['NNS']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + line.words[
                                           bucket['IN']] + ' ' + j[0] + '?'

                            pattern_name = 'PASIN6'
                            questions.append(question)

                    elif all(key in bucket for key in PAS6):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['VBD']] not in ['was', 'were', 'had']:
                            question = 'Did ' + line.words[bucket['NNS']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + line.words[bucket['NN']] + ' ' + '?'

                            pattern_name = 'PAS6'
                            questions.append(question)

                    # -----------------------------------------------------------------------------------------------------------#

                    elif all(key in bucket for key in PASDT5):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0] and line.words[bucket['VBD']] not in ['was', 'were', 'had']:
                            question = 'Did ' + line.words[bucket['NN']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + "anything" + ' ' + line.words[
                                           bucket['IN']] + ' ' + \
                                       line.words[bucket['DT']] + ' ' + j[0] + ' ' + '?'

                            pattern_name = 'PASDT5'
                            questions.append(question)

                    elif all(key in bucket for key in PASIN5):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0] and line.words[bucket['VBD']] not in ['was', 'were', 'had']:
                            question = 'Did ' + line.words[bucket['NN']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + "anything" + ' ' + line.words[
                                           bucket['IN']] + ' ' + j[0] + '?'

                            pattern_name = 'PASIN5'
                            questions.append(question)


                    elif all(key in bucket for key in PAS5):  # 'NNP', 'VBZ' in sentence.
                        if line.words[bucket['NN']] != j[0] and line.words[bucket['VBD']] not in ['was', 'were', 'had']:
                            question = 'Did ' + line.words[bucket['NN']] + ' ' + lemmatizer.lemmatize(
                                line.words[bucket['VBD']], pos="v") + ' ' + j[0] + ' ' + '?'

                            pattern_name = 'PAS5'
                            questions.append(question)

                # -----------------------------------------------------------------------------------------------------------#

                except:
                    a = 'a'
                ############################################### End past simple #####################################
                # When the tags are generated 's is split to ' and s. To overcome this issue.
                if 'VBZ' in bucket and line.words[bucket['VBZ']] == "’":
                    question = question.replace(" ’ ", "'s ")
                    questions.append(question)

                # Print the genetated questions as output.
                # if question != '':
                # print('\n', 'Question: ' + question)
                # print('\n', 'pattern_name: ' + pattern_name)
            keyword_Questions_dic[key] = questions.copy()
            questions.clear()


    except:
        # print(' ')
        # print("No Modal Questions Generated! Please revise your text.")
        keyword_Questions_dic[key] = "No Modal Questions Generated! Please revise your text."

    return (keyword_Questions_dic)


# ********************************************************** End Gen Modal Questions*****************************************

############################################################################################################################
############################################################################################################################

#################################################  Filter   ##########################################################

def filter(str):
    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    word = ''
    for ch in str:
        if ch not in punctuation:
            word = word + ch
    return (word)


# *************************************************End Filter**************************************************************

############################################################################################################################
# ********************************************************** Gen distractors*****************************************

# it's simulated dictionary as the output of  distractors Generation task
#distractors_dic['Mina'] = ['Omar', 'Hazem', 'Ali']


# ********************************************************** End Gen distractors*****************************************
##############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
# ********************************************************** Gen Yes or NO Questions*****************************************
def gen_y_N_Question(dic_tmp, distractors_dic):
    # Y_N_Question_dic = copy.deepcopy(dic_tmp)
    random_numer = random.randint(0, 2)  # to choose one distractor randomly form 3 distractors

    for key in dic_tmp:  # for every key in dic
        old_word = key  # the original keyword
        new_word = distractors_dic[key][random_numer]  # randomly choose a distractor
        key_len = len(dic_tmp[key])  # number of questions related to this key

        for ques in range(key_len):  # for each questions related to this key
            correct_Ques = dic_tmp[key][ques]  # the original question
            if (
                    key in correct_Ques):  # if the key substring of correct question? ; because when sentence converted to ques it sometimes does not still contain the key!
                fake_Ques = correct_Ques.replace(old_word, new_word)  # construct the fake question
                dic_tmp[key][ques] = [correct_Ques, 'Yes', fake_Ques, 'No']  # append the correct and incorrect question
            else:
                dic_tmp[key][ques] = [correct_Ques, 'Yes', correct_Ques,
                                      'Yes']  # this case appends the correct question only ,because no fake question had been constructed
    return (dic_tmp)


# **********************************************************End Gen Yes or NO Questions*****************************************

############################################################################################################################
############################################################################################################################
############################################################################################################################


########################################################## Convert dic to list ##########################################################################
def convert_dic_List(Y_N_Question_dic):
    for key in Y_N_Question_dic:
        for sent in Y_N_Question_dic[key]:
            if (sent[3] == 'No'):  # this condition prevent repetetion
                Y_N_Ques = [sent[0], ["Yes", "No"], sent[
                    1]]  # sent[0] is the correct question ,["Yes" , "No"] is the option list , and sent[1] the 'yes' answer
                Y_N_List.append(Y_N_Ques)
                Y_N_Ques = [sent[2], ["Yes", "No"], sent[
                    3]]  # sent[2] is the fake question ,["Yes" , "No"] is the option list ,and sent[3] the 'no' answer
                Y_N_List.append(Y_N_Ques)
    return Y_N_List


########################################################## End Convert dic to list ############################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################


# **********************************************************write_Y_N_qustions*****************************************
def write_Y_N_qustions(Y_N_List):
    f = open("/content/drive/My Drive/Question_Cinderella_story.txt", "w")
    Q_num = 0
    for i in Y_N_List:
        Q_num = Q_num + 1
        tmp = str(Q_num) + "- " + i[0] + "\n"
        f.write(tmp)
    f.close()


# ********************************************************** End write_Y_N_qustions*****************************************

# **********************************************************write_Y_N_Answer*****************************************
def write_Y_N_Answer(Y_N_List):
    f = open("/content/drive/My Drive/Answer_Cinderella_story.txt", "w")
    Q_num2 = 0
    for i in Y_N_List:
        Q_num2 = Q_num2 + 1
        tmp = str(Q_num2) + "- " + i[2] + "\n"
        f.write(tmp)
    f.close()


# ********************************************************** End write_Y_N_qustions*****************************************
############################################################################################################################
############################################################################################################################
############################################################################################################################

def main():
    # print(distractors_dic)
    # print(keyword_dic_sents)
    dic_tmp = gen_Modal_Question(keyword_dic_sents)
    Y_N_Question_dic = gen_y_N_Question(dic_tmp, distractors_dic)
    Y_N_List = convert_dic_List(Y_N_Question_dic)
    write_Y_N_qustions(Y_N_List)
    write_Y_N_Answer(Y_N_List)

    # print(dic_tmp)
    for key in Y_N_Question_dic:
        for sent in Y_N_Question_dic[key]:
            if (sent[3] == 'No'):
                print(sent[0])
                print(sent[1])
                print(sent[2])
                print(sent[3])


if __name__ == "__main__":
    main()