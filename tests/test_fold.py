import unittest
from fold.Grid import Grid
from fold.Bin import Bin
from fold.Fold import Fold


class MyTestCase(unittest.TestCase):
    def test_fold(self):
        rfile = 'data/001.R'
        sfile = 'data/001.S'
        xfile = 'data/001.X'
        gfile = 'data/test-simple-grid.json'
        fold_csv = 'data/fold_result.csv'
        grid = Grid()
        grid.read(gfile)
        fold = Fold(grid)
        fold.set_rps(rfile)
        fold.set_sps(sfile)
        fold.load_sps()
        fold.calculate_fold(xfile)

        fold.write_fold_to_csv(fold_csv)



if __name__ == '__main__':
    unittest.main()
