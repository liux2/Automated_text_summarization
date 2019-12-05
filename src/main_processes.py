import os
import sys
import json
import pytextrank
import sentiment_mod as s
import named_entity as ne
import pytextrank_stages as ptr

path_stage0 = "src/corpus.json"
path_stage1 = "src/stage1.json"
path_stage2 = "src/stage2.json"
path_stage3 = "src/stage3.json"

def pre_processes(ans_full_path, special_signs):
    #get special signs (remove these special signs to get higher accuracy)
    sp_signs = ''
    with open(special_signs, 'rt') as f:
        for line in f:
            #remove \n in line string
            line = line.translate({ord(c): None for c in '\n'})
            sp_signs = sp_signs+line
    #txt to dict to json
    lines = []
    with open(ans_full_path, 'rt') as f:
        for line in f:
            #remove special signs in line string
            line = line.translate({ord(c): None for c in sp_signs})
            lines.append(line)
    index = 0
    for line in lines:
        temp_dict = {}
        if not line.strip() == "":
            temp_dict["text"] = "%s" % line.strip("\n")
            temp_dict["id"] = "%s" % str(index)
        #print(temp_dict)
        index+=1
        with open(path_stage0, 'w') as f:
            json.dump(temp_dict, f)

def m_processes(s_list):
    #rephrase sentences list and keywords list
    #get sentences list
    one_conv_names_list = [] #contains all org names in one conversation
    stage3_list = [] #contains dictionary objects from stage3 json
    final_stage3_list = []
    sentiment_kw_list = []
    with open(path_stage3, 'r') as f:
        for line in f:
            x = json.loads(line)
            x.update(used = 'n')
            stage3_list.append(x)

    #mapping stage 4 sentences with sentences list
    #sent_dict is the individual json object in json file
    for curr_sent in s_list:
        for sent_dict in stage3_list:
            if sent_dict.get('text') == curr_sent:
                sent_dict.update(used = 'y')
    #check if any sentence left
    for sent_dict in stage3_list:
        if sent_dict.get('used') == 'n':
            #go through sentimental check
            temp_tuple = s.sentiment(sent_dict.get('text'))
    #get organization names by stanford_ner
    for sent_dict in stage3_list:
        temp_name = ne.orgs(sent_dict.get('text')) #here text might need to convert double to single (or don't need)'''
        if temp_name != []:
            sent_dict.update(used = 'y')
        one_conv_names_list = one_conv_names_list + temp_name #merge temp list to main list
    #get special org names by list (e.g. Allegheny as Allegheny College)
    #get all 'y's in a list
    for i in range(len(stage3_list)):
        for sent_dict in stage3_list:
            if sent_dict.get('idx') == i:
                if sent_dict.get('used') == 'y':
                    final_stage3_list.append(sent_dict.get('text'))

    return final_stage3_list, sentiment_kw_list, one_conv_names_list

def cleanup():
    #clean up
    os.remove("src/corpus.json")
    os.remove("src/stage1.json")
    os.remove("src/stage2.json")
    os.remove("src/stage3.json")
    if os.path.exists("graph.dot"):
        os.remove("graph.dot")

def structure(ans_full_path, directory_path, special_signs, phrase_l, word_l, exc_path, kws_path):
    pre_processes(ans_full_path, special_signs)
    ptr.stage1(path_stage0, path_stage1)
    ptr.stage2(path_stage1, path_stage2)
    ptr.stage3(path_stage1, path_stage2, path_stage3)
    final_tuple = m_processes(ptr.stage4(path_stage2, path_stage3, phrase_l, word_l)[1])
    final_sentenses = " ".join(final_tuple[0])
    raw_keywords_list = ptr.stage4(path_stage2, path_stage3, phrase_l, word_l)[0] + final_tuple[1] + final_tuple[2]
    nondpct_keyword_list = [keywords.lower() for keywords in raw_keywords_list]
    #remove keywords within longer key phrase
    for keyword in nondpct_keyword_list:
        temp_list = nondpct_keyword_list.copy()
        temp_list.remove(keyword)
        for item in temp_list:
            if keyword.find(item) != -1 and item != '\n':
                nondpct_keyword_list.remove(item)
    final_keywords = ", ".join(set(nondpct_keyword_list))
    #set() is for same keywords
    #intermidiate files
    with open(exc_path,'a') as e:
        e.write(final_sentenses+'\n')
    with open(kws_path,'a') as k:
        k.write(final_keywords+'\n')
    cleanup()
