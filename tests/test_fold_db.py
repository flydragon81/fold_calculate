import unittest
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from SpsDataDb.entity.Base import Base
from FixedWidthTextParser.Seismic.SpsParser import Sps21Parser, Point
from SpsDataDb.SpsDataDb import SpsDataDb
from FoldDb.Fold import Fold
from FoldDb.Grid import Grid
from SpsDataDb.entity.Sps import Sps
from SpsDataDb.entity.Rps import Rps
from SpsDataDb.entity.Template import Template, Xps
from SpsDataDb.entity.Bin import Bin

from var_dump import var_dump


class MyTestCase(unittest.TestCase):
    def test_simple(self):
        sql_file = 'data/test-simple.sqlite'

        engine = create_engine('sqlite:///' + sql_file, echo=False)
        # engine = create_engine('postgresql://test:test@postgres-test.lxd/gr3d')
        session = sessionmaker()
        session.configure(bind=engine)
        Base.metadata.create_all(engine)

        s = session()
        parser = Sps21Parser()
        sps_db = SpsDataDb(parser, s)

        # filename_s = 'data/001.S'
        # filename_r = 'data/001.R'
        # filename_x = 'data/001.X'
        #
        # sps_db.load_s(filename_s)
        # sps_db.load_r(filename_r)
        # sps_db.load_x(filename_x)

        grid_file = 'data/test-simple-grid.json'

        grid = Grid()
        grid.read(grid_file)

        fold = Fold(grid)

        fold.calculate_fold(sps_db)

        for f in fold.get_fold():
            if f > 0:
                print(f)


if __name__ == '__main__':
    unittest.main()
