from FixedWidthTextParser.Seismic.SpsParser import Sps21Parser, Point, Relation
from model.Template import Template
from model.helpers import create_new_point
from model.Stats import Stats


class SpsData:
    def __init__(self):
        self.__rps = []  # [Point]
        self.__sps = []  # [Point]
        self.__xps = []  # [Template]
        self.__parser = Sps21Parser()

        self.__stats_calculated = False
        self.__stats_sps = []  # src stats
        self.__stats_rps = []  # rcv stats

    def get_rps(self):
        return self.__rps

    def get_sps(self):
        return self.__sps

    def get_xps(self):
        return self.__xps

    def get_status_rps(self):
        return self.__stats_rps

    def get_status_sps(self):
        return self.__stats_sps

    def set_xps(self, xps_file):
        self.__xps = self.__xps_file_read(xps_file)

    def set_rps(self, rps_file):
        self.__rps = self.__point_file_read(rps_file)

    def set_sps(self, sps_file):
        self.__sps = self.__point_file_read(sps_file)

    def __point_file_read(self, point_file):
        result = []

        with open(point_file) as file:
            line = file.readline()
            while line:
                parsed = self.__parser.parse_point(line)
                if parsed is not None:
                    point = Point(parsed)
                    result.append(point)

                line = file.readline()

        return result

    def __xps_file_read(self, xps_file):
        osln = 0.0
        ospn = 0.0
        osidx = 0
        template: Template = None
        templates = []
        with open(xps_file) as file:
            line = file.readline()
            while line:
                parsed = self.__parser.parse_relation(line)
                if parsed is not None:
                    rel = Relation(parsed)
                    if osln == rel.line and ospn == rel.point and osidx == rel.point_idx:
                        template.add_relation(rel)
                    else:
                        if template is not None:
                            templates.append(template)
                        point = create_new_point(rel.line, rel.point, rel.point_idx)
                        template = Template(point)
                        template.add_relation(rel)
                    osln = rel.line
                    ospn = rel.point
                    osidx = rel.point_idx

                line = file.readline()

        if template is not None:
            templates.append(template)

        return templates

    def get_stats_s(self):
        return self.__stats_sps

    def get_stats_r(self):
        return self.__stats_rps

    def calculate_stats(self):
        if self.__stats_calculated is False:
            self.__calculate_stats(self.__sps, self.__stats_sps)
            self.__calculate_stats(self.__rps, self.__stats_rps)
            self.__stats_calculated = True

    def get_line_for_max_n_rps(self):
        return self.__get_line_for_max_n_points(self.__stats_rps)

    def get_line_for_max_n_sps(self):
        return self.__get_line_for_max_n_points(self.__stats_sps)

    @staticmethod
    def __get_line_for_max_n_points(stats: list):
        stats.sort(key=lambda x: x.n, reverse=True)
        return stats[0].ln

    def get_n_points_for_rcv_line(self, rcv_line):
        return self.__get_n_points_for_line(rcv_line, self.__stats_rps)

    def get_n_points_for_src_line(self, src_line):
        return self.__get_n_points_for_line(src_line, self.__stats_sps)

    @staticmethod
    def __get_n_points_for_line(line_number, stats: list):
        n = 0
        for i in stats:
            if line_number == i.ln:
                n = i.n
        return n

    def get_all_points_for_rcv_line(self, rcv_line):
        return self.__get_all_points_for_line(rcv_line, self.__rps)

    def get_all_points_for_src_line(self, src_line):
        return self.__get_all_points_for_line(src_line, self.__sps)

    @staticmethod
    def __get_all_points_for_line(line_number, point: list):
        points = []
        for po in point:
            if po.line == line_number:
                points.append(po)

    # get point from line_number and point_number
    def get_point_for_rcv_line_point(self, rcv_line, rcv_point):
        return self.__get_point_for_line_point(rcv_line, rcv_point, self.__rps)

    def get_point_for_src_line_point(self, src_line, src_point):
        return self.__get_point_for_line_point(src_line, src_point, self.__sps)

    @staticmethod
    def __get_point_for_line_point(line_number,point_number, point: list):
        points = []
        for po in point:
            if po.line == line_number and po.point == point_number:
                points = po
        return points

    # get line stats
    def get_line_stats_for_rcv_line(self, rcv_line):
        return self.__get_line_stats_for_line(rcv_line, self.__stats_rps)

    def get_line_stats_for_src_line(self, src_line):
        return self.__get_line_stats_for_line(src_line, self.__stats_sps)

    @staticmethod
    def __get_line_stats_for_line(line_number, stats_list: list):
        result = []
        for st in stats_list:
            if st.ln == line_number:
                result = st
        return result

    def stats_calculate(self):
        if self.__stats_calculated is False:
            self.__calculate_stats(self.__sps, self.__stats_sps)
            self.__calculate_stats(self.__rps, self.__stats_rps)
            self.__stats_calculated = True

    def __calculate_stats(self, point_list: list, stats_list: list):
        # point_list.sort(key=lambda x: x.line)
        size = len(stats_list)
        st = Stats()
        st.ln = 0.0
        st.n = 0
        st.fp = 0.0
        st.lp = 0.0
        for po in point_list:
            i = 0
            num = 0
            while i < size:
                st = stats_list[i]
                if st.ln == po.line:
                    # st.ln = lln
                    stats_list[i].n += 1
                    num += 1
                    if st.fp > po.point:
                        stats_list[i].fp = po.point
                    if st.lp < po.point:
                        stats_list[i].lp = po.point

                i += 1
            if num == 0:
                newst = Stats()
                newst.ln = po.line
                newst.n = 1
                newst.fp = po.point
                newst.lp = po.point
                stats_list.append(newst)
                size = len(stats_list)

        return stats_list
        newst = Stats()
        newst.ln = po.line
        newst.n = 1
        newst.fp = po.point
        newst.lp = po.point
        stats_list.append(newst)
