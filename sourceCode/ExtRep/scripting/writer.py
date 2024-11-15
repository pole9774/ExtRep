import os

import xml.etree.ElementTree as xeTree

def extract_nodes_with_attrib(root, attrib_type, target_attrib):
    nodes = []
    if (str(root.attrib.get(attrib_type))).replace(" ", "") == target_attrib.replace(" ", ""):
        nodes.append(root.attrib)
    for child in root:
        nodes.extend(extract_nodes_with_attrib(child, attrib_type, target_attrib))
    return nodes

def locate_element(record_node_attrib, xml_file_path):
    attribs = {}
    attribs["resource-id"] = "resource-id"
    attribs["text"]= "text"
    attribs["content-desc"] = "content-desc"
    attribs["class"] = "class"
    attribs["bounds"] = "bounds"

    code = ""
    for attrib in attribs:
        target_attrib = record_node_attrib[attrib]
        if target_attrib == "":
            continue

        xml_tree = xeTree.parse(xml_file_path)
        root = xml_tree.getroot()
        nodes = extract_nodes_with_attrib(root, attrib, target_attrib)

        if attrib == "resource-id":
            for i in range(0, len(nodes)):
                if str(nodes[i]).replace(" ", "") == str(record_node_attrib).replace(" ", ""):
                    code = "driver.find_elements_by_id('" + nodes[i].get(attrib) + "')" + "[" + str(i) + "]"
                    break
            if code != "":
                break

        if attrib == "text" and len(nodes) == 1:
            code = "driver.find_element_by_android_uiautomator('new UiSelector().text(" + '"' + nodes[0].get(attrib) + '"' + ")')"
            break

        if attrib == "content-desc" and len(nodes) == 1:
            code = "driver.find_element_by_accessibility_id('" + nodes[0].get(attrib) + "')"
            break

        if attrib == "class":
            for i in range(0, len(nodes)):
                if str(nodes[i]).replace(" ", "") == str(record_node_attrib).replace(" ", ""):
                    code = "driver.find_elements_by_class_name('" + nodes[i].get(attrib) + "')" + "[" + str(i) + "]"
                    break
            if code != "":
                break

        if attrib == "bounds" and len(nodes) == 1:
            # target attrib does not have spaces
            cur_bound = target_attrib.split("[")[1]
            cur_bound = cur_bound.split("]")[0]
            bound_x = cur_bound.split(",")[0]
            bound_y = cur_bound.split(",")[1]
            code = 'driver.tap([(' + bound_x + ', ' + bound_y + ')])'
            break

    return code

def write_repaired_test_script(codes, result_test_script, caps):
    if not os.path.exists(result_test_script):
        os.makedirs(result_test_script)
    result_file = 'repaired_script.py'

    with open(os.path.join(result_test_script, result_file), 'w') as f:
        f.write("import time\n")
        f.write("from appium import webdriver\n\n")
        f.write("desired_caps = {}\n")
        for cap in caps:
            if cap != 'webdriver.Remote':
                f.write(caps[cap])
                f.write('\n')
        f.write('\n')
        f.write(caps['webdriver.Remote'])
        f.write('\n')
        f.write('time.sleep(10)\n\n')

        f.write('try:\n')
        els = []
        for i in range(0, len(codes)):
            cur_el = '    el' + str(i + 1) + ' = ' + codes[i] + '\n'
            cur_el_click = '    el' + str(i + 1) + '.click()' + '\n'
            cur_el += cur_el_click
            els.append(cur_el)

        for el in els[0:-1]:
            f.write(el)
            f.write('    time.sleep(3)\n\n')

        f.write(els[-1])
        f.write('\n')
        f.write('finally:\n    time.sleep(3)\n    driver.quit()\n')

