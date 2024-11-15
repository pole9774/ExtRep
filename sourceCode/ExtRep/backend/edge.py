class Edge:
    """
    GUI edge
    """

    def __init__(self, b_id, e_id, n_id):
        self.begin_id = b_id
        self.end_id = e_id
        self.action = 'clicked'

        self.node_id = n_id


def has_same_edge(screens, edges, begin_id, end_id, clicked_node):
    for edge in edges:
        if edge.begin_id == begin_id and edge.end_id == end_id:
            screen = screens[begin_id]
            node = screen.get_node_by_id(edge.node_id)
            if node.loc_x == clicked_node.loc_x and node.loc_y == clicked_node.loc_y and \
                    node.width == clicked_node.width and node.height == clicked_node.height:
                return True

    return False