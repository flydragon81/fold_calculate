from typing import final
from class_attr_check import auto_attr_check
import sys
from model.SpsData import SpsData
from FixedWidthTextParser.Seismic.SpsParser import Point
import math
from model.helpers import create_new_point, create_new_point0


@auto_attr_check
@final
class Grid:
    NGEXT = 50
    NBEXT = 20
    x0 = float
    y0 = float
    rot = float
    dxb = float
    dyb = float
    nxb = int
    nyb = int
    lockx0 = bool
    locky0 = bool
    lockrot = bool
    lockdxb = bool
    lockdyb = bool
    locknxb = bool
    locknyb = bool
    rot_src = float
    rot_rcv = float
    d_src = float
    d_rcv = float
    __corners = []

    def get_corners(self):
        return self.__corners

    def reset_helper(self):
        self.rot_src = 0
        self.rot_rcv = 0
        self.d_src = 0
        self.d_rcv = 0

    @staticmethod
    def __min_float():
        return sys.float_info.min

    @staticmethod
    def __max_float():
        return sys.float_info.max

    def calculate_corners(self, sps_data: SpsData, sps, rps):
        min_x = sys.float_info.max
        max_x = sys.float_info.min
        min_y = sys.float_info.max
        max_y = sys.float_info.min
        sps_data.set_sps(sps)
        sps_data.set_rps(rps)
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

    def point_rotate_x_y(self, point: Point):
        new_point = create_new_point(point.line, point.point, point.point_idx)
        x = point.easting
        y = point.northing
        x0 = float(self.x0)
        y0 = float(self.y0)
        rot = float(self.rot)

        if (rot == 45) or (rot == -45):
            rot += 0.00000000000000001
        dx = x - x0
        dy = y - y0
        a = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
        beta = math.atan(dy / dx)
        gama = math.pi / 2 - rot / 180 * math.pi - beta
        rotx = x0 + a * math.sin(gama)
        roty = y0 + a * math.cos(gama)
        new_point = (rotx, roty, point.point_idx)

        return new_point

    def point_rotate(self, sps_data: SpsData):

        self.lockrot = False
        self.lockdxb = False
        self.lockdyb = False

        RLNmaxN = sps_data.get_line_for_max_n_rps()
        minpn = sps_data.get_line_stats_for_rcv_line(RLNmaxN).fp
        maxpn = sps_data.get_line_stats_for_rcv_line(RLNmaxN).lp
        RLn = sps_data.get_n_points_for_rcv_line(RLNmaxN)

        minRP = sps_data.get_point_for_rcv_line_point(RLNmaxN, minpn)
        maxRP = sps_data.get_point_for_rcv_line_point(RLNmaxN, maxpn)

        lenR = math.sqrt(math.pow((minRP.easting - maxRP.easting), 2) +
                         math.pow((minRP.northing - maxRP.northing), 2))
        dRly = maxRP.northing - minRP.northing
        self.rot_rcv = math.acos(dRly / lenR) * 180 / math.pi
        self.d_rcv = lenR / (RLn - 1)

        SLNmaxN = sps_data.get_line_for_max_n_sps()
        minpn = sps_data.get_line_stats_for_src_line(SLNmaxN).fp
        maxpn = sps_data.get_line_stats_for_src_line(SLNmaxN).lp
        SLn = sps_data.get_n_points_for_src_line(SLNmaxN)

        minSP = sps_data.get_point_for_src_line_point(SLNmaxN, minpn)
        maxSP = sps_data.get_point_for_src_line_point(SLNmaxN, maxpn)

        lenS = math.sqrt(math.pow((minSP.easting - maxSP.easting), 2) +
                         math.pow((minSP.northing - maxSP.northing), 2))
        dSly = maxSP.northing - minSP.northing
        self.rot_src = math.acos(dSly / lenS) * 180 / math.pi
        self.d_src = lenS / (SLn - 1)

        if self.rot_rcv < self.rot_src:
            if self.lockrot == False:
                self.rot = self.rot_rcv
            if self.lockdxb == False:
                self.dxb = self.d_src / 2
            if self.lockdyb == False:
                self.dyb = self.rot_rcv / 2
        else:
            if self.lockrot == False:
                self.rot = self.rot_src
            if self.lockdxb == False:
                self.dxb = self.d_rcv / 2
            if self.lockdyb == False:
                self.dyb = self.rot_src / 2

        return lenR, lenS
