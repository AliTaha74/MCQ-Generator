from Flask_Blog.Flask_Blog import WHQ
from Flask_Blog.Flask_Blog import Distractors
from Flask_Blog.Flask_Blog import TF
from Flask_Blog.Flask_Blog import YN

def test(txt):

    lo = WHQ.keywords_Q_FN(txt)
    dicm = WHQ.Generate_Questions(lo[1], lo[3])
    dic_h = {**lo[2], **lo[3]}
    dic_distractors_h = Distractors.distractors_module(dic_h)
    lqfwh = Distractors.get_questions_and_answers(dic_distractors_h, dicm, lo[0])
    dicn = TF.gen_T_F_Question(lo[1], dic_distractors_h)
    lqtf = TF.get_TF_and_answers(dicn)

    Modal_Q = YN.gen_Modal_Question(lo[1])
    YN_Q = YN.gen_y_N_Question(Modal_Q, dic_distractors_h)
    ln = YN.convert_dic_List(YN_Q)

    final_Qs = lqfwh + lqtf + ln
    #WHQ.main()
    #Distractors.main()
    #TF.main()
    #questions = TF.Final_Qestions
    #print(final_Qs)
    return final_Qs

#Q=[["Who lives in Alaska?",["Alex","Mark","John","Tom"]],["Where does Mark live ?",["Alaska","Arisona","California","Texas"]],["Does Mark live in Texas?",["Yes","No"]],["Mark lives in Alaska?",["True","False"]],["...... lives in Alaska",["Alex","Mark","John","Tom"]]]
