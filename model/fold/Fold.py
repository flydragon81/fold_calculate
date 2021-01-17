from model.fold.Grid import Grid
from model.SpsData import SpsData
from model.fold.Bin import Bin
from model.Template import Template
from FixedWidthTextParser.Seismic.SpsParser import Point, Relation


class Fold:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.fold: dict = {}  # key is bin number, value is fold object
        osln: float = 0.0
        ospn: float = 0.0
        osidx: float = 0.0
        sln = float
        spn = float
        sidx = int
        rln = float
        frp = float
        trp = float
        rx = float
        ry = float
        bx = float
        by = float

    sps_data = SpsData()
    sps = sps_data.get_sps()
    xps = sps_data.get_xps()
    for s in sps:
        sln = s.line
        spn = s.point
        sidx = s.point_idx
        tem = Template(s)
        for i in range(0, len(tem)):
            rln = tem[i].rcv_line
            frp = tem[i].from_rcv
            trp = tem[i].to_rcv




        pass


