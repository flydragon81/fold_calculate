from typing import final
import sys
from model.SpsData import SpsData
from FixedWidthTextParser.Seismic.SpsParser import Point
import math
from model.helpers import create_new_point_ln_pn_idx, create_new_point_x_y
import pickle, json


@final
class Grid:
    NGEXT = 50
    NBEXT = 20

    def __init__(self, x0: float = 0.0, y0: float = 0.0, rot: float = 0.0,
                 dxb: float = 0.0, dyb: float = 0.0, nxb: int = 0, nyb: int = 0):
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

    def write_object(self, filename):
        file = open(filename, 'wb')
        pickle.dump(self, file)
        file.close()

    @staticmethod
    def read_object(filename):
        file = open(filename, 'rb')
        obj: Grid = pickle.load(file)
        file.close()
        return obj

    def write(self, filename):
        grid_dict = {'x0': self.__x0, 'y0': self.__y0, 'rot': self.__rot, 'dxb': self.__dxb,
                     'dyb': self.__dyb, 'nxb': self.__nxb, 'nyb': self.__nyb}
        file = open(filename, 'w')
        json.dump(grid_dict, file)
        file.close()

    def read(self, filename):
        file = open(filename, 'r')
        grid_dict = json.load(file)
        self.__x0 = grid_dict['x0']
        self.__y0 = grid_dict['y0']
        self.__rot = grid_dict['rot']
        self.__dxb = grid_dict['dxb']
        self.__dyb = grid_dict['dyb']
        self.__nxb = grid_dict['nxb']
        self.__nyb = grid_dict['nyb']
        file.close()

    @staticmethod
    def __min_float():
        return sys.float_info.min

    @staticmethod
    def __max_float():
        return sys.float_info.max

    def calculate_corners(self, sps_data: SpsData):
        min_x = sys.float_info.max
        max_x = sys.float_info.min
        min_y = sys.float_info.max
        max_y = sys.float_info.min

        src_point = sps_data.get_sps()
        rcv_point = sps_data.get_rps()

        point: Point
        for point in src_point:
            x = point.easting
            y = point.northing
            if x < min_x:
                self.__corners[0] = point
                min_x = x
            if x > max_x:
                self.__corners[2] = point
                max_x = x
            if y < min_y:
                self.__corners[1] = point
                min_y = y
            if y > max_y:
                self.__corners[3] = point
                max_y = y

        for point in rcv_point:
            x = point.easting
            y = point.northing
            if x < min_x:
                self.__corners[0] = point
                min_x = x
            if x > max_x:
                self.__corners[2] = point
                max_x = x
            if y < min_y:
                self.__corners[1] = point
                min_y = y
            if y > max_y:
                self.__corners[3] = point
                max_y = y
