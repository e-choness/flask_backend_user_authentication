class Tree(object):
    def __init__(self, data):
        self.data = data
        self.root_node = list()
        self.common_node = dict()
        self.tree = list()

    def find_root_node(self, ) -> list:
        """
        find root
        :return: root list node
        """
        # self.root_node = list(filter(lambda x: x["father_id"] is None, data))
        for node in self.data:
            if node["father_id"] is None:
                self.root_node.append(node)
        return self.root_node

    def find_common_node(self) -> dict:
        """
        :return: 
        """

        for node in self.data:
            father_id = node.get("father_id")
            if father_id is not None:
                if father_id not in self.common_node:
                    self.common_node[father_id] = list()
                self.common_node[father_id].append(node)
        return self.common_node

    def build_tree(self, ) -> list:
        """
        :return:
        """
        self.find_root_node()
        self.find_common_node()
        for root in self.root_node:
            base = dict(name=root["name"], id=root["id"], child=list())
            self.find_child(base["id"], base["child"])
            self.tree.append(base)
        return self.tree

    def find_child(self, father_id: int, child_node: list):
        """
        :param father_id:
        :param child_node: 
        :return:
        """
        child_list = self.common_node.get(father_id, [])
        for item in child_list:
            base = dict(name=item["name"], id=item["id"], child=list())
            self.find_child(item["id"], base["child"])
            child_node.append(base)
