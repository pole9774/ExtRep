import os
import pickle
import shutil
import time
import xml.etree.ElementTree as xeTree

from backend.xml_tree import parse_nodes_patch
from scripting.collector import visual, event_seq_replay
from scripting.writer import write_repaired_test_script, locate_element
from utils.calculate_similarity import get_screen_sim_score, get_node_sim
import gensim.models.keyedvectors as word2vec
from utils.operate_current_device import reopen_app


class Repairer:
    """
    Repair the given test script
    """

    def __init__(self, package_name, w, caps, result_save_path, extended_model, extended_edge_bounds, ori_screens_order, ori_edges_order, ori_edge_bounds_order):

        self.package_name = package_name

        current_dir = os.getcwd()
        tmp = "demo/tmpFiles/rep"
        tmp_path_list = tmp.split("/")
        self.path = os.path.join(current_dir, *tmp_path_list)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.result_save_path = result_save_path

        self.extended_model = extended_model
        self.extended_screens = []
        self.extended_edges = []
        self.extended_edge_bounds = extended_edge_bounds
        self.extended_edge_to_bounds = {}

        self.ori_screens_order = ori_screens_order
        self.ori_edges_order = ori_edges_order
        self.ori_edge_bounds_order = ori_edge_bounds_order
        self.ori_edge_to_bounds = {}
        self.screens_no_match = []
        self.edges_no_match = []
        self.cur_round = 0
        self.ori_begin_screen_index = 0
        self.ori_begin_edge_index = 0

        self.target_seqs = [[]]

        # TODO: coordinate sequence of events from app's main screen to the screen where the test begins
        # TODO: if so, add it manually
        self.update_pre_event_sequences = []
        self.pre_event_sequences = []
        for elem in self.update_pre_event_sequences:
            self.pre_event_sequences.append(elem)

        self.screen_id = 1
        self.cur_screen_id = -1
        self.clicked_node = None

        self.distinct_rate = 0.9
        self.text_sim = 0.4

        self.flag = -1
        self.tmp_model = None
        self.w = w

        self.wv2_model = None

        self.ori_event_detail = []
        self.match_detail_info = []

        self.caps = caps

    def preprocess_text(self, model, screen_dir):
        """
        do not remove spaces
        """
        screens = []
        for key in model.screens:
            screen = model.screens[key]
            # patch
            screen_xml_file = os.path.join((screen.act_name + '-' + str(screen.id)), '1.xml')
            screen_xml_path = os.path.join(screen_dir, screen_xml_file)
            with open(screen_xml_path, encoding='utf-8') as f:
                xml_str = f.read()
            root = xeTree.fromstring(xml_str)
            screen_ori_nodes = parse_nodes_patch(root)

            for node in screen.nodes:
                node_str = ''
                for attrib_key in node.attrib:
                    node_str = node_str + node.attrib[attrib_key]
                node_str = node_str.replace(' ', '').lower()
                for ori_node in screen_ori_nodes:
                    ori_node_str = ''
                    for attrib_key in ori_node.attrib:
                        ori_node_str = ori_node_str + ori_node.attrib[attrib_key]
                    ori_node_str = ori_node_str.replace(' ', '').lower()
                    if node_str == ori_node_str:
                        node.attrib = ori_node.attrib
                        break
            screens.append(screen)

        return screens

    def remove_has_succeeding_sequences(self, seq_list, end_ids):
        res_list = []
        for seq in seq_list:
            last_edge = seq[-1]
            if last_edge.end_id not in end_ids:
                res_list.append(seq)

        return res_list

    def find_edge_from_list(self, edge, edge_bounds, edges, edges_bounds):
        for i in range(0, len(edges)):
            cur_edge = edges[i]
            if cur_edge.begin_id == edge.begin_id and cur_edge.end_id == edge.end_id:
                cur_edge_bounds = edges_bounds[i]
                if cur_edge_bounds[0] == edge_bounds[0] and cur_edge_bounds[1] == edge_bounds[1] and \
                        cur_edge_bounds[2] == edge_bounds[2] and cur_edge_bounds[3] == edge_bounds[3]:
                    return cur_edge

        return None

    def extract_original_seqs_base(self, begin_index, w):
        """
        extract the acyclic sequences of length up to w from the original seqs
        """
        res_seqs = [[]]
        screen_ids = []
        begin_edge = self.ori_edges_order[begin_index]
        screen_ids.append(begin_edge.begin_id)
        for i in range(begin_index, min(begin_index+w, len(self.ori_edges_order))):
            edge = self.ori_edges_order[i]
            if edge.end_id in screen_ids:
                break
            else:
                edge_bounds = self.ori_edge_bounds_order[i]
                mapping_edge = self.find_edge_from_list(edge, edge_bounds, self.extended_edges, self.extended_edge_bounds)
                assert mapping_edge is not None, "The current edge cannot be recognized."
                res_seqs[0].append(mapping_edge)

        return res_seqs

    def extract_candidate_seqs_base(self, model, begin_screen_id, w):
        """
        extract all acyclic sequences of length up to w from the given model
        any succeeding edges with a total length not exceeding w should be added
        """
        model_edges = model.edges
        candidate_seqs_dict = {}
        res_seqs_dict = {}

        for i in range(0, w):
            length = i + 1
            tmp_candidate_seqs = []

            if length == 1:
                for edge in model_edges:
                    if edge.begin_id == begin_screen_id:
                        tmp_seq = []
                        tmp_seq.append(edge)
                        tmp_candidate_seqs.append(tmp_seq)
            else:
                has_succeeding_end_ids = []
                for pre_seq in candidate_seqs_dict[length - 1]:
                    screen_ids = []
                    screen_ids.append(begin_screen_id)
                    for edge in pre_seq:
                        screen_ids.append(edge.end_id)

                    for edge in model_edges:
                        if edge.begin_id == screen_ids[-1] and (edge.end_id not in screen_ids):
                            tmp_seq = []
                            tmp_seq.extend(pre_seq)
                            tmp_seq.append(edge)
                            tmp_candidate_seqs.append(tmp_seq)
                            if edge.begin_id not in has_succeeding_end_ids:
                                has_succeeding_end_ids.append(edge.begin_id)
                update_res_seqs_list = self.remove_has_succeeding_sequences(res_seqs_dict[length-1], has_succeeding_end_ids)
                res_seqs_dict[length-1] = update_res_seqs_list

            candidate_seqs_dict[length] = tmp_candidate_seqs
            res_seqs_dict[length] = tmp_candidate_seqs

        res_seqs = []

        for length in range(1, len(res_seqs_dict)+1):
            res_seqs.extend(res_seqs_dict[length])

        print("the total number of candidate branches obtained is: " + str(len(res_seqs)))
        for seq in res_seqs:
            tmp_screen_ids = []
            tmp_screen_ids.append(begin_screen_id)
            for edge in seq:
                tmp_screen_ids.append(edge.end_id)
            print(tmp_screen_ids)
        print("-------------------------------------------------------------------------------")

        return res_seqs

    def extract_candidate_seqs(self, candidate_model, begin_screen_id, w):
        """
        extract all acyclic sequences of length up to w from the given candidate model
        """
        candidate_model_edges = candidate_model.edges
        candidate_seqs_dict = {}

        for i in range(0, w):
            length = i + 1
            print("all candidate sequences of length " + str(length) + " are being extracted ...")
            tmp_candidate_seqs = []

            if length == 1:
                for edge in candidate_model_edges:
                    if edge.begin_id == begin_screen_id:
                        tmp_seq = []
                        tmp_seq.append(edge)
                        tmp_candidate_seqs.append(tmp_seq)
            else:
                for pre_seq in candidate_seqs_dict[length - 1]:
                    screen_ids = []
                    screen_ids.append(begin_screen_id)
                    for edge in pre_seq:
                        screen_ids.append(edge.end_id)

                    for edge in candidate_model_edges:
                        if edge.begin_id == screen_ids[-1] and (edge.end_id not in screen_ids):
                            tmp_seq = []
                            tmp_seq.extend(pre_seq)
                            tmp_seq.append(edge)
                            tmp_candidate_seqs.append(tmp_seq)

            print("the total number of candidate sequences of length " + str(length) + " is: " + str(len(tmp_candidate_seqs)) + ".")
            candidate_seqs_dict[length] = tmp_candidate_seqs

        candidate_seqs = []

        for length in range(1, len(candidate_seqs_dict)+1):
            candidate_seqs.extend(candidate_seqs_dict[length])

        print("the total number of candidate sequences obtained is: " + str(len(candidate_seqs)))
        print("-------------------------------------------------------------------------------")

        return candidate_seqs

    def calculate_branch_sim(self, end_screens, edges):
        """
        Calculate the similarity between the current branch and the original branch(branches are acyclic)
        :param screens: current branch's screens
        :param edges: current branch's edges
        :return:
        """
        # calculate screen similarity
        cur_branch_screen_ids = []
        cur_branch_begin_screen_id = edges[0].begin_id
        cur_branch_screen_ids.append(cur_branch_begin_screen_id)
        for screen in end_screens:
            cur_branch_screen_ids.append(screen.id)

        ori_screen_ids = []
        for screen in self.screens_no_match[self.ori_begin_screen_index:]:
            ori_screen_ids.append(screen.id)

        cur_branch_cal_begin_screen_index = -1
        cur_branch_cal_end_screen_index = len(cur_branch_screen_ids) - 1
        cur_branch_match_end_screen_index = -1
        ori_branch_cal_begin_screen_index = 0
        ori_branch_cal_end_screen_index = -1
        for i in range(0, len(cur_branch_screen_ids)):
            cur_screen_id = cur_branch_screen_ids[i]
            if cur_screen_id in ori_screen_ids:
                cur_branch_cal_begin_screen_index = i
                break

        # no same screens
        if cur_branch_cal_begin_screen_index == -1:
            return 0

        for i in range(len(cur_branch_screen_ids)-1, cur_branch_cal_begin_screen_index-1, -1):
            cur_screen_id = cur_branch_screen_ids[i]
            if cur_screen_id in ori_screen_ids:
                cur_branch_match_end_screen_index = i
                break

        # no same screens except for the begin screen
        if cur_branch_cal_begin_screen_index == 0 and cur_branch_match_end_screen_index == 0:
            return 0

        cur_branch_match_end_screen_id = cur_branch_screen_ids[cur_branch_match_end_screen_index]
        for i in range(0, len(ori_screen_ids)):
            if cur_branch_match_end_screen_id == ori_screen_ids[i]:
                ori_branch_cal_end_screen_index = i
                break

        cur_branch_cal_screen_ids = []
        for i in range(cur_branch_cal_begin_screen_index, cur_branch_cal_end_screen_index+1):
            cur_branch_cal_screen_ids.append(cur_branch_screen_ids[i])
        ori_branch_cal_screen_ids = []
        for i in range(ori_branch_cal_begin_screen_index, ori_branch_cal_end_screen_index+1):
            ori_branch_cal_screen_ids.append(ori_screen_ids[i])

        screen_sim = 0
        max_screen_len = max(len(cur_branch_cal_screen_ids), len(ori_branch_cal_screen_ids))
        u_screen_len = 0
        for cur_id in cur_branch_cal_screen_ids:
            if cur_id in ori_branch_cal_screen_ids:
                u_screen_len += 1
        # remove the common begin screen
        if self.ori_begin_screen_index == 0:
            u_screen_len -= 1
            max_screen_len -= 1
        screen_sim = u_screen_len / max_screen_len

        # calculate edge similarity
        cur_branch_cal_edges = []
        for i in range(cur_branch_cal_begin_screen_index, cur_branch_cal_end_screen_index):
            cur_edge = edges[i]
            cur_branch_cal_edges.append(cur_edge)
        ori_branch_cal_edges = []
        for i in range(ori_branch_cal_begin_screen_index, ori_branch_cal_end_screen_index):
            cur_edge = self.edges_no_match[i+self.ori_begin_screen_index]
            ori_branch_cal_edges.append(cur_edge)

        edge_sim = 0
        max_edge_len = max(len(cur_branch_cal_edges), len(ori_branch_cal_edges))
        u_edge_len = 0
        for cur_branch_edge in cur_branch_cal_edges:
            for ori_branch_edge in ori_branch_cal_edges:
                if cur_branch_edge.begin_id == ori_branch_edge.begin_id and cur_branch_edge.end_id == ori_branch_edge.end_id:
                    cur_branch_edge_bounds = self.extended_edge_to_bounds[cur_branch_edge]
                    ori_branch_edge_bounds = self.ori_edge_to_bounds[ori_branch_edge]
                    same_flag = True
                    for i in range(0, len(cur_branch_edge_bounds)):
                        if cur_branch_edge_bounds[i] != ori_branch_edge_bounds[i]:
                            same_flag = False
                            break
                    if same_flag is True:
                        u_edge_len += 1
                        break
        edge_sim = u_edge_len / max_edge_len

        sim = (edge_sim + screen_sim) / 2

        return sim

    def calculate_seq_trans_prob(self, original_seq, candidate_seq, candidate_model_screens, null_sim):
        """
        similarity between STLs
        """

        max_score = -1
        k = len(original_seq)
        l = len(candidate_seq)
        normalize_param = max(k, l)
        first_node_match_seq = []

        for i in range(0, self.w+1):
            first_part_prob = -1

            first_original_seq = original_seq[0]
            first_candidate_seq = []
            for j in range(1, i+1):
                if j <= len(candidate_seq):
                    first_candidate_seq.append(candidate_seq[j - 1])

            first_base_screen = self.extended_screens[first_original_seq.end_id - 1]
            # first_base_edge_node = self.extended_screens[first_original_seq.begin_id - 1].get_node_by_id(first_original_seq.node_id)
            # if first_base_edge_node is None:
            first_base_edge_bounds = self.extended_edge_to_bounds[first_original_seq]
            first_base_edge_node = self.extended_screens[first_original_seq.begin_id - 1].get_node_by_bounds(first_base_edge_bounds)

            first_node_match_index = -1
            if len(first_candidate_seq) == 0:
                first_part_prob = null_sim
            else:
                for j in range(0, len(first_candidate_seq)):
                    cur_match_node = first_candidate_seq[j]
                    matched_updated_screen = candidate_model_screens[cur_match_node.end_id - 1]
                    matched_updated_edge_node = candidate_model_screens[cur_match_node.begin_id - 1].get_node_by_id(cur_match_node.node_id)

                    screen_sim = get_screen_sim_score(first_base_screen, matched_updated_screen)
                    tmp_flag, edge_sim = get_node_sim(first_base_edge_node, matched_updated_edge_node, self.wv2_model)

                    match_pair_score = (screen_sim + edge_sim) / 2
                    all_pair_multiply_score = pow(null_sim, (len(first_candidate_seq) - 1)) * match_pair_score

                    cur_first_part_prob = pow(all_pair_multiply_score, 1/len(first_candidate_seq))
                    if cur_first_part_prob > first_part_prob:
                        first_part_prob = cur_first_part_prob
                        first_node_match_index = j

            second_original_seq = original_seq[1:]
            second_candidate_seq = candidate_seq[i:]

            if len(second_original_seq) == 0 or len(second_candidate_seq) == 0:
                if len(second_original_seq) == 0 and len(second_candidate_seq) == 0:
                    second_part_prob = 1
                else:
                    second_part_prob = null_sim
            else:
                second_part_prob, inter = self.calculate_seq_trans_prob(second_original_seq, second_candidate_seq, candidate_model_screens, null_sim)

            cur_score = pow(first_part_prob*second_part_prob, 1/normalize_param)

            if cur_score > max_score or (cur_score == max_score and abs(i - 1) <= abs(len(first_node_match_seq) - 1)):
                max_score = cur_score
                first_node_match_seq = []
                for j in range(0, first_node_match_index+1):
                    first_node_match_seq.append(first_candidate_seq[j])

        return max_score, first_node_match_seq

    def calculate_null_sim(self, original_seq_node, original_seq_screen, seq_node, seq_screen):
        """
        calculate the similarity between null and non-null events
        sim = 1/2(min(sim(screenx, screeny)) + min(sim(edgem, edgen)))
        """
        null_screen_sim = 1
        null_edge_sim = 1
        for i in range(0, len(original_seq_screen)):
            for j in range(0, len(seq_screen)):
                screen1 = original_seq_screen[i]
                screen2 = seq_screen[j]
                tmp_screen_sim = get_screen_sim_score(screen1, screen2)
                if tmp_screen_sim < null_screen_sim:
                    null_screen_sim = tmp_screen_sim

        for i in range(0, len(original_seq_node)):
            for j in range(0, len(seq_node)):
                edge1 = original_seq_node[i]
                edge2 = seq_node[j]
                tmp_flag, tmp_edge_sim = get_node_sim(edge1, edge2, self.wv2_model)
                if tmp_edge_sim < null_edge_sim:
                    null_edge_sim = tmp_edge_sim

        null_sim = (null_screen_sim + null_edge_sim) / 2
        return null_sim

    def find_matched_seq_sin_branch(self, original_seq, original_seq_node, original_seq_screen, candidate_seqs, candidate_model_screens):
        max_score = 0
        target_seq = []

        for seq in candidate_seqs:
            seq_node = []
            seq_screen = []
            for edge in seq:
                end_screen = candidate_model_screens[edge.end_id - 1]
                seq_screen.append(end_screen)
                tmp_node = candidate_model_screens[edge.begin_id - 1].get_node_by_id(edge.node_id)
                seq_node.append(tmp_node)

            null_sim = self.calculate_null_sim(original_seq_node, original_seq_screen, seq_node, seq_screen)
            cur_sim, match_seq = self.calculate_seq_trans_prob(original_seq, seq, candidate_model_screens, null_sim)

            if cur_sim > max_score or (cur_sim == max_score and abs(len(match_seq) - 1) <= abs(len(target_seq) - 1)):
                max_score = cur_sim
                target_seq = []
                for elem in match_seq:
                    target_seq.append(elem)

        return max_score, target_seq

    def find_matched_seq_mul_branch(self, begin_screen, interm_update_pre_event_sequences):
        # find all sequences in the extended model that
        # start at begin_screen with length not exceeding self.w
        begin_screen_id = begin_screen.id
        # ExtRep
        scenario_seqs = self.extract_candidate_seqs_base(self.extended_model, begin_screen_id, self.w)
        # # ExtRep-Ext, only use the original branch
        # scenario_seqs = self.extract_original_seqs_base(self.cur_round-1, self.w)

        # load candidate model in updated app
        if self.flag == 0:
            candidate_model = self.tmp_model
        else:

            # TODO: add your own traversal methods here
            # screen -- dict  edge -- list
            tmp_path1 = os.path.join(self.path, "traverse", str(self.cur_round))
            tmp_path2 = "simple_result/candidate_model"
            tmp_path_list2 = tmp_path2.split("/")
            tmp_model_path = os.path.join(tmp_path1, *tmp_path_list2)
            with open(tmp_model_path, 'rb') as f:
                candidate_model = pickle.load(f)

        # extract all candidate sequences
        print("extract all candidate sequences in the updated model ...")
        candidate_seqs = self.extract_candidate_seqs(candidate_model, 1, self.w)

        if self.flag == 0:
            tmp_file_index = 1
            for index in range((len(self.match_detail_info) - 1), -1, -1):
                if self.match_detail_info[index] == 0 and self.match_detail_info[index - 1] == 1:
                    tmp_file_index = index + 1
                    break
            screen_dir = os.path.join(self.path, "traverse", str(tmp_file_index))
        else:
            screen_dir = os.path.join(self.path, "traverse", str(self.cur_round))
        candidate_model_screens = self.preprocess_text(candidate_model, screen_dir)

        # repair
        max_score_mul = 0
        selected_origianl_seq = []
        first_node_match_seq_mul = []
        for original_seq in scenario_seqs:
            original_seq_node = []
            original_seq_screen = []
            for edge in original_seq:
                end_screen = self.extended_screens[edge.end_id - 1]
                original_seq_screen.append(end_screen)
                # tmp_node = self.extended_screens[edge.begin_id - 1].get_node_by_id(edge.node_id)
                # if tmp_node is None:
                edge_bounds = self.extended_edge_to_bounds[edge]
                tmp_node = self.extended_screens[edge.begin_id - 1].get_node_by_bounds(edge_bounds)
                assert tmp_node is not None, "The current edge cannot be recognized."
                original_seq_node.append(tmp_node)

            # similarity between the current branch and the original branch
            branch_sim = self.calculate_branch_sim(original_seq_screen, original_seq)
            # maximum repair similarity for the current branch
            repair_sim, first_node_match_seq_sin = self.find_matched_seq_sin_branch(original_seq, original_seq_node, original_seq_screen, candidate_seqs, candidate_model_screens)
            max_score_sin = repair_sim*branch_sim

            if max_score_sin > max_score_mul or (max_score_sin == max_score_mul and abs(len(first_node_match_seq_sin) - 1) <= abs(len(first_node_match_seq_mul) - 1)):
                max_score_mul = max_score_sin
                first_node_match_seq_mul = []
                for elem in first_node_match_seq_sin:
                    first_node_match_seq_mul.append(elem)

                selected_origianl_seq = []
                for elem in original_seq:
                    selected_origianl_seq.append(elem)

        self.match_detail_info.append(len(first_node_match_seq_mul))
        self.flag = len(first_node_match_seq_mul)
        if self.flag == 0:
            self.tmp_model = candidate_model

        target_seq_bounds = []
        target_seq_info = []
        for seq in first_node_match_seq_mul:
            tmp_node = candidate_model_screens[seq.begin_id - 1].get_node_by_id(seq.node_id)
            tmp_bounds = [tmp_node.loc_x, tmp_node.loc_y, tmp_node.width, tmp_node.height]
            target_seq_bounds.append(tmp_bounds)
            target_seq_info.append(tmp_node.attrib)

        for bounds in target_seq_bounds:
            self.update_pre_event_sequences.append(bounds)

        for pre_target_seq in self.target_seqs:
            for bounds in target_seq_bounds:
                pre_target_seq.append(bounds)

        selected_origianl_seq_end_screens = []
        selected_origianl_seq_edges = []
        selected_origianl_seq_end_screen_ids = []
        for edge in selected_origianl_seq:
            selected_origianl_seq_edges.append(edge)
            end_screen = self.extended_screens[edge.end_id - 1]
            selected_origianl_seq_end_screens.append(end_screen)
            selected_origianl_seq_end_screen_ids.append(end_screen.id)

        # update
        self.screens_no_match.pop(0)
        self.edges_no_match.pop(0)
        while len(self.screens_no_match) > 0:
            ori_next_round_begin_screen = self.screens_no_match[0]
            self.ori_begin_screen_index = 0
            self.ori_begin_edge_index = 0
            match_screen_index = -1
            for i in range(0, len(selected_origianl_seq_end_screens)):
                screen = selected_origianl_seq_end_screens[i]
                if screen.id == ori_next_round_begin_screen.id:
                    match_screen_index = i
                    break

            if match_screen_index != -1:
                if match_screen_index == 0:
                    break
                for i in range(match_screen_index-1, -1, -1):
                    screen = selected_origianl_seq_end_screens[i]
                    self.screens_no_match.insert(0, screen)
                    self.ori_begin_screen_index += 1
                    edge = selected_origianl_seq_edges[i]
                    self.edges_no_match.insert(0, edge)
                    self.ori_begin_edge_index += 1
                break
            else:
                self.screens_no_match.pop(0)
                self.edges_no_match.pop(0)

    def save_work(self):
        result_dir = os.path.join(self.path, 'result')
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        count = 1
        reopen_app(self.package_name)
        for target_seq in self.target_seqs:
            self.cur_screen_id = -1
            self.screen_id = 1

            if len(target_seq) != 0:
                tmp_dir = os.path.join(result_dir, str(count))

                print("replay event sequence from app's main screen to the screen where the test begins")
                if len(self.pre_event_sequences) != 0:
                    event_seq_replay(self.pre_event_sequences, False, "")
                    time.sleep(2)
                count += 1

                screens, edges, record_node_attrib = event_seq_replay(target_seq, True, tmp_dir)
                codes = []
                for i in range(0, len(record_node_attrib)):
                    xml_file_path = os.path.join(tmp_dir, "scenario_screens", str(i+1)+".xml")
                    code = locate_element(record_node_attrib[i], xml_file_path)
                    codes.append(code)
                write_repaired_test_script(codes, tmp_dir, self.caps)

                visual(screens, edges, tmp_dir)

    def work(self):
        print("Read the extended scenario model.")
        current_dir = os.getcwd()
        tmp = "demo/tmpFiles/ext/scenario/extended_result"
        tmp_path_list = tmp.split("/")
        scenario_model_path = os.path.join(current_dir, *tmp_path_list, "simple_result", "extended_model")
        f = open(scenario_model_path, 'rb')
        self.extended_model = pickle.load(f)
        print("Read successful.")

        current_dir = os.getcwd()
        tmp = "demo/tmpFiles/ext/scenario/extended_result"
        tmp_path_list = tmp.split("/")
        screen_dir = os.path.join(current_dir, *tmp_path_list)
        self.extended_screens = self.preprocess_text(self.extended_model, screen_dir)

        self.extended_edges = self.extended_model.edges
        for i in range(0, len(self.extended_edges)):
            edge = self.extended_edges[i]
            edge_bounds = self.extended_edge_bounds[i]
            self.extended_edge_to_bounds[edge] = edge_bounds

        print("------------------self.ori_event_detail--------------------")
        for i in range(0, len(self.ori_edges_order)):
            edge = self.ori_edges_order[i]
            edge_bounds = self.ori_edge_bounds_order[i]
            self.ori_edge_to_bounds[edge] = edge_bounds
            # tmp_node = self.extended_screens[edge.begin_id - 1].get_node_by_id(edge.node_id)
            # if tmp_node is None:
            tmp_node = self.extended_screens[edge.begin_id - 1].get_node_by_bounds(edge_bounds)
            assert tmp_node is not None, "The current edge cannot be recognized."
            self.ori_event_detail.append(str(tmp_node.attrib))
            print(str(tmp_node.attrib))
        print("-----------------------------------------------------------")

        print("Loading the trained word2vec model for subsequent similarity calculations ...")
        tmp = "w2v/w2v-googleplay.model"
        tmp_path_list = tmp.split("/")
        load_path = os.path.join(current_dir, *tmp_path_list)
        try:
            self.wv2_model = word2vec.KeyedVectors.load_word2vec_format(load_path, binary=True)
        except UnicodeDecodeError:
            self.wv2_model = word2vec.KeyedVectors.load(load_path)
        print("Finished loading.")

        for screen in self.ori_screens_order:
            self.screens_no_match.append(screen)
        for edge in self.ori_edges_order:
            self.edges_no_match.append(edge)

        # at least two screens, one start-screen and one end-screen
        while len(self.screens_no_match) > 1:
            self.cur_round += 1
            begin_screen = self.screens_no_match[0]
            print("Current begin screen id: " + str(begin_screen.id))
            print("-----------------------------------------------------------")
            self.find_matched_seq_mul_branch(begin_screen, self.update_pre_event_sequences)

        time.sleep(1)
        self.save_work()

        current_dir = os.getcwd()
        tmp1 = "demo/tmpFiles/rep"
        tmp_path_list1 = tmp1.split("/")
        tmp2 = "/result/1/repaired_script.py"
        tmp_path_list2 = tmp2.split("/")
        recommend_script_path = os.path.join(current_dir, *tmp_path_list1, *tmp_path_list2)
        shutil.copy(recommend_script_path, self.result_save_path)




