from FixedWidthTextParser.Seismic.SpsParser import Relation, Point


class Template:
    def __init__(self, point: Point):
        self.__point = point
        self.__relations = []

    def get_point(self):
        return self.__point

    def set_relations(self, relations):
        self.__relations = relations

    def get_relations(self):
        return self.__relations

    def add_relation(self, relation: Relation):
        self.__relations.append(relation)

    def read_relation(self, xps_file):

        pass
