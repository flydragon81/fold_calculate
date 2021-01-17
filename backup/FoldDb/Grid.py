"""
    Grid
"""
import sys
import math
import pickle
import json
from typing import final
from FixedWidthTextParser.Seismic.SpsParser import Point

from model.SpsData import SpsData
from model.fold.Bin import Bin
from model.helpers import create_point_by_line_point_idx, create_point_by_easting_northing


@final
class Grid:
    NGEXT = 50
    NBEXT = 20

    # __x0 = float
    # __y0 = float
    # __rot = float
    # __dxb = float
    # __dyb = float
    # __nxb = int
    # __nyb = int
    # __corners = list

    def __init__(self, x0: float = 0.0, y0: float = 0.0, rot: float = 0.0, dxb: float = 0.0, dyb: float = 0.0,
                 nxb: int = 0, nyb: int = 0):

        self.__x0 = x0
        self.__y0 = y0
        self.__rot = rot
        self.__dxb = dxb
        self.__dyb = dyb
        self.__nxb = nxb
        self.__nyb = nyb
        self.__corners = [None, None, None, None]

    def get_x0(self):
        return self.__x0

    def get_y0(self):
        return self.__y0

    def get_rot(self):
        return self.__rot

    def get_dxb(self):
        return self.__dxb

    def get_dyb(self):
        return self.__dyb

    def get_nxb(self):
        return self.__nxb

    def get_nyb(self):
        return self.__nyb

    def get_corners(self):
        return self.__corners

    def calculate_corners(self, sps_data: SpsData):
        """
            SpsData sps_data
        """
        min_x = sys.float_info.max
        max_x = sys.float_info.min
        min_y = sys.float_info.max
        max_y = sys.float_info.min

        src_points = sps_data.get_all_s()
        rcv_points = sps_data.get_all_r()

        point: Point
        for point in src_points:
            x = point.easting
            y = point.northing

            # C[0]
            if x < min_x:
                self.__corners[0] = point
                min_x = x

            # C[2]
            if x > max_x:
                self.__corners[2] = point
                max_x = x

            # C[1]
            if y < min_y:
                self.__corners[1] = point
                min_y = y

            # C[3]
            if y > max_y:
                self.__corners[3] = point
                max_y = y

        for point in rcv_points:
            x = point.easting
            y = point.northing

            # C[0]
            if x < min_x:
                self.__corners[0] = point
                min_x = x

            # C[2]
            if x > max_x:
                self.__corners[2] = point
                max_x = x

            # C[1]
            if y < min_y:
                self.__corners[1] = point
                min_y = y

            # C[3]
            if y > max_y:
                self.__corners[3] = point
                max_y = y

    def rotate_point_x_y(self, point: Point, counterclockwise=False):
        rotated_point = create_point_by_line_point_idx(point.line, point.point, point.point_idx)
        x = point.easting
        y = point.northing
        x0 = float(self.__x0)
        y0 = float(self.__y0)
        rot = float(self.__rot)
        if counterclockwise is True:
            rot = rot * -1

        radians = math.radians(rot)

        adjusted_x = (x - x0)
        adjusted_y = (y - y0)
        cos_rad = math.cos(radians)
        sin_rad = math.sin(radians)
        rotx = x0 + cos_rad * adjusted_x + sin_rad * adjusted_y
        roty = y0 + -sin_rad * adjusted_x + cos_rad * adjusted_y

        rotated_point.easting = rotx
        rotated_point.northing = roty

        return rotated_point

    def bin_xy2cr(self, rotated: Point):
        b = Bin()

        c1 = (rotated.easting - self.__x0) / self.__dxb
        c2 = math.floor(c1)

        if c1 > c2:
            c = int(c2 + 1)
        else:
            c = int(c2)

        r1 = (rotated.northing - self.__y0) / self.__dyb
        r2 = math.floor(r1)

        if r1 > r2:
            r = int(r2 + 1)
        else:
            r = int(r2)

        b.column = c
        b.row = r

        return b

    def bin_number(self, b: Bin):
        number = -1
        if b.column > 0 and b.row > 0:
            number = (b.row - 1) * self.__nxb + b.column

        return number

    def bin_cr(self, bin_number: int):
        b = Bin()
        r = int(math.floor((bin_number / self.__nxb)) + 1)
        c = bin_number - (r - 1) * self.__nxb
        b.column = c
        b.row = r

        return b

    def write_object(self, filename):
        file = open(filename, "wb")
        pickle.dump(self, file)
        file.close()

    @staticmethod
    def read_object(filename):
        file = open(filename, "rb")
        obj: Grid = pickle.load(file)
        file.close()
        return obj

    def write(self, filename):
        grid_dict = {'x0': self.__x0, 'y0': self.__y0, 'rot': self.__rot, 'dxb': self.__dxb, 'dyb': self.__dyb,
                     'nxb': self.__nxb, 'nyb': self.__nyb}
        file = open(filename, "w")
        json.dump(grid_dict, file)
        file.close()

    def read(self, filename):
        file = open(filename, "r")
        grid_dict = json.load(file)
        self.__x0 = grid_dict['x0']
        self.__y0 = grid_dict['y0']
        self.__rot = grid_dict['rot']
        self.__dxb = grid_dict['dxb']
        self.__dyb = grid_dict['dyb']
        self.__nxb = grid_dict['nxb']
        self.__nyb = grid_dict['nyb']
        file.close()

# def __calculate_rot(self, sps_data: SpsData):
#     rl_max_n = sps_data.get_line_for_max_n_rps()
#     sl_max_n = sps_data.get_line_for_max_n_sps()
#     n_rp = sps_data.get_n_points_for_rcv_line(rl_max_n)
#     n_sp = sps_data.get_n_points_for_src_line(sl_max_n)
#     rcv = sps_data.get_all_points_for_rcv_line(rl_max_n)
#     src = sps_data.get_all_points_for_src_line(sl_max_n)
#
#     min_pn = sys.float_info.max
#     max_pn = sys.float_info.min
#
#     min_rp: Point = None
#     max_rp: Point = None
#
#     min_x_r = sps_data.get_x_min_r()
#     max_x_r = sps_data.get_x_max_r()
#     min_y_r = sps_data.get_y_min_r()
#     max_y_r = sps_data.get_y_max_r()
#
#     min_x_s = sps_data.get_x_min_s()
#     max_x_s = sps_data.get_x_max_s()
#     min_y_s = sps_data.get_y_min_s()
#     max_y_s = sps_data.get_y_max_s()
#
#     # print(min_x_r, max_x_r)
#     # print(min_y_r, max_y_r)
#
#     # rp: Point
#     # for rp in rcv:
#     #     if min_pn > rp.point:
#     #         min_pn = rp.point
#     #         min_rp = rp
#     #
#     #     if max_pn < rp.point:
#     #         max_pn = rp.point
#     #         max_rp = rp
#     #
#     # min_pn = sys.float_info.max
#     # max_pn = sys.float_info.min
#     #
#     # min_sp: Point = None
#     # max_sp: Point = None
#     #
#     # for sp in src:
#     #     if min_pn > sp.point:
#     #         min_pn = sp.point
#     #         min_sp = sp
#     #
#     #     if max_pn < sp.point:
#     #         max_pn = sp.point
#     #         max_sp = sp
#
#     len_r = math.sqrt(math.pow(min_x_r - max_x_r, 2) + math.pow(min_y_r - max_y_r, 2))
#     len_s = math.sqrt(math.pow(min_x_s - max_x_s, 2) + math.pow(min_y_s - max_y_s, 2))
#     d_rl_y = max_y_r - min_y_r
#     d_sl_y = max_y_s - min_y_s
#
#     # len_r = math.sqrt(math.pow(min_rp.easting - max_rp.easting, 2) + math.pow(min_rp.northing - max_rp.northing, 2))
#     # len_s = math.sqrt(math.pow(min_sp.easting - max_sp.easting, 2) + math.pow(min_sp.northing - max_sp.northing, 2))
#     # d_rl_y = max_rp.northing - min_rp.northing
#     # d_sl_y = max_sp.northing - min_sp.northing
#
#     self.rot_rcv = math.acos(d_rl_y / len_r) * 180 / math.pi
#     self.rot_src = math.acos(d_sl_y / len_s) * 180 / math.pi
#
#     # self.d_rcv = len_r / (n_rp - 1)
#     # self.d_src = len_s / (n_sp - 1)
#
#     if self.rot_rcv < self.rot_src:
#         if self.lock_rot is False:
#             self.rot = self.rot_rcv
#     else:
#         if self.lock_rot is False:
#             self.rot = self.rot_src
#
# def calculate_grid(self, sps_data: SpsData):
#     self.__calculate_rot(sps_data)
#     self.__calculate_grid_origin(sps_data)
#     # self.__calculate_grid_nb(sps_data)
#
# def calculate_grid_new(self, sps_data: SpsData, dxb: float, dyb: float):
#     pass
