import os
import pickle
import sys
import time
import warnings
import cv2

from backend.edge import Edge
from backend.model import GUIModel
from backend.screen import Screen
from utils.get_current_device_info import save_screen, get_cur_screen_info, get_tmp_screen, has_same_screen
from utils.logging import init_logger
from utils.operate_current_device import action_click

logger_number = 1


def read_test_scripts(script_path):

    locators = []
    caps = {}
    code_line = []
    tmp_caps = ['platformName', 'platformVersion', 'deviceName', 'appPackage', 'appActivity',
                'newCommandTimeout', 'noReset', 'webdriver.Remote']

    with open(script_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.strip() != '' and line.strip()[0] != '#':
                el = []

                line = line.strip().split('#')[0]
                line = line.rstrip()

                if 'platformName' in tmp_caps and 'platformName' in line:
                    caps['platformName'] = line
                    tmp_caps.remove('platformName')
                    continue
                if 'platformVersion' in tmp_caps and 'platformVersion' in line:
                    caps['platformVersion'] = line
                    tmp_caps.remove('platformVersion')
                    continue
                if 'deviceName' in tmp_caps and 'deviceName' in line:
                    caps['deviceName'] = line
                    tmp_caps.remove('deviceName')
                    continue
                if 'appPackage' in tmp_caps and 'appPackage' in line:
                    caps['appPackage'] = line
                    tmp_caps.remove('appPackage')
                    continue
                if 'appActivity' in tmp_caps and 'appActivity' in line:
                    caps['appActivity'] = line
                    tmp_caps.remove('appActivity')
                    continue
                if 'newCommandTimeout' in tmp_caps and 'newCommandTimeout' in line:
                    caps['newCommandTimeout'] = line
                    tmp_caps.remove('newCommandTimeout')
                    continue
                if 'noReset' in tmp_caps and 'noReset' in line:
                    caps['noReset'] = line
                    tmp_caps.remove('noReset')
                    continue
                if 'webdriver.Remote' in tmp_caps and 'webdriver.Remote' in line:
                    caps['webdriver.Remote'] = line
                    tmp_caps.remove('webdriver.Remote')
                    continue

                if 'find_element' in line:
                    el_type = ''
                    el_info = ''
                    el_num = -1
                    if 'find_element_by_android_uiautomator' in line:
                        el_type = 'text'
                        tmp_info = line.strip().split('text(', 1)[1]
                        el_info = tmp_info[1:-4]
                    else:
                        if 'find_element_by_id' in line:
                            el_type = 'resource-id'
                            el_num = 0
                        if 'find_elements_by_id' in line:
                            el_type = 'resource-id'
                        elif 'find_elements_by_class_name' in line:
                            el_type = 'class'
                        elif 'find_element_by_accessibility_id' in line:
                            el_type = 'content-desc'

                        tmp_info = line.strip().split('(', 1)[1]

                        if tmp_info[-1] == ')':
                            el_info = tmp_info[1:-2]

                        if tmp_info[-1] == ']':
                            index = -2
                            while True:
                                if tmp_info[index] != '[':
                                    index -= 1
                                else:
                                    index += 1
                                    break
                            el_num = int(tmp_info[index: -1])
                            el_info = tmp_info[1: (index-3)]

                    el.append(el_type)
                    el.append(el_info)
                    el.append(el_num)

                if el != []:
                    locators.append(el)
                    code_line.append(line)
                    continue

                if 'tap' in line:
                    el.append('bound')
                    tmp_info = line.strip().split('[', 1)[1]
                    el_locx = tmp_info.strip().split(',', 1)[0][1:]
                    el.append(int(el_locx))
                    el_locy = tmp_info.strip().split(',', 1)[1][:-3]
                    el.append(int(el_locy))

                if el != []:
                    locators.append(el)
                    code_line.append(line)

    if len(tmp_caps) != 0:
        warnings.warn("The following information is required to connect to Appium: ")
        warnings.warn("--------------------")
        for elem in tmp_caps:
            if elem == 'webdriver.Remote':
                warnings.warn('webdriver')
            else:
                warnings.warn(elem)
        warnings.warn("--------------------")

    return locators, caps, code_line


def visual(screens, edges, save_path):
    screen_save_path = os.path.join(save_path, "scenario_screens")

    e_count = 1
    for edge in edges:
        screen = screens[edge.begin_id]
        clicked_node = screen.get_node_by_id(edge.node_id)

        img_path = os.path.join(screen_save_path, str(screen.id) + '.png')
        img = cv2.imread(img_path)
        x1, y1, x2, y2 = clicked_node.parse_bounds()
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

        cv2.imwrite(os.path.join(save_path, 'action' + str(e_count) + '.png'), img)
        e_count += 1

    edge = edges[-1]
    screen = screens[edge.end_id]
    img_path = os.path.join(screen_save_path, str(screen.id) + '.png')
    img = cv2.imread(img_path)
    cv2.imwrite(os.path.join(save_path, 'destination.png'), img)


def script_replay(locators, save_path):
    distinct_rate = 0.9
    screen_id = 1
    cur_screen_id = -1

    screens = {}
    edges = []

    base_event_sequences = []

    clicked_node = None
    screen_save_path = os.path.join(save_path, "scenario_screens")
    no_found_flag = False
    for locator in locators:

        if cur_screen_id == -1:
            nodes, act_name = get_cur_screen_info()
            screen = Screen(nodes, screen_id, act_name)

            cur_screen_id = screen.id

            screens[cur_screen_id] = screen
            screen_id += 1
            save_screen(screen, screen_save_path)

            # bound
            if locator[0] == 'bound':
                for node in screen.nodes:
                    if not node.children:
                        if locator[1] == node.loc_x and locator[2] == node.loc_y and \
                                'Group' not in node.attrib['class']:
                            clicked_node = node
                            break
            # resource-id and class
            elif locator[0] == 'resource-id' or locator[0] == 'class':
                node_type_count = -1
                for node in screen.nodes:
                    if node.attrib[locator[0]] == locator[1]:
                        node_type_count += 1
                    if node_type_count == locator[2]:
                        clicked_node = node
                        break
            # text and content-desc
            else:
                for node in screen.nodes:
                    node_str = node.attrib[locator[0]].replace(" ", "").lower()
                    ori_str = locator[1].replace(" ", "").lower()
                    if node_str == ori_str:
                        clicked_node = node
                        break

            if clicked_node is None:
                print(locator)
                print('Unable to find the currently clicked element, the test script replay failed.')
                no_found_flag = True
                break
                # sys.exit()

            bound = [clicked_node.loc_x, clicked_node.loc_y, clicked_node.width, clicked_node.height]
            base_event_sequences.append(bound)

            action_click(clicked_node)
            time.sleep(1)

        else:
            tmp_screen = get_tmp_screen()
            exist_screen_id = has_same_screen(screens, tmp_screen, distinct_rate)
            if exist_screen_id == cur_screen_id:
                print('screen does not transfer')

            tmp_screen.id = screen_id

            screens[tmp_screen.id] = tmp_screen
            screen_id += 1
            save_screen(tmp_screen, screen_save_path)

            edge = Edge(cur_screen_id, tmp_screen.id, clicked_node.idx)
            edges.append(edge)
            screens[cur_screen_id].des.append(tmp_screen.id)
            cur_screen_id = tmp_screen.id

            clicked_node = None

            # bound
            if locator[0] == 'bound':
                for node in tmp_screen.nodes:
                    if not node.children:
                        if locator[1] == node.loc_x and locator[2] == node.loc_y and \
                                'Group' not in node.attrib['class']:
                            clicked_node = node
                            break
            # resource-id and class
            elif locator[0] == 'resource-id' or locator[0] == 'class':
                node_type_count = -1
                for node in tmp_screen.nodes:
                    if node.attrib[locator[0]] == locator[1]:
                        node_type_count += 1
                    if node_type_count == locator[2]:
                        clicked_node = node
                        break
            # text and content-desc
            else:
                for node in tmp_screen.nodes:
                    node_str = node.attrib[locator[0]].replace(" ", "").lower()
                    ori_str = locator[1].replace(" ", "").lower()
                    if node_str == ori_str:
                        clicked_node = node
                        break

            if clicked_node is None:
                print(locator)
                print('Unable to find the currently clicked element, the test script replay failed.')
                no_found_flag = True
                break
                # sys.exit()

            bound = [clicked_node.loc_x, clicked_node.loc_y, clicked_node.width, clicked_node.height]
            base_event_sequences.append(bound)

            action_click(clicked_node)
            time.sleep(1)

    if no_found_flag is not True:
        tmp_screen = get_tmp_screen()
        exist_screen_id = has_same_screen(screens, tmp_screen, distinct_rate)
        if exist_screen_id == cur_screen_id:
            print('screen does not transfer')

        tmp_screen.id = screen_id

        screens[tmp_screen.id] = tmp_screen
        screen_id += 1
        save_screen(tmp_screen, screen_save_path)

        edge = Edge(cur_screen_id, tmp_screen.id, clicked_node.idx)
        edges.append(edge)
        screens[cur_screen_id].des.append(tmp_screen.id)

    print('edge')
    for edge in edges:
        print('---')
        print('begin')
        print(edge.begin_id)
        print('end')
        print(edge.end_id)
        print('node')
        print(edge.node_id)
        print('---')

    print('screen')
    for key in screens:
        screen = screens[key]
        s = ''
        for node in screen.nodes:
            if node.attrib['text'] != '':
                s += node.attrib['text']
        print(screen.id)
        print(s)
        print('-------------')

    # save model
    scenario_model = GUIModel(screens, edges)
    model = pickle.dumps(scenario_model)
    with open(os.path.join(save_path, 'scenario_model'), 'wb') as f:
        f.write(model)

    visual(screens, edges, save_path)

    return base_event_sequences, scenario_model


def event_seq_replay(event_seqs, save_flag, save_path):
    distinct_rate = 0.9
    if len(event_seqs) == 0:
        return

    screen_id = 1
    cur_screen_id = -1

    screens = {}
    edges = []
    record_info = []
    record_node_attrib = []

    clicked_node = None
    screen_save_path = os.path.join(save_path, "scenario_screens")
    for pos in event_seqs:

        if cur_screen_id == -1:
            nodes, act_name = get_cur_screen_info()
            screen = Screen(nodes, screen_id, act_name)

            cur_screen_id = screen.id

            screens[cur_screen_id] = screen
            screen_id += 1
            if save_flag is True:
                save_screen(screen, screen_save_path)

            for node in screen.nodes:
                if not node.children:
                    if pos[0] == node.loc_x and pos[1] == node.loc_y and \
                        pos[2] == node.width and pos[3] == node.height and \
                            'Group' not in node.attrib['class']:
                        clicked_node = node
                        break

            if clicked_node is None:
                print(pos)
                print('Unable to find the currently clicked element, the test script replay failed.')
                return

            if save_flag is True:
                record_node_attrib.append(clicked_node.attrib)
                clicked_node_str = str(clicked_node.attrib)
                record_info.append(clicked_node_str)

            action_click(clicked_node)
            time.sleep(1)

        else:
            tmp_screen = get_tmp_screen()
            exist_screen_id = has_same_screen(screens, tmp_screen, distinct_rate)
            if exist_screen_id == cur_screen_id:
                print('screen does not transfer')

            tmp_screen.id = screen_id

            screens[tmp_screen.id] = tmp_screen
            screen_id += 1
            if save_flag is True:
                save_screen(tmp_screen, screen_save_path)

            edge = Edge(cur_screen_id, tmp_screen.id, clicked_node.idx)
            edges.append(edge)
            screens[cur_screen_id].des.append(tmp_screen.id)
            cur_screen_id = tmp_screen.id

            clicked_node = None
            for node in tmp_screen.nodes:
                if not node.children:
                    if pos[0] == node.loc_x and pos[1] == node.loc_y and \
                        pos[2] == node.width and pos[3] == node.height and \
                            'Group' not in node.attrib['class']:
                        clicked_node = node
                        break

            if clicked_node is None:
                print(pos)
                print('Unable to find the currently clicked element, the test script replay failed.')
                return

            if save_flag is True:
                record_node_attrib.append(clicked_node.attrib)
                clicked_node_str = str(clicked_node.attrib)
                record_info.append(clicked_node_str)

            action_click(clicked_node)
            time.sleep(1)

    tmp_screen = get_tmp_screen()
    exist_screen_id = has_same_screen(screens, tmp_screen, distinct_rate)
    if exist_screen_id == cur_screen_id:
        print('screen does not transfer')

    tmp_screen.id = screen_id

    screens[tmp_screen.id] = tmp_screen
    screen_id += 1
    if save_flag is True:
        save_screen(tmp_screen, screen_save_path)

    edge = Edge(cur_screen_id, tmp_screen.id, clicked_node.idx)
    edges.append(edge)
    screens[cur_screen_id].des.append(tmp_screen.id)

    print('edge')
    for edge in edges:
        print('---')
        print('begin')
        print(edge.begin_id)
        print('end')
        print(edge.end_id)
        print('node')
        print(edge.node_id)
        print('---')

    print('screen')
    for key in screens:
        screen = screens[key]
        s = ''
        for node in screen.nodes:
            if node.attrib['text'] != '':
                s += node.attrib['text']
        print(screen.id)
        print(s)
        print('-------------')

    if save_flag is True:
        scenario_model = GUIModel(screens, edges)
        model = pickle.dumps(scenario_model)
        with open(os.path.join(save_path, 'scenario_model'), 'wb') as f:
            f.write(model)

        visual(screens, edges, save_path)

        global logger_number
        logger_number += 1
        logger_name = "logger" + str(logger_number)
        record_path = os.path.join(save_path, 'detail_info.txt')
        if not os.path.exists(record_path):
            with open(record_path, 'w'):
                pass
        logger = init_logger(logger_name, record_path)
        for i in range(0, len(record_info)):
            event_str = 'event' + str(i+1) + ': ' + record_info[i]
            logger.info(event_str)

    return screens, edges, record_node_attrib


if __name__ == '__main__':
    # path_save_dir = "D://lab//ExtRep//newAdd//featureCoverage//test-33-DaysMatter-17//scenario//original_path"
    path_save_dir = "D://lab//ExtRep//newAdd//featureCoverage//experiment//approach//ExtRep-Ext//result1//test-29-CamScanner-16"
    script_path = "D://lab//ExtRep//newAdd//featureCoverage//experiment//approach//ExtRep-Ext//tmp//repair_script.py"
    # script_path = "D://lab//ExtRep//newAdd//featureCoverage//experiment//tmp//ExtRep//test-57-Diaguard-25.py"
    locators, caps, ori_code_line = read_test_scripts(script_path)
    script_replay(locators, path_save_dir)
