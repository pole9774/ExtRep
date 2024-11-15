import numpy as np
from numpy.linalg import norm

from backend.screen import is_same_screen
from utils.StrUtil import StrUtil, get_words_vector_by_tfidf, get_words_sim


def get_screen_sim_score(x_screen, y_screen):
    x_text = []
    for node in x_screen.nodes:
        if node.attrib['text'] != '':
            node_pro = node.attrib['text'].lower().strip()
            tmp_text = StrUtil.tokenize("text", node_pro)
            x_text.extend(tmp_text)

    y_text = []
    for node in y_screen.nodes:
        if node.attrib['text'] != '':
            node_pro = node.attrib['text'].lower().strip()
            tmp_text = StrUtil.tokenize("text", node_pro)
            y_text.extend(tmp_text)


    tmp_str = ' '
    x_text_str = tmp_str.join(x_text)
    xx_text_words, x_weight = get_words_vector_by_tfidf([x_text_str])

    tmp_str = ' '
    y_text_str = tmp_str.join(y_text)
    yy_text_words, y_weight = get_words_vector_by_tfidf([y_text_str])
    text_sim = get_words_sim(xx_text_words, x_weight, yy_text_words, y_weight)

    text_flag = True

    if xx_text_words[0] == 'none' and yy_text_words[0] == 'none':
        text_flag = False

    final_sim = 0

    if text_flag:
        final_sim = text_sim

    return final_sim

def get_node_sim(x_node, y_node, wv2_model):
    flag = False
    word_flag = True

    x_word = []
    x_id = x_node.attrib['resource-id'].lower().strip()
    if x_id != '' and ('/' in x_id):
        x_id = x_id.split('/')[1]
    x_word.extend(StrUtil.tokenize("resource-id", x_id))
    x_word.extend(StrUtil.tokenize("text", x_node.attrib['text'].lower().strip()))
    x_word.extend(StrUtil.tokenize("content-desc", x_node.attrib['content-desc'].lower().strip()))

    y_word = []
    y_id = y_node.attrib['resource-id'].lower().strip()
    if y_id != '' and ('/' in y_id):
        y_id = y_id.split('/')[1]
    y_word.extend(StrUtil.tokenize("resource-id", y_id))
    y_word.extend(StrUtil.tokenize("text", y_node.attrib['text'].lower().strip()))
    y_word.extend(StrUtil.tokenize("content-desc", y_node.attrib['content-desc'].lower().strip()))

    word_sim = 0

    x_out_vocab = []
    y_out_vocab = []
    x_tmp_word = x_word.copy()
    y_tmp_word = y_word.copy()

    for word in x_tmp_word:
        if word not in wv2_model.wv.vocab:
            x_out_vocab.append(word)
    for word in y_tmp_word:
        if word not in wv2_model.wv.vocab:
            y_out_vocab.append(word)

    if len(x_word) != 0 and len(y_word) != 0:
        x_count = 0
        y_count = 0
        x_vec = np.zeros(wv2_model.vector_size)
        y_vec = np.zeros(wv2_model.vector_size)
        for word in x_word:
            if word not in wv2_model.wv.vocab:
                x_count += 1
                continue
            x_vec += wv2_model.wv[word]
        if len(x_word) != x_count:
            x_vec /= (len(x_word) - x_count)
        for word in y_word:
            if word not in wv2_model.wv.vocab:
                y_count += 1
                continue
            y_vec += wv2_model.wv[word]
        if len(y_word) != y_count:
            y_vec /= (len(y_word) - y_count)
        if len(x_word) != x_count and len(y_word) != y_count:
            word_sim = np.dot(x_vec, y_vec) / (norm(x_vec)*norm(y_vec))

    if word_flag:
        return flag, word_sim
    else:
        flag = True
        return flag, 0

def get_ext_sim(base_scenario_model, ext_scenario_model, autoseq_id):
    base_screens = base_scenario_model.screens
    base_edges = base_scenario_model.edges
    ext_cur_edge = ext_scenario_model.edges[autoseq_id]
    ext_begin_screen = ext_scenario_model.screens[ext_cur_edge.begin_id]
    ext_end_screen = ext_scenario_model.screens[ext_cur_edge.end_id]
    ext_cur_node = ext_begin_screen.get_node_by_id(ext_cur_edge.node_id)
    ext_cur_node_attrib = ext_cur_node.attrib

    screen_sim = 0
    for key in base_screens:
        if is_same_screen(base_screens[key], ext_end_screen, 0.9):
            screen_sim = 1
            break

    sim_flag = False
    edge_sim = 0
    for base_edge in base_edges:
        base_node = base_screens[base_edge.begin_id].get_node_by_id(base_edge.node_id)
        base_node_attrib = base_node.attrib
        # cur_sim_flag = True
        # for key in base_node_attrib:
        #     if base_node_attrib[key] != ext_cur_node_attrib[key]:
        #         cur_sim_flag = False
        #         break
        if str(base_node_attrib).replace(" ", "") == str(ext_cur_node_attrib).replace(" ", ""):
            sim_flag = True
            break
        # if cur_sim_flag is True:
        #     sim_flag = True
        #     break
    if sim_flag is True:
        edge_sim = 1

    sim = (screen_sim + edge_sim) / 2

    return sim