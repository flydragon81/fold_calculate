import math

from FoldDb.Grid import Grid
from SpsDataDb.SpsDataDb import SpsDataDb
from SpsDataDb.entity.Template import Template, Xps
from SpsDataDb.entity.Rps import Rps

from FixedWidthTextParser.Seismic.SpsParser import Point
from FoldDb.helpers import create_point_by_easting_northing


class Fold:
    def __init__(self, grid: Grid):
        self.__grid: Grid = grid
        self.__bin: dict = {}  # key is bin number, value is Bin object
        self.__fold_array: list = [0] * (self.__grid.get_nxb() * self.__grid.get_nyb())
        self.__row = self.__fold_array.copy()
        self.__col = self.__fold_array.copy()
        self.__rps_dict = {}
        self.__sps_dict = {}

    def get_fold(self):
        return self.__fold_array

    def convert_r_to_dic(self, sps: SpsDataDb):
        points = sps.get_all_r()
        point:Point
        for point in points:
            self.__rps_dict(point.line)
            pass

    def calculate_fold(self, sps: SpsDataDb):
        osln: float = 0
        ospn: float = 0
        osidx: int = 0
        points: list = []
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

        t: Template
        for t in sps.get_all_x():
            sline = t.sline
            spoint = t.spoint
            sidx = t.sidx

            src = sps.get_s(sline, spoint, sidx)
            xps: Xps
            for xps in t.relations:
                # xrlin = xps.rline
                # xrfrp = xps.from_rp
                # xrtrp = xps.to_rp
                # xridx = xps.ridx
                # for rp in range(int(xrfrp), int(xrtrp)):
                #     rpoint = sps.get_r(xrlin, float(rp), xridx)

                rpoints = sps.get_r4line_range_points(xps.rline, xps.from_rp, xps.to_rp)

                point: Rps
                for point in rpoints:
                    rx = point.easting
                    ry = point.northing
                    bx = (src.easting + rx) / 2
                    by = (src.northing + ry) / 2
                    # offset = math.sqrt(math.pow(sx - rx, 2) + math.pow(sy - ry, 2))

                    bpoint = create_point_by_easting_northing(bx, by)
                    brpoint = self.__grid.rotate_point_x_y(bpoint)
                    bin = self.__grid.bin_xy2cr(brpoint)
                    binn = self.__grid.bin_number(bin)
                    if binn > 0 & binn < len(self.__fold_array):
                        self.__fold_array[binn] += 1
                        self.__col[binn] = bin.column
                        self.__row[binn] = bin.row

    # def cover_rps_to_dict(self, sps: SpsDataDb):
    #     points = sps.get_all_r()
