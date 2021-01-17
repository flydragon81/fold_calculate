import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from SpsDataDb.entity.Base import Base
from SpsDataDb.entity.Sps import Sps
from SpsDataDb.entity.Rps import Rps
from SpsDataDb.entity.Template import Template, Xps
from FixedWidthTextParser.Seismic.SpsParser import Sps21Parser
from SpsDataDb.SpsDataDb import SpsDataDb


class MyTestCase(unittest.TestCase):
    def test_loading(self):
        sql_file = 'data/test.sqlite'
        engine = create_engine('sqlite:///' + sql_file, echo=False)
        session = sessionmaker()
        session.configure(bind=engine)
        Base.metadata.create_all(engine)

        parser = Sps21Parser()

        s = session()
        sps_data = SpsDataDb(parser, s)

        # r_filename = 'data/001.R'
        # s_filename = 'data/001.S'
        # x_filename = 'data/001.X'
        #
        # sps_data.load_s(s_filename)
        # sps_data.load_r(r_filename)
        # sps_data.load_x(x_filename)


if __name__ == '__main__':
    unittest.main()
