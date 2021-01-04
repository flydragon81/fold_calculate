from model.SpsData import SpsData
from model.Stats import Stats
import unittest
from FixedWidthTextParser.Seismic.SpsParser import Point
from var_dump import var_dump
from model.fold.Grid import Grid


class TestSpsData(unittest.TestCase):
    def test_load(self):
        sps_data = SpsData()

        filename = 'data/data.S'
        sps_data.set_sps(filename)
        self.assertEqual(537, len(sps_data.get_sps()))

        filename = 'data/001.R'
        sps_data.set_rps(filename)
        self.assertEqual(4770, len(sps_data.get_rps()))

        filename = 'data/001.X'
        sps_data.set_xps(filename)
        self.assertEqual(84, len(sps_data.get_xps()))

        sps_data.calculate_stats()
        rst = sps_data.get_status_rps()
        print(type(rst))
        status: Stats
        for status in rst:
            print(status.ln, status.n, status.fp, status.lp)
        sst = sps_data.get_status_sps()
        print(type(sst))
        for status in sst:
            print(status.ln, status.n, status.fp, status.lp)

        maxrl = sps_data.get_line_for_max_n_rps()
        self.assertEqual(1001, maxrl)

        maxsl = sps_data.get_line_for_max_n_sps()
        self.assertEqual(26584, maxsl)

        rlnum = sps_data.get_n_points_for_rcv_line(1001)
        self.assertEqual(318, rlnum)

        slnum = sps_data.get_n_points_for_src_line(26584)
        self.assertEqual(35, slnum)

        rlst = sps_data.get_line_stats_for_rcv_line(maxrl)
        print(rlst.ln, rlst.n, rlst.fp, rlst.lp)

        slst = sps_data.get_line_stats_for_src_line(maxsl)
        print(slst.ln, slst.n, slst.fp, slst.lp)

        rlpoint = sps_data.get_point_for_rcv_line_point(rlst.ln, rlst.fp)
        print(rlpoint.line,rlpoint.easting)

        slpoint = sps_data.get_point_for_src_line_point(slst.ln, slst.fp)
        print(slpoint.line,slpoint.easting)


        gr = Grid()
        length = gr.point_rotate(sps_data)
        print(length)
