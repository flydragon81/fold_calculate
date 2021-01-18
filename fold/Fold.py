import csv
from FixedWidthTextParser.Seismic.SpsParser import Point, Sps21Parser, Relation
from fold.Grid import Grid
from fold.helpers import create_point_by_easting_northing, create_point_by_line_point_idx
from fold.Bin import Bin


class Fold:
    def __init__(self, grid: Grid):
        self.__parser = Sps21Parser()
        self.__grid: Grid = grid
        self.__bin: dict = {}  # key is bin number, value is Bin object
        self.__row: dict = {}
        self.__col: dict = {}
        self.__rps = []
        self.__sps = []
        self.__rps_dict = {}
        self.__sps_dict = {}

    def get_rps(self):
        return self.__rps

    def get_sps(self):
        return self.__sps

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

    def load_sps(self):
        self.covert_r_to_dict()
        self.convert_s_to_dict()

    def covert_r_to_dict(self):
        for point in self.__rps:
            number = point.line
            if number in self.__rps_dict.keys():
                self.__rps_dict[number].append(point)
            else:
                self.__rps_dict[number] = [point]

    def convert_s_to_dict(self):
        points = self.__sps
        point: Point
        for point in points:
            combin = self.combin_line_point_idx(point.line, point.point, point.point_idx)
            self.__sps_dict[combin] = point

    def get_r_from_rline_frompn_topn(self, rline, frompn, topn):
        result = []
        point: Point
        for point in self.__rps_dict[rline]:
            if point.point >= frompn and point.point <= topn:
                result.append(point)
        return result

    def combin_line_point_idx(self, line: float, point: float, idx: int):
        combin = str(line) + str(point), str(idx)
        return combin

    def calculate_fold(self, xps_file):
        osln: float = 0
        ospn: float = 0
        osidx: int = 0
        sln: float = 0
        spn: float = 0
        sidx: int = 0
        rln: float = 0
        frp: float = 0
        trp: float = 0
        rx: float = 0
        ry: float = 0
        bx: float = 0
        by: float = 0
        sx: float = 0
        sy: float = 0
        with open(xps_file) as file:
            line = file.readline()
            while line:
                parsed = self.__parser.parse_relation(line)
                if parsed is not None:
                    relation = Relation(parsed)
                    sln = relation.line
                    spn = relation.point
                    sidx = relation.point_idx

                    combin = self.combin_line_point_idx(sln, spn, sidx)
                    src = self.__sps_dict[combin]
                    sx = src.easting
                    sy = src.northing
                    rline = relation.rcv_line
                    frp = relation.from_rcv
                    trp = relation.to_rcv
                    rpoints = self.get_r_from_rline_frompn_topn(rline, frp, trp)
                    point: Point
                    for point in rpoints:
                        rx = point.easting
                        ry = point.northing
                        bx = (sx + rx) / 2
                        by = (sy + ry) / 2
                        # offset = math.sqrt(math.pow(sx - rx, 2) + math.pow(sy - ry, 2))

                        bpoint = create_point_by_easting_northing(bx, by)
                        brpoint = self.__grid.rotate_point_x_y(bpoint)
                        bin = self.__grid.bin_xy2cr(brpoint)
                        binn = self.__grid.bin_number(bin)
                        if binn in self.__bin.keys():
                            self.__bin[binn].fold += 1
                            self.__col[binn] = bin.column
                            self.__row[binn] = bin.row
                        else:
                            bin.fold = 1
                            self.__bin[binn] = bin
                line = file.readline()

    def write_fold_to_csv(self, file_name):
        with open(file_name, 'w', newline='') as f:
            head = ['binn', 'row', 'column', 'easting', 'northing', 'fold']
            writer = csv.writer(f)
            writer.writerow(head)
            for key in self.__bin.keys():
                #self.__bin[key]= Bin()
                row = [key,
                       self.__bin[key].fold,
                       self.__bin[key].row,
                       self.__bin[key].column,
                       self.__bin[key].easting,
                       self.__bin[key].northing,
                       ]

                # 写入一行数据
                writer.writerow(row)
