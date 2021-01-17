from model.SpsData import SpsData
from model.Stats import Stats
import unittest
from FixedWidthTextParser.Seismic.SpsParser import Point
from var_dump import var_dump
from model.fold.Grid import Grid
from model.helpers import create_new_point_x_y, create_new_point_ln_pn_idx


class MyTestCase(unittest.TestCase):
    # def test_grid(self):
    #     r_file_name = 'data/001.R'
    #     s_file_name = 'data/001.S'
    #     x_file_name = 'data/001.X'
    #     sps_data = SpsData()
    #     sps_data.load_all(r_file_name, s_file_name, x_file_name)
    #
    #     grid = Grid()
    #     grid.calculate_corners(sps_data)
    #     c0: Point = grid.get_corners()
    #     # print(c0[0].easting)
    #     self.assertEqual(767331.7, c0[0].easting)
    #     # print(c0[2].easting)
    #     self.assertEqual(783181.7, c0[2].easting)
    #     # print(c0[1].northing)
    #     self.assertEqual(2601551.3, c0[1].northing)
    #     # print(c0[3].northing)
    #     self.assertEqual(2605751.3, c0[3].northing)
    #
    #     rot = grid.point_rotate(sps_data)
    #     #       print(grid.rot_rcv, grid.rot_src)
    #
    #     ori = grid.calculate_grid_origin(sps_data)
    #     #        print(ori, grid.dyb, grid.dxb)
    #
    #     print(c0[2].easting, c0[2].northing)
    #     rotated = grid.point_rotate_x_y(c0[3], False)
    #     #       print(rotated)
    #     print(c0[2].easting)
    #     print(round(rotated.easting, 1), rotated.northing)
    #
    #     ratated_back = grid.point_rotate_x_y(rotated, True)
    #     print(ratated_back.easting, ratated_back.northing)

    def test_read_write_object(self):
        grid = Grid(767331.7, 2601551.3, 30.0, 25.0, 12.5, 1000, 2000)
        filename = 'data/grid.pickle'
        grid.write_object(filename)
        new_grid = Grid.read_object(filename)

        self.assertEqual(grid.get_x0(), new_grid.get_x0())

    def test_read_write(self):
        grid = Grid(767331.7, 2601551.3, 30.0, 25.0, 12.5, 1000, 2000)
        filename = 'data/grid.json'
        grid.write(filename)

        new_grid = Grid()
        new_grid.read(filename)

        self.assertEqual(grid.get_x0(), new_grid.get_x0())



if __name__ == '__main__':
    unittest.main()
