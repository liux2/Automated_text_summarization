import os
import sys
import json
import pytextrank

def stage1(path_stage0, path_stage1):
    #Stage 1
    with open(path_stage1, 'w') as f:
        for graf in pytextrank.parse_doc(pytextrank.json_iter(path_stage0)):
            f.write("%s\n" % pytextrank.pretty_print(graf._asdict()))
            # to view output in this notebook
            #print(pytextrank.pretty_print(graf))

def stage2(path_stage1, path_stage2):
    #Stage 2
    graph, ranks = pytextrank.text_rank(path_stage1)
    pytextrank.render_ranks(graph, ranks)

    with open(path_stage2, 'w') as f:
        for rl in pytextrank.normalize_key_phrases(path_stage1, ranks):
            f.write("%s\n" % pytextrank.pretty_print(rl._asdict()))

def stage3(path_stage1, path_stage2, path_stage3):
    #Stage 3
    kernel = pytextrank.rank_kernel(path_stage2)

    with open(path_stage3, 'w') as f:
        for s in pytextrank.top_sentences(kernel, path_stage1):
            f.write(pytextrank.pretty_print(s._asdict()))
            f.write("\n")

def stage4(path_stage2, path_stage3, phrase_l, word_l):
    #Stage 4
    phrases = [p for p in pytextrank.limit_keyphrases(path_stage2, phrase_limit=int(phrase_l))]
    sent_iter = sorted(pytextrank.limit_sentences(path_stage3, word_limit=int(word_l)), key=lambda x: x[1])
    s = []

    for sent_text, idx in sent_iter:
        s.append(" ".join(sent_text))

    return phrases, s
