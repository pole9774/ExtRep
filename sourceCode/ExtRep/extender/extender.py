import os
import pickle
import shutil

from backend.screen import Screen, is_same_screen
from backend.edge import Edge
from backend.model import GUIModel
from backend.visualize import VisualTool
from scripting.collector import script_replay, event_seq_replay
from utils.operate_current_device import close_app, open_app


class Extender:
    def __init__(self, package_name, locators, w):

        current_dir = os.getcwd()
        tmp = "demo/tmpFiles/ext/scenario"
        tmp_path_list = tmp.split("/")
        self.path = os.path.join(current_dir, *tmp_path_list)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.package_name = package_name

        # TODO: coordinate sequence of events from app's main screen to the screen where the test begins
        # if so, add it manually
        self.pre_base_event_sequences = []
        self.base_event_sequences = []
        self.locators = locators

        self.depth = w

        self.base_scenario_model = None
        self.base_screens = []
        self.base_edges = []

        self.auto_part_traversal_model = []

        self.extended_model = None
        self.extended_screens = {}
        self.extended_edges = []
        # 新加
        self.extended_edge_bounds = []
        self.extended_screen_id = 1
        self.extended_cur_begin_screen_id = -1
        self.extended_cur_end_screen_id = -1

        self.ori_screens_order = []
        self.ori_edges_order = []
        # 新加
        self.ori_edge_bounds_order = []


    def save_extended_model_screen(self, cur_screen, cur_screens_dir):
        """
        save extended model screen
        :param cur_screen:
        :param cur_screens_dir:
        :return:
        """

        cur_screen_nodes = cur_screen.nodes
        cur_screen_act_name = cur_screen.act_name
        extended_model_screen = Screen(cur_screen_nodes, self.extended_screen_id, cur_screen_act_name)

        cur_screen_id = cur_screen.id
        cur_screen_dir = os.path.join(cur_screens_dir, str(cur_screen_act_name) + '-' + str(cur_screen_id))
        extended_screen_save_dir = os.path.join(self.path, 'extended_result', str(cur_screen_act_name) + '-' + str(extended_model_screen.id))
        shutil.copytree(cur_screen_dir, extended_screen_save_dir)
        extended_model_screen.shot_dir = os.path.join(extended_screen_save_dir, '1.png')

        self.extended_screens[self.extended_screen_id] = extended_model_screen
        self.extended_screen_id += 1

        return extended_model_screen

    def update_screen(self, old_screen_dir, new_screen_dir):
        old_xml_path = os.path.join(old_screen_dir, "1.xml")
        old_png_path = os.path.join(old_screen_dir, "1.png")
        new_xml_path = os.path.join(new_screen_dir, "1.xml")
        new_png_path = os.path.join(new_screen_dir, "1.png")

        if os.path.exists(old_xml_path):
            os.remove(old_xml_path)
        if os.path.exists(old_png_path):
            os.remove(old_png_path)

        shutil.copy2(new_xml_path, old_screen_dir)
        shutil.copy2(new_png_path, old_screen_dir)

    def save_extended_model_edge(self, begin_id, end_id, node_id, cur_node_bounds):
        """
        save extended model edge
        :param begin_id: begin screen id
        :param end_id: end screen id
        :param node_id: edge node id
        :return:
        """

        cur_edge = Edge(begin_id, end_id, node_id)

        self.extended_edges.append(cur_edge)
        self.extended_edge_bounds.append(cur_node_bounds)

        return cur_edge

    def find_screen_id_in_screen_list(self, screen, screen_list):
        """
        given a screen, find its id in the screen list
        :param screen: the screen to look for
        :param screen_list: model's screens
        :return: screen id
        """
        for model_screen in screen_list:
            if is_same_screen(screen, model_screen, 0.9):
                return model_screen.id

        return -1

    def find_screen_id_in_screen_dict(self, screen, screen_dict):
        """
        given a screen, find its id in the screen dict
        :param screen: the screen to look for
        :param screen_dict: model's screens
        :return: screen id
        """
        for model_screen in screen_dict.values():
            if is_same_screen(screen, model_screen, 0.9):
                return model_screen.id

        return -1

    def has_existed_edge(self, begin_id, end_id, bounds, screen_dict, edges):
        for edge in edges:
            if edge.begin_id == begin_id and edge.end_id == end_id:
                node = screen_dict[edge.begin_id].get_node_by_id(edge.node_id)
                if node.loc_x == bounds[0] and node.loc_y == bounds[1] and node.width == bounds[2] and node.height == bounds[3]:
                    return True

        return False

    def find_edge(self, begin_id, end_id, bounds, screen_dict, edges):
        for edge in edges:
            if edge.begin_id == begin_id and edge.end_id == end_id:
                node = screen_dict[edge.begin_id].get_node_by_id(edge.node_id)
                if node.loc_x == bounds[0] and node.loc_y == bounds[1] and node.width == bounds[2] and node.height == bounds[3]:
                    return edge

        return None

    def extract_extend_seqs(self, end_screen_ids, model_screens, model_edges, ori_node_bounds):
        """
        extract all acyclic sequences of length up to w from the given candidate model edges
        the begin screen id of these sequences must be 1
        the end screen id of these sequences must in end_screen_ids
        filter out the original edge based on ori_node_bounds
        """

        candidate_seqs_dict = {}
        res_seqs_dict = {}

        for i in range(0, self.depth):
            length = i + 1
            tmp_candidate_seqs = []

            if length == 1:
                for edge in model_edges:
                    if edge.begin_id == 1:
                        tmp_seq = []
                        tmp_seq.append(edge)
                        tmp_candidate_seqs.append(tmp_seq)
            else:
                for pre_seq in candidate_seqs_dict[length - 1]:
                    screen_ids = []
                    screen_ids.append(1)
                    for edge in pre_seq:
                        screen_ids.append(edge.end_id)

                    for edge in model_edges:
                        if edge.begin_id == screen_ids[-1] and (edge.end_id not in screen_ids):
                            tmp_seq = []
                            tmp_seq.extend(pre_seq)
                            tmp_seq.append(edge)
                            tmp_candidate_seqs.append(tmp_seq)

            candidate_seqs_dict[length] = tmp_candidate_seqs

        for length in range(1, len(candidate_seqs_dict)+1):
            tmp_res_seqs = []
            for seq in candidate_seqs_dict[length]:
                # filter out the original edge
                if length == 1:
                    cur_edge = seq[0]
                    cur_node = model_screens[cur_edge.begin_id - 1].get_node_by_id(cur_edge.node_id)
                    if cur_node.loc_x == ori_node_bounds[0] and cur_node.loc_y == ori_node_bounds[1] and \
                        cur_node.width == ori_node_bounds[2] and cur_node.height == ori_node_bounds[3]:
                        continue

                last_edge = seq[-1]
                if last_edge.end_id in end_screen_ids:
                    tmp_res_seqs.append(seq)

            res_seqs_dict[length] = tmp_res_seqs

        return res_seqs_dict

    def auto_path_extend(self, auto_path_id):
        """
        current round: auto_path_id + 1
        """
        pre_event_sequences = []

        for i in range(0, len(self.pre_base_event_sequences)):
            pre_event_sequences.append(self.pre_base_event_sequences[i])

        for i in range(0, auto_path_id):
            pre_event_sequences.append(self.base_event_sequences[i])

        # TODO: add your own traversal methods here
        # screen -- dict  edge -- list
        # read model
        current_dir = os.getcwd()
        tmp1 = "demo/tmpFiles/ext/traverse"
        tmp_path_list1 = tmp1.split("/")
        tmp2 = "simple_result/candidate_model"
        tmp_path_list2 = tmp2.split("/")
        tmp_path = os.path.join(current_dir, *tmp_path_list1, str(auto_path_id + 1), *tmp_path_list2)
        f = open(tmp_path, 'rb')
        part_traversal_model = pickle.load(f)

        self.auto_part_traversal_model.append(part_traversal_model)

        part_traversal_model_screens = []
        for key in part_traversal_model.screens:
            screen = part_traversal_model.screens[key]
            part_traversal_model_screens.append(screen)

        part_traversal_model_edges = part_traversal_model.edges

        cur_end_screen_id = -1
        cur_node_id = -1
        end_screen_ids = []

        cur_node_bounds = self.base_event_sequences[auto_path_id]

        # find cur_end_screen_id, cur_node_id
        for edge in part_traversal_model_edges:
            if edge.begin_id == 1:
                tmp_node = part_traversal_model_screens[edge.begin_id - 1].get_node_by_id(edge.node_id)
                if tmp_node.loc_x == cur_node_bounds[0] and tmp_node.loc_y == cur_node_bounds[1] and \
                        tmp_node.width == cur_node_bounds[2] and tmp_node.height == cur_node_bounds[3]:
                    cur_end_screen_id = edge.end_id
                    cur_node_id = edge.node_id

        if cur_end_screen_id == -1:
            end_screen_in_base = self.base_screens[auto_path_id + 1]
            cur_end_screen_id = self.find_screen_id_in_screen_list(end_screen_in_base, part_traversal_model_screens)

        cur_screens_dir = os.path.join(current_dir, *tmp_path_list1, str(auto_path_id + 1))
        cur_begin_screen = part_traversal_model_screens[0]

        if auto_path_id == 0:
            ori_screen = self.save_extended_model_screen(cur_begin_screen, cur_screens_dir)
            self.ori_screens_order.append(ori_screen)
        else:
            # updated begin screen
            old_screen = self.ori_screens_order[-1]
            old_screen_dir = os.path.join(self.path, 'extended_result', str(old_screen.act_name) + '-' + str(old_screen.id))
            new_screen_dir = os.path.join(cur_screens_dir, str(cur_begin_screen.act_name) + '-' + str(cur_begin_screen.id))
            self.update_screen(old_screen_dir, new_screen_dir)
            old_screen.nodes = cur_begin_screen.nodes

        cur_end_screen = part_traversal_model_screens[cur_end_screen_id - 1]
        extended_cur_begin_screen_id = self.find_screen_id_in_screen_dict(cur_begin_screen, self.extended_screens)
        tmp_extended_cur_end_screen_id = self.find_screen_id_in_screen_dict(cur_end_screen, self.extended_screens)
        if tmp_extended_cur_end_screen_id == -1:
            saved_screen = self.save_extended_model_screen(cur_end_screen, cur_screens_dir)
            tmp_extended_cur_end_screen_id = saved_screen.id
        extended_cur_end_screen_id = tmp_extended_cur_end_screen_id
        self.extended_cur_begin_screen_id = extended_cur_begin_screen_id
        self.extended_cur_end_screen_id = extended_cur_end_screen_id
        self.ori_screens_order.append(self.extended_screens[self.extended_cur_end_screen_id])

        if self.has_existed_edge(self.extended_cur_begin_screen_id, self.extended_cur_end_screen_id, cur_node_bounds, self.extended_screens, self.extended_edges) is False:
            ori_edge = self.save_extended_model_edge(self.extended_cur_begin_screen_id, self.extended_cur_end_screen_id, cur_node_id, cur_node_bounds)
            self.extended_screens[self.extended_cur_begin_screen_id].des.append(self.extended_cur_end_screen_id)
        else:
            ori_edge = self.find_edge(self.extended_cur_begin_screen_id, self.extended_cur_end_screen_id, cur_node_bounds, self.extended_screens, self.extended_edges)
        self.ori_edges_order.append(ori_edge)
        self.ori_edge_bounds_order.append(cur_node_bounds)

        # finds the screen ids in the current model that is less than or equal to depth-1 screens
        # after the cur_end_screen
        end_screen_ids.append(cur_end_screen_id)
        if (auto_path_id + 1) <= len(self.base_screens) - self.depth:
            for i in range(auto_path_id+2, auto_path_id+self.depth+1):
                cur_screen = self.base_screens[i]
                cur_screen_id = self.find_screen_id_in_screen_list(cur_screen, part_traversal_model_screens)
                if cur_screen_id != -1:
                    end_screen_ids.append(cur_screen_id)

        tmp_res_seqs_dict = self.extract_extend_seqs(end_screen_ids, part_traversal_model_screens, part_traversal_model_edges, cur_node_bounds)
        res_seqs_list = []
        res_seqs_list.extend(tmp_res_seqs_dict[1])

        # further removing the loops
        # the screen reached by the edge has appeared in self.base_screens[:auto_path_id]
        for length in range(2, len(tmp_res_seqs_dict) + 1):
            for seq in tmp_res_seqs_dict[length]:
                seq_screens = []
                for edge in seq:
                    if edge.begin_id != 1:
                        seq_screens.append(part_traversal_model_screens[edge.begin_id - 1])
                    if edge.end_id != cur_end_screen_id:
                        seq_screens.append(part_traversal_model_screens[edge.end_id - 1])
                has_loop = False
                for seq_screen in seq_screens:
                    for ori_screen in self.base_screens[:auto_path_id]:
                        if is_same_screen(seq_screen, ori_screen, 0.9):
                            has_loop = True
                            break
                if has_loop is False:
                    res_seqs_list.append(seq)

        # screen_mapping_dict -- cur_model_screen_id : extended_model_screen_id
        screen_mapping_dict = {}
        screen_mapping_dict[1] = self.extended_cur_begin_screen_id
        screen_mapping_dict[cur_end_screen_id] = self.extended_cur_end_screen_id
        for seq in res_seqs_list:
            for edge in seq:
                mapped_begin_id = -1
                mapped_end_id = -1
                mapped_node_id = edge.node_id
                tmp_node = part_traversal_model_screens[edge.begin_id - 1].get_node_by_id(edge.node_id)
                mapped_node_bounds = [tmp_node.loc_x, tmp_node.loc_y, tmp_node.width, tmp_node.height]

                # save new screen
                if edge.begin_id in screen_mapping_dict.keys() and edge.end_id in screen_mapping_dict.keys():
                    mapped_begin_id = screen_mapping_dict[edge.begin_id]
                    mapped_end_id = screen_mapping_dict[edge.end_id]
                elif edge.begin_id in screen_mapping_dict.keys() and edge.end_id not in screen_mapping_dict.keys():
                    mapped_begin_id = screen_mapping_dict[edge.begin_id]

                    tmp_new_screen = part_traversal_model_screens[edge.end_id - 1]
                    mapped_end_id = self.find_screen_id_in_screen_dict(tmp_new_screen, self.extended_screens)
                    if mapped_end_id == -1:
                        new_screen = tmp_new_screen
                        saved_screen = self.save_extended_model_screen(new_screen, cur_screens_dir)
                        mapped_end_id = saved_screen.id
                    screen_mapping_dict[edge.end_id] = mapped_end_id
                elif edge.begin_id not in screen_mapping_dict.keys() and edge.end_id in screen_mapping_dict.keys():
                    mapped_end_id = screen_mapping_dict[edge.end_id]

                    tmp_new_screen = part_traversal_model_screens[edge.begin_id - 1]
                    mapped_begin_id = (self.find_screen_id_in_screen_dict(tmp_new_screen, self.extended_screens)).id
                    if mapped_begin_id == -1:
                        new_screen = tmp_new_screen
                        saved_screen = self.save_extended_model_screen(new_screen, cur_screens_dir)
                        mapped_begin_id = saved_screen.id
                    screen_mapping_dict[edge.begin_id] = mapped_begin_id
                else:
                    tmp_new_begin_screen = part_traversal_model_screens[edge.begin_id - 1]
                    tmp_new_end_screen = part_traversal_model_screens[edge.end_id - 1]
                    mapped_begin_id = self.find_screen_id_in_screen_dict(tmp_new_begin_screen, self.extended_screens)
                    mapped_end_id = self.find_screen_id_in_screen_dict(tmp_new_end_screen, self.extended_screens)

                    if mapped_begin_id == -1:
                        new_screen = tmp_new_begin_screen
                        saved_screen = self.save_extended_model_screen(new_screen, cur_screens_dir)
                        mapped_begin_id = saved_screen.id
                    if mapped_end_id == -1:
                        new_screen = tmp_new_begin_screen
                        saved_screen = self.save_extended_model_screen(new_screen, cur_screens_dir)
                        mapped_end_id = saved_screen.id
                    screen_mapping_dict[edge.begin_id] = mapped_begin_id
                    screen_mapping_dict[edge.begin_id] = mapped_end_id

                # save new edge
                if self.has_existed_edge(mapped_begin_id, mapped_end_id, mapped_node_bounds, self.extended_screens, self.extended_edges) is False:
                    self.save_extended_model_edge(mapped_begin_id, mapped_end_id, mapped_node_id, mapped_node_bounds)
                    if mapped_end_id not in self.extended_screens[mapped_begin_id].des:
                        self.extended_screens[mapped_begin_id].des.append(mapped_end_id)
        print("screen_mapping_dict:")
        print(screen_mapping_dict)

    def full_path_extend(self):
        # for key in self.base_scenario_model.screens:
        #     screen = self.base_scenario_model.screens[key]
        #     self.base_screens.append(screen)
        #
        # self.base_edges = self.base_scenario_model.edges

        print("the total number of rounds extended: " + str(len(self.base_edges)))
        for auto_path_id in range(0, len(self.base_edges)):
            print("current round: " + str(auto_path_id + 1))
            self.auto_path_extend(auto_path_id)
            print("end of current round")

    def work(self):
        # # If there is a preorder sequence, add the sequence manually and run the code commented below
        # print("Replay event sequence from app's main screen to the screen where the test begins.")
        # event_seq_replay(self.pre_base_event_sequences, False, "")
        # print("Replay successful.")
        #
        # print("Replay base event sequences.")
        # original_branch_save_dir = os.path.join(self.path, 'original_branch')
        # if not os.path.exists(original_branch_save_dir):
        #     os.makedirs(original_branch_save_dir)
        # self.base_event_sequences, self.base_scenario_model = script_replay(self.locators, original_branch_save_dir)
        # print("Replay successful.")
        #
        # print("Extend the basic test script.")
        # close_app(self.package_name)
        # open_app(self.package_name)
        # event_seq_replay(self.pre_base_event_sequences, False, "")

        print("Read the base scenario model.")
        current_dir = os.getcwd()
        tmp = "demo/tmpFiles/ext/scenario/original_branch"
        tmp_path_list = tmp.split("/")
        scenario_model_path = os.path.join(current_dir, *tmp_path_list, "scenario_model")
        f = open(scenario_model_path, 'rb')
        self.base_scenario_model = pickle.load(f)
        print("Read successful.")

        for key in self.base_scenario_model.screens:
            screen = self.base_scenario_model.screens[key]
            self.base_screens.append(screen)

        self.base_edges = self.base_scenario_model.edges
        for edge in self.base_edges:
            node = self.base_screens[edge.begin_id - 1].get_node_by_id(edge.node_id)
            bound = [node.loc_x, node.loc_y, node.width, node.height]
            self.base_event_sequences.append(bound)
        print(self.base_event_sequences)

        self.full_path_extend()

        model_save_dir = os.path.join(self.path, 'extended_result', 'simple_result')
        if not os.path.exists(model_save_dir):
            os.makedirs(model_save_dir)
        self.extended_model = GUIModel(self.extended_screens, self.extended_edges)
        model = pickle.dumps(self.extended_model)
        with open(os.path.join(model_save_dir, 'extended_model'), 'wb') as f:
            f.write(model)

        ori_screen_ids_order = []
        for screen in self.ori_screens_order:
            ori_screen_ids_order.append(screen.id)
        visual_obj = VisualTool(self.extended_screens, self.extended_edges, self.extended_edge_bounds, model_save_dir, ori_screen_ids_order, self.ori_edge_bounds_order)
        visual_obj.save_work()

        return self.extended_model, self.extended_edge_bounds, self.ori_screens_order, self.ori_edges_order, self.ori_edge_bounds_order
