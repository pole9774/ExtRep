import os
import sys
import warnings
import xml.etree.ElementTree as xeTree

from uiautomator import device

from backend.screen import Screen, is_same_screen
from backend.xml_tree import parse_nodes


def get_activity_name():
    cmd = 'adb shell \"dumpsys window w | grep name=\" '
    result = os.popen(cmd)
    res = result.buffer.read().decode(encoding='utf-8')
    activity_name = ''
    for line in res.splitlines():
        if "activity" in line.lower():
            activity_name = line.split('/')[1][:-1]
            break

    return activity_name


def get_package_name():
    try:
        cmd = "adb shell \"dumpsys window w | grep name=\""
        r = os.popen(cmd)
        info = r.readlines()

        for i in range(len(info)):
            if 'Activity' in info[i]:
                package_name = info[i].strip().split('/')[0].split('name=')[1]
                break
            else:
                if 'mumu' not in info[i] and 'systemui' not in info[i] and '/' in info[i]:
                    package_name = info[i].strip().split('/')[0].split('name=')[1]
                    break

        return package_name
    except Exception as e:
        return 'error package name'


def get_cur_screen_info():
    xml_info = device.dump(compressed=False)
    root = xeTree.fromstring(xml_info)
    nodes = parse_nodes(root)
    act_name = get_activity_name()

    return nodes, act_name


def get_tmp_screen():
    xml_info = device.dump(compressed=False)
    root = xeTree.fromstring(xml_info)
    nodes = parse_nodes(root)
    act_name = get_activity_name()
    tmp_screen = Screen(nodes, -1, act_name)

    return tmp_screen


def save_screen(screen, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    device.dump(os.path.join(save_path, str(screen.id) + '.xml'), compressed=False)
    device.screenshot(os.path.join(save_path, str(screen.id) + '.png'))
    screen.shot_dir = os.path.join(save_path, str(screen.id) + '.png')


def has_same_screen(screens, tmp_screen, distinct_rate):
    for screen_id in screens.keys():
        screen = screens[screen_id]
        if is_same_screen(screen, tmp_screen, distinct_rate):
            return screen_id

    return -1


def get_elements():
    """
    get screen elements
    :return:
    """

    xml_info = device.dump(compressed=False)
    root = xeTree.fromstring(xml_info)
    nodes = parse_nodes(root)
    # act_name = self.get_activity_name()
    # tmp_screen = Screen(nodes, -1, act_name)
    for node in nodes:
        if not node.children:
            print(node.attrib)

