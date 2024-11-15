class Screen():
    """
    GUI screen/state
    """

    def __init__(self, nodes, s_id, activity):
        self.act_name = activity
        self.id = s_id
        # the event sequence that reached the screen
        self.event_sequences = []
        self.nodes = nodes
        self.has_clicked_nodes = []

        self.depth = -1

        self.des = []

        self.all_transfer_sequences = []

        self.visited_des = []

        self.shortest_transfer_sequences = []

        self.shot_dir = ''

        self.filter_id = False

        self.id_list = []

    def get_clickable_node(self):
        clickable_nodes = []
        id_list = []
        for node in self.nodes:
            if not is_node_in_list(node, self.has_clicked_nodes) and \
                    node.attrib['clickable'] == 'true' and \
                    node.attrib['resource-id'] not in id_list:

                clickable_nodes.append(node)

        if not clickable_nodes:
            return None
        else:
            self.has_clicked_nodes.append(clickable_nodes[0])
            return clickable_nodes[0]

    def get_clickable_leaf_node(self, black_elem_list):
        clickable_nodes = []
        for node in self.nodes:
            if node.attrib['clickable'] == 'true':
                if not node.children:
                    if not is_in_black_list(node, black_elem_list):
                        if not is_node_in_list(node, self.has_clicked_nodes) and not is_ignored_node(node) and \
                                node.attrib['resource-id'] not in self.id_list:
                            clickable_nodes.append(node)

                            if node.attrib['resource-id'] != '' and self.filter_id is True:
                                self.id_list.append(node.attrib['resource-id'])
                else:
                    for desc in node.descendants:
                        if not desc.children:
                            if not is_in_black_list(desc, black_elem_list):
                                if not is_node_in_list(desc, self.has_clicked_nodes) \
                                        and not is_ignored_node(desc) and \
                                        desc.attrib['resource-id'] not in self.id_list and \
                                        not is_node_in_list(desc, clickable_nodes):
                                    clickable_nodes.append(desc)

                                    if desc.attrib['resource-id'] != '' and self.filter_id is True:
                                        self.id_list.append(desc.attrib['resource-id'])

        if not clickable_nodes:
            return None
        else:
            self.has_clicked_nodes.append(clickable_nodes[0])
            return clickable_nodes[0]

    def get_node_by_id(self, node_id):
        for node in self.nodes:
            if node.idx == node_id:
                return node

        return None

    def get_node_by_bounds(self, bounds):
        for node in self.nodes:
            if is_ignored_node(node) is not True and \
                    node.loc_x == bounds[0] and node.loc_y == bounds[1] and \
                    node.width == bounds[2] and node.height == bounds[3]:
                return node

        return None

def is_ignored_node(node):
    if 'Layout' in node.attrib['class'] or node.attrib['class'] == 'android.view.View':
        return True

    return False


class Stack:
    """
    a stack to store screen ids
    """
    def __init__(self):
        self.items = []

    def push(self, num):
        self.items.append(num)

    def pop(self):
        return self.items.pop()

    def empty(self):
        return self.items == []

    def top(self):
        if self.items:
            return self.items[len(self.items) - 1]

        return -1

    def size(self):
        return len(self.items)


class Queue:
    """
    a queue to store screen ids
    """

    def __init__(self):
        self.items = []

    def push(self, num):
        self.items.append(num)

    def pop(self):
        if self.items:
            return self.items.pop(0)

        return -1

    def empty(self):
        return self.items == []

    def top(self):
        if self.items:
            return self.items[0]

        return -1

    def size(self):
        return len(self.items)

    def remove(self, num):
        if num in self.items:
            self.items.remove(num)
            return self.items

        return -1


def is_same_screen(x_screen, y_screen, distinct_rate):
    if x_screen.act_name != y_screen.act_name:
        return False

    x_xpath_list = []
    y_xpath_list = []

    for node in x_screen.nodes:
        x_xpath_list.append(node.full_xpath)

    for node in y_screen.nodes:
        y_xpath_list.append(node.full_xpath)

    count = 0
    for xpath in x_xpath_list:
        if xpath in y_xpath_list:
            count += 1

    if max(len(x_xpath_list), len(y_xpath_list)) == 0:
        return False

    if count / max(len(x_xpath_list), len(y_xpath_list)) >= distinct_rate:
        return True

    return False


def is_node_in_list(tmp_node, node_list):
    for node in node_list:
        if tmp_node.idx == node.idx:
            return True

    return False


def is_in_black_list(tmp_node, black_elem_list):
    node_text = tmp_node.attrib['text']
    node_id = tmp_node.attrib['resource-id']
    node_content = tmp_node.attrib['content-desc']
    is_black = False

    for text in black_elem_list['text']:
        if text in node_text:
            is_black = True

    for res_id in black_elem_list['id']:
        if res_id in node_id:
            is_black = True

    for content in black_elem_list['content']:
        if content in node_content:
            is_black = True

    for idx in black_elem_list['idx']:
        if idx == tmp_node.idx:
            is_black = True

    return is_black