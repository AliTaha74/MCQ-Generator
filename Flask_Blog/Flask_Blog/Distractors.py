import nltk
nltk.download('wordnet')
nltk.download('wordnet_ic')
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic as wn_ic
import random

from Flask_Blog.Flask_Blog import WHQ

# def preparing_textFormat(text):
#     output = re.sub('([\n\r\t ]{2,})', ' ', text)
#     return output
#

with open("C:\\Users\\AG PC\\Desktop\\Person_def.txt", "r") as f:
    content = f.readlines()
person_wordlist = [x.strip() for x in content]

with open("C:\\Users\\AG PC\\Desktop\\Numbers.txt", "r") as f:
    content = f.readlines()
numbers_wordlist = [x.strip() for x in content]

with open("C:\\Users\\AG PC\\Desktop\\MaleNames.txt", "r") as f:
    content = f.readlines()
male_names_list = [x.strip() for x in content]

with open("C:\\Users\\AG PC\\Desktop\\FemaleNames.txt", "r") as f:
    content = f.readlines()
female_names_list = [x.strip() for x in content]

male_relations_list = ["father", "husband", "son", "brother", "grandfather", "grandson",
                       "uncle", "nephew", "cousin"]
female_relations_list = ["mother", "wife", "daughter", "sister", "grandmother", "granddaughter",
                         "aunt", "niece", "cousin"]
ordinal_list = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth",
                "ninth", "tenth", "eleventh", "twelfth", "thirteenth", "twentieth", "twenty-first",
                "twenty-second","twenty-third", "twenty-fourth", "thirtieth"]
weekDays_list = ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]
months_list = ["january", "february", "march", "april", "may", "june", "july",
               "august", "september", "october", "november", "december"]
seasons_list = ["spring", "summer", "autumn", "winter"]
periodicity_list = ["daily", "hourly", "weekly", "monthly", "yearly"]


documentwords = ['lol']

allpersons_in_text = []
for x in WHQ.Return_NER_POS():
  values = WHQ.Return_NER_POS().get(x)
  if values[0] == "PERSON":
    allpersons_in_text.append(x)
#print(allpersons_in_text)

############################################################################################################
# Using Wordnet to get Distractions


# def check_peron(word_synset):
#     """دي عشان اشوف الكلمة دي بني ادم ولا لا """
#     definition = word_synset.definition()
#     definition = definition.lower()
#     print(definition)
#     words = definition.split(" ")
#     for word in words:
#         if word in person_wordlist:
#             return True
#     return False


# def person_synset(wordstring):
#     """دي عشان ارجع التعريفات synsets الي بتوصف بني ادمين بس من الكلمة ك string"""
#     w_synsets = wn.synsets(wordstring)
#     if len(w_synsets) == 0:
#         return None
#     output = []
#     for synset in w_synsets:
#         if check_peron(synset):
#             output.append(synset)
#     return output

def check_language(word_synset):
    definition = word_synset.definition()
    definition = definition.lower()
    words = definition.split(" ")
    for word in words:
        if word == 'language' or 'language;':
            return True
    return False


def get_language_synset(wordstring):
    w_synsets = wn.synsets(wordstring)
    if len(w_synsets) == 0:
        return None
    output = []
    for synset in w_synsets:
        if check_language(synset):
            output.append(synset)
    return output


def get_synset(wordstring, _POS):
    """دي عشان ارdealing_with_namesجع التعريفات synsets المناسبة بس مع ال POS الي عندي"""
    w_synsets = wn.synsets(wordstring)
    if len(w_synsets) == 0:
        return None
    index = 0
    _POS = _POS.lower()
    print("This is the input POS " + _POS)
    found = False
    for synset in w_synsets:
        s_POS = synset.pos()
        if s_POS == _POS[0]:  # Works only on nouns, verbs, adjectives for now
            found = True
            break
        index += 1
    if found:
        return w_synsets[index]
    else:
        return w_synsets[0]


def get_antonyms(word):
    """بترجع مقابل الكلمة"""
    antonyms = word.lemmas()[0].antonyms()
    if not antonyms:
        return None
    return antonyms


#########################################################################################################
# The sense "concept" path
"""this takes a word and return sibling words within same definition ex: 'Potato' -> 'Eggplant' "Nightshade veggies" """


def hypernyms_o1_words(word):
    wHypernyms = word.hypernyms()
    if not wHypernyms:
        print('Cannot find super Class')
        return None
    return wHypernyms


def hypernyms_o2_words(word):
    parents = hypernyms_o1_words(word)
    if parents is None:
        return None
    output = []
    for parent in parents:
        w_hypers = parent.hypernyms()
        for hyper in w_hypers:
            if hyper not in output:
                output.append(hyper)
    return output


def hyponyms_o1_words(word):
    children = word.hyponyms()
    if not children:
        print('Cannot find Sub-Class')
        return None
    return children


def hyponyms_o2_words(word):
    children = hyponyms_o1_words(word)
    if children is None:
        return None
    output = []
    for child in children:
        w_hypos = child.hyponyms()
        if w_hypos is not None:
            for hypo in w_hypos:
                output.append(hypo)
    return output


def word_siblings(word):
    parents = hypernyms_o1_words(word)
    if parents is None:
        return None
    siblings = hyponyms_o1_words(parents[0])   # We're considering the first parent to be the best
    return siblings


def word_uncles(word):
    word_Hypernyms = hypernyms_o1_words(word)
    if not word_Hypernyms:
        return None
    return word_Hypernyms


def word_cousins(word):
    uncles = word_uncles(word)
    if uncles is None:
        print('Cannot find related words')
        return None
    options = []
    for uncle in uncles:
        cousins = uncle.hyponyms()
        for cousin in cousins:
            options.append(cousin)
    return options


def word_grandcousins(word):
    grandparents = hypernyms_o2_words(word)
    if grandparents is None:
        return None
    output = []
    for gp in grandparents:
        grandchildren = hyponyms_o2_words(gp)
        if grandchildren is not None:
            for gc in grandchildren:
                if gc not in output:
                    output.append(gc)
    return output


#########################################################################################################
# The Instances Path
"""this takes a word and return sibling instances within same category ex: 'Egypt' -> 'Sudan' "African Countries" """


def instance_hypernyms_o1_words(word):
    wHypernyms = word.instance_hypernyms()
    if not wHypernyms:
        print('Cannot find super Class')
        return None
    return wHypernyms


def instance_hypernyms_o2_words(word):
    parents = instance_hypernyms_o1_words(word)
    if parents is None:
        return None
    output = []
    for parent in parents:
        w_hypers = parent.instance_hypernyms()
        for hyper in w_hypers:
            if hyper not in output:
                output.append(hyper)
    return output


def instance_hyponyms_o1_words(word):
    children = word.instance_hyponyms()
    if not children:
        print('Cannot find Sub-Class')
        return None
    return children


def instance_hyponyms_o2_words(word):
    children = instance_hyponyms_o1_words(word)
    if children is None:
        return None
    output = []
    for child in children:
        w_hypos = child.instance_hyponyms()
        if w_hypos is not None:
            for hypo in w_hypos:
                output.append(hypo)
    return output


def word_instance_siblings(word):
    parents = instance_hypernyms_o1_words(word)
    if parents is None:
        return None
    siblings = instance_hyponyms_o1_words(parents[0])   # We're considering the first parent to be the best
    return siblings


def word_instance_uncles(word):
    word_Hypernyms = instance_hypernyms_o1_words(word)
    if not word_Hypernyms:
        return None
    return word_Hypernyms


def word_instance_cousins(word):
    uncles = word_instance_uncles(word)
    if uncles is None:
        print('Cannot find related words')
        return None
    options = []
    for uncle in uncles:
        cousins = uncle.instance_hyponyms()
        for cousin in cousins:
            options.append(cousin)
    return options


def word_instance_grandcousins(word):
    grandparents = instance_hypernyms_o2_words(word)
    if grandparents is None:
        return None
    output = []
    for gp in grandparents:
        grandchildren = instance_hyponyms_o2_words(gp)
        if grandchildren is not None:
            for gc in grandchildren:
                if gc not in output:
                    output.append(gc)
    return output


#########################################################################################################
# The member/part Path
"""this takes a word and return sibling parts within same whole ex: 'Eye' -> 'Mouth' "Face parts" """


def get_whole(word):
    parents = word.part_holonyms()
    if not parents:
        return None
    return parents


def get_part(word):
    children = word.part_meronyms()
    if not children:
        return None
    return children


def get_other_parts(word):
    output = []
    parents = get_whole(word)
    if not parents:
        return None
    parent = parents[0]
    parts = get_part(parent)
    for part in parts:
        if part not in output:
            output.append(part)
    return output


###############################################################################################################
# Measuring similarity and get the final 3 Answers

def distractors_in_document(_candidates, _documentWords):
    "بتجيب الكلمات الي اتذكرت في النص الاصلي عشان يبقي ليها اولوية"
    priority_list = []
    candidate_words = strings_from_synsets(_candidates)
    index = 0
    for c in candidate_words:
        if c in _documentWords:
            priority_list.append(_candidates[index])
        index += 1
    return priority_list


def levensteins_distance(word1, word2):
    "عشان لو عوزنا تشابه في كتابة الكلمتين ولا حاجة"
    strings = strings_from_synsets([word1, word2])
    weight = nltk.edit_distance(strings[0], strings[1])
    threshold = len(strings[0])/2
    return [weight, threshold]


def calc_similarity_weight(word1, word2, similarityFunction=6):
    """بترجع رقم بيمثل التشابه او القري بين الكلمتين"""
    """1 = wup_similarity, 2 = path, 3 = lch, 4 = res, 5 = jcn"""

    brown_ic = wn_ic.ic("ic-brown.dat")
    w1 = word1.wup_similarity(word2)
    w2 = word1.path_similarity(word2)
    w3 = word1.lch_similarity(word2)
    w4 = word1.res_similarity(word2, brown_ic)
    w5 = word1.jcn_similarity(word2, brown_ic)  # WAS FUER 'NEN FICKT

    if similarityFunction == 1:
        return w1
    if similarityFunction == 2:
        return w2
    if similarityFunction == 3:
        return w3
    if similarityFunction == 4:
        return w4
    if similarityFunction == 5:
        return w5

    avg = (w1 + w2 + w3 + (w4 / 10))  # w5 not used as it produces errors
    return avg


def random_list(weight, bestweight):
    """عشان نعرف لو في weight عمال يتكرر وبناءا عليه اختار كلمات عشاوائية متشاركين في الوزن ده
     بدل ما يطلع اول 3 بالترتيب الابجدي وخلاص"""
    if weight > bestweight:
        return False
    elif weight == bestweight:
        return True
    else:
        return None


######################################################################################################################
# Main Functions

def get_distractors(rightAnswer, wrongAnswers, simFunction=6):

    if len(wrongAnswers) < 4:
        return wrongAnswers

    output = []
    candidate_distractors = wrongAnswers[:]
    needed_matches = 3

    priority_list = distractors_in_document(wrongAnswers, documentwords)  # Assuming the Document Words is global
    if len(priority_list) == 3:
        return priority_list
    if len(priority_list) > 3:
        candidate_distractors = priority_list
    else:
        for p in priority_list:
            output.append(p)
        needed_matches = 3 - len(priority_list)

    bestmatches = [[0, 0], [0, 0], [0, 0]]  # Weight then distance then index
    randomwords = []
    best_weight = 0
    i = -1
    for word in candidate_distractors:
        i += 1
        print('iteration ' + str(i + 1))
        weight = calc_similarity_weight(rightAnswer, word, simFunction)
        # distance = levensteins_distance(rightAnswer, word)
        distance = [5, 2]  # Ay arkam 3shan el code myrbsh bs w 3shan ma3odsh aghyro lw 3ozt astkhdm el Levenstein
        print(weight)
        if weight > 5:
            continue
        # Saving same weight words
        if random_list(weight, best_weight) is True:
            randomwords.append(word)
        elif random_list(weight, best_weight) is False:
            best_weight = weight
            randomwords.clear()
            randomwords.append(word)

        if weight > bestmatches[0][0] or (weight == bestmatches[0][0] and distance[0] <= distance[1]):
            bestmatches[2][0] = bestmatches[1][0]
            bestmatches[2][1] = bestmatches[1][1]
            bestmatches[1][0] = bestmatches[0][0]
            bestmatches[1][1] = bestmatches[0][1]
            bestmatches[0][0] = weight
            bestmatches[0][1] = i
        elif weight > bestmatches[1][0] or (weight == bestmatches[1][0] and distance[0] <= distance[1]):
            bestmatches[2][0] = bestmatches[1][0]
            bestmatches[2][1] = bestmatches[1][1]
            bestmatches[1][0] = weight
            bestmatches[1][1] = i
        elif weight > bestmatches[2][0] or (weight == bestmatches[2][0] and distance[0] <= distance[1]):
            bestmatches[2][0] = weight
            bestmatches[2][1] = i

    if len(randomwords) > 3:
        print("Highest Candidates: ", randomwords)
        generated_before = []
        for i in range(3):
            n = random.randint(0, len(randomwords)-1)
            while n in generated_before:
                n = random.randint(0, len(randomwords) - 1)
            output.append(randomwords[n])
            generated_before.append(n)
    elif needed_matches == 3:
        output = [candidate_distractors[bestmatches[0][1]], candidate_distractors[bestmatches[1][1]],
                  candidate_distractors[bestmatches[2][1]]]
    else:
        for i in range(needed_matches):
            output.append(candidate_distractors[bestmatches[i][1]])
    return output


def strings_from_synsets(synsets):
    """Returns a list of strings from a list of wordnet objects"""
    output = []
    for word in synsets:
        lemmas = word.lemmas()

        # to get multi-words for the same meaning
        # for l in lemmas:
        #   output.append(l.name())

        # To get one word
        output.append(lemmas[0].name())
    return output


def print_file(nl_distractors, _test_word):
    sourceFile = open('GP.txt', 'w')
    print(_test_word, file=sourceFile)
    print(nl_distractors, file=sourceFile)
    sourceFile.close()


#################################################################################################################
# Getting distractors without Wordnet

def dealing_with_years(year):
    if not year.isdigit():
        return None
    decade = year[:-1]   # Awl 3 digits
    last_digit = int(year[-1])
    other_years = []
    generatedBefore = [last_digit]
    for i in range(3):  # 3 candidates
        n = random.randint(0,9)
        while n in generatedBefore:
            n = random.randint(0, 9)
        generatedBefore.append(n)
        other_years.append(decade + str(n))
    return other_years


def dealing_with_numbers(number):
    if number not in numbers_wordlist:
        return None
    one2nine = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    hundred2trillion = ["hundred", "thousand", "million", "billion", "trillion"]
    number = number.lower()
    multiword_number = number.split()
    output = []
    if len(multiword_number) == 1:
        for i in range(3):  # 3 candidates
            n = random.choice(numbers_wordlist)
            while n == multiword_number[0]:
                n = random.choice(numbers_wordlist)
            output.append(n)
    elif multiword_number[0] in one2nine:
        for i in range(3):  # 3 candidates
            n = random.choice(one2nine)
            while n == multiword_number[0]:
                n = random.choice(one2nine)
            assembled_string = n
            for j in multiword_number[1:]:
                assembled_string += " " + j
            output.append(assembled_string)
    elif multiword_number[1] in one2nine:
        generated_before = [multiword_number[1]]
        for i in range(3):  # 3 candidates
            n = random.choice(one2nine)
            while n in generated_before:
                n = random.choice(one2nine)
            assembled_string = multiword_number[0] + " " + n
            for j in multiword_number[2:]:
                assembled_string += " " + j
            output.append(assembled_string)
            generated_before.append(n)
    else:
        generated_before = [multiword_number[1]]
        for i in range(3):  # 3 candidates
            n = random.choice(hundred2trillion)
            while n in generated_before:
                n = random.choice(hundred2trillion)
            assembled_string = multiword_number[0] + " " + n
            for j in multiword_number[2:]:
                assembled_string += " " + j
            output.append(assembled_string)
            generated_before.append(n)
    return output


def dealing_with_names(name):
    if name in male_names_list:
        gender = male_names_list
    elif name in female_names_list:
        gender = female_names_list
    else:
        gender = male_names_list
    output = []
    generated_before = [name]
    for iterator in range(3):  # 3 candidates
        n = random.choice(gender)
        while n in generated_before:
            n = random.choice(gender)
        output.append(n)
        generated_before.append(n)
    return output


def dealing_with_kinship(relation):
    relation = relation.lower()
    if relation in male_relations_list:
        gender = male_relations_list
    elif relation in female_relations_list:
        gender = female_relations_list
    else:
        return None
    output = []
    generated_before = [relation]
    for iterator in range(3):  # 3 candidates
        n = random.choice(gender)
        while n in generated_before:
            n = random.choice(gender)
        output.append(n)
        generated_before.append(n)
    return output


def dealing_with_ordinals(word):
    output = []
    generated_before = [word]
    for iterator in range(3):  # 3 candidates
        n = random.choice(ordinal_list)
        while n in generated_before:
            n = random.choice(ordinal_list)
        output.append(n)
        generated_before.append(n)
    return output

def dealing_with_weekDays(word):
    if word not in weekDays_list:
        return None
    output = []
    generated_before = [word]
    for iterator in range(3):  # 3 candidates
        n = random.choice(weekDays_list)
        while n in generated_before:
            n = random.choice(weekDays_list)
        output.append(n)
        generated_before.append(n)
    return output

def dealing_with_months(word):
    if word not in months_list:
        return None
    output = []
    generated_before = [word]
    for iterator in range(3):  # 3 candidates
        n = random.choice(months_list)
        while n in generated_before:
            n = random.choice(months_list)
        output.append(n)
        generated_before.append(n)
    return output

def dealing_with_seasons(word):
    if word not in seasons_list:
        return None
    output = []
    generated_before = [word]
    for iterator in range(3):  # 3 candidates
        n = random.choice(seasons_list)
        while n in generated_before:
            n = random.choice(seasons_list)
        output.append(n)
        generated_before.append(n)
    return output

def dealing_with_periodicity(word):
    if word not in periodicity_list:
        return None
    output = []
    generated_before = [word]
    for iterator in range(3):  # 3 candidates
        n = random.choice(periodicity_list)
        while n in generated_before:
            n = random.choice(periodicity_list)
        output.append(n)
        generated_before.append(n)
    return output

def dealing_without_wordnet(word, NE):
    if NE == "person":
        output = dealing_with_names(word)
    elif NE == "ordinal":
        output = dealing_with_ordinals(word)
    else:
        output = dealing_with_numbers(word)
        if output is None:
            output = dealing_with_years(word)
            if output is None:
                output = dealing_with_weekDays(word)
                if output is None:
                    output = dealing_with_months(word)
                    if output is None:
                        output = dealing_with_seasons(word)
                        if output is None:
                            output = dealing_with_periodicity(word)
                            if output is None:
                                output = dealing_with_kinship(word)
    return output


#####################################################################################################################
# This is the interface function to be used from this module

def run_wordnet(_test_word,_NE,_w_POS):

    output = dealing_without_wordnet(_test_word, _NE)
    if output is not None:
        return output

    test_word_synset = get_synset(_test_word, _w_POS)
    if test_word_synset is None:
        print('Unknown Word')
        return None
    else:
        distractors = []
        candidates = []
        has_dist = True
        if _w_POS == "Adj":
            candidates = get_antonyms(test_word_synset)
            if candidates is None:
                has_dist = False
        else:
            all_NE = []
            if _NE == "LANGUAGE":
                all_NE = get_language_synset(_test_word)
            found = False
            for classedWord in all_NE:
                listforfun = [classedWord]
                print("I Got that meaning " + strings_from_synsets(listforfun)[0])
                p_has_dist = True
                p_candidates = get_other_parts(classedWord)
                if p_candidates is None or len(p_candidates) < 3:
                    p_candidates = word_cousins(classedWord)
                    if p_candidates is None:
                        p_candidates = word_instance_cousins(classedWord)
                        if p_candidates is None:
                            p_has_dist = False
                if p_has_dist:
                    found = True
                    p_distractors = get_distractors(classedWord, p_candidates)
                    for c in p_candidates:
                        candidates.append(c)
                    for d in p_distractors:
                        distractors.append(d)
            if found:
                return distractors


            else:
                candidates = get_other_parts(test_word_synset)
                if candidates is None or len(candidates) < 3:
                    candidates = word_cousins(test_word_synset)
                    if candidates is None:
                        candidates = word_instance_cousins(test_word_synset)
                        if candidates is None:
                            has_dist = False
        if has_dist:
            print("Final Candidates: ", candidates)
            distractors = get_distractors(test_word_synset, candidates)
            NL_distractors = strings_from_synsets(distractors)
            return NL_distractors
        return None



def run_distractors(test_word, w_POS, NE):

    #Cheking if it's a multi-word expression
    words = test_word.split()
    #Turning it into the Wordnet MultiWord Format with Underscore
    if len(words) > 1:
        test_word = ""
        for i in range(len(words)):
            test_word += words[i] + "_"
        test_word = test_word[:-1]
    # Getting Distractors
    print("i am working on " + test_word)
    distractors = run_wordnet(test_word, w_POS, NE)
    multi_words = False
    multi_index = 0
    if distractors is None:
        print("i am treated as multi word")
        for w in words:
            print("Now Working on " + w + " alone")
            distractors = run_wordnet(w, w_POS, NE)
            if distractors:
                multi_words = True
                break
            multi_index += 1
    if distractors is None:
        return ["Nill", "Nill", "Nill"]
    else:
        if multi_words:
            multiword_distractors = []
            for d in distractors:
                temp = ""
                i = 0
                while i < multi_index:
                    temp += words[i] + " "
                    i += 1
                temp += d
                i += 1
                while i < len(words):
                    temp += " " + words[i]
                    i += 1
                multiword_distractors.append(temp)

            while (len(multiword_distractors) < 3):
                multiword_distractors.append("Nill")

            distractors = multiword_distractors
    return distractors


###################################################################################################################
# Dictionaries for project integration & Website

# """ INPUT -> Dictionary with the keywords as key, and value is a list: index1 has NE & index2 has POS"""
#dic_hazem = {**WHQ.Return_NER_POS(),**WHQ.Return_Rake()}
dic_hazem = {}
#dic_hazem = Return_NER_POS()
#All_questions = {**fillgap_dic(),**Retuen_Q_Dic()}
# """OUTPUT -> Dictionary with the keywords as key, and value is a list of 3 distractors"""
dic_dist = {}

def distractors_module(dic_hazem):
    for x in dic_hazem:
        values = dic_hazem.get(x)
        if len(values) < 2:
            final_distractors = run_distractors(x, values[0], "NOUN")
        else:
            final_distractors = run_distractors(x, values[0], values[1])
        dic_dist[x] = final_distractors
    return dic_dist
#print(distractors_module(dic_hazem))
#print(dic_dist)

def get_questions_and_answers(dic_distractors, dic_questions,dic_fill):
    output = []
    for x in dic_questions:
        currentList = []
        if dic_questions[x] == []:
            continue
        else:
            questionsList = dic_questions[x]
            for q in questionsList :
                currentList = []
                answersList = [x]
                answersList.append(dic_distractors[x][0])
                answersList.append(dic_distractors[x][1])
                answersList.append(dic_distractors[x][2])
                currentList.append(q)
                currentList.append(answersList)
                currentList.append(x)
                output.append(currentList)
    for x in dic_fill:
        currentList = []
        if dic_fill[x] == []:
            continue
        else:
            questionsList = dic_fill[x]
            for q in questionsList:
                currentList = []
                answersList = [x]
                answersList.append(dic_distractors[x][0])
                answersList.append(dic_distractors[x][1])
                answersList.append(dic_distractors[x][2])
                currentList.append(q)
                currentList.append(answersList)
                currentList.append(x)
                output.append(currentList)
    return output
#print(get_questions_and_answers(distratoors,fillgap_dic))
#print(distractors_module(dic_hazem))
# target_word = "German"
# word_POS = "Noun"
# named_entity = "LANGUAGE"

# final_distractors = run_distractors(target_word, named_entity, word_POS)
# print("Final Distractors: ", final_distractors)

#Printing to File
#print_file(NL_distractors, test_word)


#################################################################################################################
# All my functions :

# hypernyms()
# instance_hypernyms()
# hyponyms()
# instance_hyponyms()
# member_holonyms()
# substance_holonyms()
# part_holonyms()
# member_meronyms()
# substance_meronyms()
# part_meronyms()
# topic_domains()
# in_topic_domains()
# region_domains()
# in_region_domains()
# usage_domains()
# in_usage_domains()
# attributes()
# entailments()
# causes()
# also_sees()
# verb_groups()
# similar_tos()

# lemma.antonyms()

# synset.pos()
var = WHQ.Rakedic
WH_Fillgap_Q = get_questions_and_answers(distractors_module(dic_hazem), WHQ.Retuen_Q_Dic(), WHQ.fillgap_dic)

#def main():


#if __name__ == '__main__':
    #main()

