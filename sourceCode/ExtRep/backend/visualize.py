import os

import cv2
from graphviz import Digraph


class VisualTool:
    def __init__(self, screens, edges, edge_bounds, save_dir, ori_screen_ids, ori_edge_bounds_order):
        self.dot = Digraph(comment='The Round Table')

        self.screens = screens
        self.edges = edges
        self.edge_bounds = edge_bounds

        self.save_dir = save_dir

        self.ori_screen_ids = ori_screen_ids
        self.ori_edge_bounds_order = ori_edge_bounds_order

    def create_nodes(self):
        for key in self.screens.keys():
            screen = self.screens[key]

            img = cv2.imread(screen.shot_dir)
            small_img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

            img_dir = os.path.join(self.save_dir, 'image')

            if not os.path.exists(img_dir):
                os.makedirs(img_dir)

            file = os.path.join(img_dir, str(screen.id) + '.png')
            cv2.imwrite(file, small_img)
            self.dot.node(str(screen.id), shapefile=file, fontsize='30')


    def create_edges(self):
        for i in range(0, len(self.edges)):
            edge = self.edges[i]
            bounds = self.edge_bounds[i]
            clickable_node = self.screens[edge.begin_id].get_node_by_id(edge.node_id)
            if clickable_node is None:
                clickable_node = self.screens[edge.begin_id].get_node_by_bounds(bounds)
            if clickable_node is not None:
                if clickable_node.attrib['text'] != '':
                    label = clickable_node.attrib['text'] + '-' + clickable_node.attrib['bounds']
                elif clickable_node.attrib['content-desc'] != '':
                    label = clickable_node.attrib['content-desc'] + '-' + clickable_node.attrib['bounds']
                elif clickable_node.attrib['resource-id'] != '':
                    label = clickable_node.attrib['resource-id'].split('/')[1] + '-' + clickable_node.attrib['bounds']
                else:
                    label = clickable_node.attrib['bounds']
            else:
                print("please check: " + "begin_id = " + str(edge.begin_id) + " end_id = " + str(edge.end_id) + " bounds = " + str(bounds))
                continue
            if edge.begin_id in self.ori_screen_ids and edge.end_id in self.ori_screen_ids:
                begin_screen_index = self.ori_screen_ids.index(edge.begin_id)
                ori_edge_bounds = self.ori_edge_bounds_order[begin_screen_index]
                if bounds[0] == ori_edge_bounds[0] and bounds[1] == ori_edge_bounds[1] and \
                        bounds[2] == ori_edge_bounds[2] and bounds[3] == ori_edge_bounds[3]:
                    self.dot.edge(str(edge.begin_id), str(edge.end_id), label=label, fontname='SimSun', fontsize='30')
                else:
                    self.dot.edge(str(edge.begin_id), str(edge.end_id), label=label, fontname='SimSun', fontsize='30', color='blue')
            else:
                self.dot.edge(str(edge.begin_id), str(edge.end_id), label=label, fontname='SimSun', fontsize='30', color='blue')


    def save_graph(self):
        self.dot.render(filename='extended_graph', directory=self.save_dir, view=True)

    def save_work(self):
        self.create_nodes()
        self.create_edges()
        self.save_graph()


class VisualToolCrawler:
    def __init__(self, screens, edges, save_dir):
        self.dot = Digraph(comment='The Round Table')

        self.screens = screens

        self.edges = edges

        self.save_dir = save_dir

    def create_nodes(self):
        for key in self.screens.keys():
            screen = self.screens[key]

            img = cv2.imread(screen.shot_dir)
            small_img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

            img_dir = self.save_dir + '/' + 'image'

            if not os.path.exists(img_dir):
                os.makedirs(img_dir)

            cv2.imwrite(img_dir + '/' + str(screen.id) + '.png', small_img)

            self.dot.node(str(screen.id), shapefile=img_dir + '/' + str(screen.id) + '.png', fontsize='30')

    def create_edges(self):
        for edge in self.edges:
            node_id = edge.node_id
            clickable_node = self.screens[edge.begin_id].get_node_by_id(node_id)
            if clickable_node.attrib['text'] != '':
                label = clickable_node.attrib['text'] + '-' + clickable_node.attrib['bounds']
            elif clickable_node.attrib['content-desc'] != '':
                label = clickable_node.attrib['content-desc'] + '-' + clickable_node.attrib['bounds']
            elif clickable_node.attrib['resource-id'] != '':
                label = clickable_node.attrib['resource-id'].split('/')[1] + '-' + clickable_node.attrib['bounds']
            else:
                label = clickable_node.attrib['bounds']
            # label = clickable_node.attrib['bounds']
            self.dot.edge(str(edge.begin_id), str(edge.end_id), label=label, fontname='SimSun', fontsize='30')

    def save_graph(self):
        self.dot.render(filename='traverse_graph2', directory=self.save_dir, view=True)

    def save_work(self):
        self.create_nodes()
        self.create_edges()
        self.save_graph()