from model.SpsData import SpsData
from model.Stats import Stats
import unittest
from FixedWidthTextParser.Seismic.SpsParser import Point
from var_dump import var_dump
from model.fold.Grid import Grid


class TestSpsData(unittest.TestCase):
    def test_load(self):
        sps_data = SpsData()

        r_filename = 'data/001.R'
        s_filename = 'data/001.S'
        x_filename = 'data/001.X'
        sps_data.load_all(r_filename, s_filename, x_filename)

        # sps_data.set_sps(s_filename)
        self.assertEqual(84, len(sps_data.get_sps()))

        # sps_data.set_rps(r_filename)
        self.assertEqual(4770, len(sps_data.get_rps()))

        # sps_data.set_xps(x_filename)
        self.assertEqual(84, len(sps_data.get_xps()))

        # sps_data.calculate_stats()
        rst = sps_data.get_status_rps()
        # print(type(rst))
        status: Stats
        # for status in rst:
        #     print(status.ln, status.n, status.fp, status.lp)
        self.assertEqual(15, len(rst))
        sst = sps_data.get_status_sps()
        # print(type(sst))
        # for status in sst:
        #     print(status.ln, status.n, status.fp, status.lp)
        self.assertEqual(4, len(sst))

        xst = sps_data.get_xps()
        # print(len(xst))

        maxrl = sps_data.get_line_for_max_n_rps()
        self.assertEqual(1001, maxrl)

        maxsl = sps_data.get_line_for_max_n_sps()
        self.assertEqual(5001, maxsl)

        rlnum = sps_data.get_n_points_for_rcv_line(1001)
        self.assertEqual(318, rlnum)

        slnum = sps_data.get_n_points_for_src_line(5001)
        self.assertEqual(21, slnum)

        # rlst: Stats = sps_data.get_line_stats_for_rcv_line(maxrl)
        # # print(rlst.ln, rlst.n, rlst.fp, rlst.lp)
        # self.assertEqual(5318.0, rlst.lp)
        #
        # slst: Stats = sps_data.get_line_stats_for_src_line(maxsl)
        # # print(slst.ln, slst.n, slst.fp, slst.lp)
        # self.assertEqual(34600.0, slst.fp)
        #
        # rlpoint: Point = sps_data.get_point_for_rcv_line_point(rlst.ln, rlst.fp)
        # # print(rlpoint.line, rlpoint.easting)
        # self.assertEqual(767331.7, rlpoint.easting)
        #
        # slpoint: Point = sps_data.get_point_for_src_line_point(slst.ln, slst.fp)
        # # print(slpoint.line, slpoint.easting)
        # self.assertEqual(841381.3, slpoint.easting)
        #
        # rps_dict = sps_data.get_rps_dict()
        # for i in rps_dict.values():
        #     pass
