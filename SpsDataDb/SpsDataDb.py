from sqlalchemy.orm import session
from FixedWidthTextParser.Seismic.SpsParser import SpsParser, Point, Relation
from SpsDataDb.entity.Sps import Sps
from SpsDataDb.entity.Rps import Rps
from SpsDataDb.entity.Template import Template, Xps


class SpsDataDb:
    COMMIT_X_EVERY = 100000

    def __init__(self, parser: SpsParser, ses: session):
        self.__session: session = ses
        self.__parser = parser

    def load_x(self, filename):
        osln = 0.0
        ospn = 0.0
        osidx = 0

        counter = 0
        with open(filename, mode='r', buffering=(2 << 16) + 8) as sps:
            line = sps.readline()
            while line:
                counter += 1
                parsed = self.__parser.parse_relation(line)
                if parsed is not None:
                    r = Relation(parsed)
                    xps = Xps(sline=r.line, spoint=r.point, sidx=r.point_idx, from_ch=r.from_channel,
                              to_ch=r.to_channel, rline=r.rcv_line, from_rp=r.from_rcv, to_rp=r.to_rcv, ridx=r.rcv_idx)
                    self.__session.add(xps)
                    sln = r.line
                    spn = r.point
                    spidx = r.point_idx

                    if sln == osln and spn == ospn and spidx == osidx:
                        template.relations.append(xps)
                    else:
                        template = Template()
                        template.sline = sln
                        template.spoint = spn
                        template.sidx = spidx
                        template.relations.append(xps)
                        self.__session.add(template)

                    osln = sln
                    ospn = spn
                    osidx = spidx
                line = sps.readline()

                if self.COMMIT_X_EVERY == counter:
                    self.__session.commit()
                    counter = 0

        self.__session.commit()

        # last template
        # if template is not None:
        #     templates.append(template)

    def load_s(self, filename):
        points = self.__load_points(filename)
        p: Point
        for p in points:
            point = Sps(line=p.line, point=p.point, idx=p.point_idx, easting=p.easting, northing=p.northing)
            self.__session.add(point)

        self.__session.commit()

    def load_r(self, filename):
        points = self.__load_points(filename)
        p: Point
        for p in points:
            point = Rps(line=p.line, point=p.point, idx=p.point_idx, easting=p.easting, northing=p.northing)
            self.__session.add(point)

        self.__session.commit()

    def __load_points(self, filename):
        points = []
        with open(filename) as handle:
            line = handle.readline()
            while line:
                parsed = self.__parser.parse_point(line)
                if parsed is not None:
                    points.append(Point(parsed))
                line = handle.readline()
        return points

    def get_all_s(self):
        return self.__session.query(Sps).all()

    def get_all_x(self):
        return self.__session.query(Template).all()

    def get_all_r(self):
        return self.__session.query(Rps).all()

    def get_all_r4line(self, line: float):
        return self.__session.query(Rps).filter_by(line=line)

    def get_r4line_range_points(self, line: float, frp: float, trp: float):
        return self.__session.query(Rps).filter(Rps.line == line, Rps.point >= frp, Rps.point <= trp)

    def get_s(self, line: float, point: float, idx: int) -> Sps:
        return self.__session.query(Sps).filter_by(line=line, point=point, idx=idx).first()

    def get_r(self, line: float, point: float, idx: int) -> Rps:
        return self.__session.query(Rps).filter_by(line=line, point=point, idx=idx).first()
