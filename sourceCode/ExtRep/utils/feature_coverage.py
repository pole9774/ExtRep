import pickle

from backend.screen import is_same_screen


def find_same_screen(ori_screen, screens):
    for screen in screens:
        if is_same_screen(ori_screen, screen, 0.9):
            return screen
    print("---------------------------")
    print(ori_screen.id)
    print(ori_screen.nodes)
    print("---------------------------")
    for screen in screens:
        print(screen.id)
        print(screen.nodes)
        print(is_same_screen(ori_screen, screen, 0.9))
    print("---------------------------")
    return None


def find_same_edge(ori_edge, edges, ori_path_screens, cur_path_screens, screens_mapping_dict):
    ori_edge_begin_screen = ori_path_screens[ori_edge.begin_id]
    ori_edge_end_screen = ori_path_screens[ori_edge.end_id]

    if ori_edge_begin_screen in screens_mapping_dict.keys() and ori_edge_end_screen in screens_mapping_dict.keys():
        ori_edge_node = ori_edge_begin_screen.get_node_by_id(ori_edge.node_id)
        # ori_edge_bounds = [ori_edge_node.loc_x, ori_edge_node.loc_y, ori_edge_node.width, ori_edge_node.height]
        mapping_begin_screen = screens_mapping_dict[ori_edge_begin_screen]
        mapping_end_screen = screens_mapping_dict[ori_edge_end_screen]

        for edge in edges:
            edge_begin_screen = cur_path_screens[edge.begin_id]
            edge_end_screen = cur_path_screens[edge.end_id]
            if edge_begin_screen == mapping_begin_screen and edge_end_screen == mapping_end_screen:
                cur_edge_node = edge_begin_screen.get_node_by_id(edge.node_id)
                # cur_edge_bounds = [cur_edge_node.loc_x, cur_edge_node.loc_y, cur_edge_node.width, cur_edge_node.height]
                if ori_edge_node.attrib == cur_edge_node.attrib:
                    return edge
    else:
        return None


def calculate_feature_coverage(ori_path_model, cur_path_model):
    ori_path_screens = ori_path_model.screens
    ori_path_edges = ori_path_model.edges

    cur_path_screens = cur_path_model.screens
    screens_no_match = []
    for screen in cur_path_screens.values():
        screens_no_match.append(screen)
    cur_path_edges = cur_path_model.edges
    edges_no_match = []
    for edge in cur_path_edges:
        edges_no_match.append(edge)

    # screens_mapping_dict -- ori_path_screen : cur_path_screen
    screens_mapping_dict = {}
    screen_coverage_num = 0
    for screen in ori_path_screens.values():
        screen_matched = find_same_screen(screen, screens_no_match)
        if screen_matched is not None:
            screen_coverage_num += 1
            screens_mapping_dict[screen] = screen_matched
            screens_no_match.remove(screen_matched)
    # screen_len = len(ori_path_screens) - 1
    # max
    screen_len = max(len(ori_path_screens), len(cur_path_screens)) - 1
    if screen_coverage_num != 0:
        screen_coverage = (screen_coverage_num - 1) / screen_len
    else:
        screen_coverage = 0

    edge_coverage_num = 0
    for edge in ori_path_edges:
        edge_matched = find_same_edge(edge, edges_no_match, ori_path_screens, cur_path_screens, screens_mapping_dict)
        if edge_matched is not None:
            edge_coverage_num += 1
            edges_no_match.remove(edge_matched)
    # edge_len = len(ori_path_edges)
    # max
    edge_len = max(len(ori_path_edges), len(cur_path_edges))
    edge_coverage = edge_coverage_num / edge_len

    # print important information
    screens_id_mapping_dict = {}
    for key, value in screens_mapping_dict.items():
        screens_id_mapping_dict[key.id] = value.id
    print("screens_id_mapping_dict = " + str(screens_id_mapping_dict))
    print("screen_coverage = " + str(screen_coverage))
    print("edge_coverage = " + str(edge_coverage))

    feature_coverage = (screen_coverage + edge_coverage) / 2
    return feature_coverage


if __name__ == '__main__':
    print("Read the original scenario model.")
    ori_path_model_path = "D://lab//ExtRep//newAdd//featureCoverage//exploreStudy//test-25-Snotepad-13//scenario//original_path//scenario_model"
    f = open(ori_path_model_path, 'rb')
    ori_path_model = pickle.load(f)
    print("Read successful.")

    print("Read the current scenario model.")
    cur_path_model_path = "D://lab//ExtRep//newAdd//featureCoverage//exploreStudy//test-25-Snotepad-13//scenario//branch_min_same//scenario_model"
    f = open(cur_path_model_path, 'rb')
    cur_path_model = pickle.load(f)
    print("Read successful.")

    FC = calculate_feature_coverage(ori_path_model, cur_path_model)
    print("feature_coverage = " + str(FC))
