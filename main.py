import FixedWidthTextParser
from FixedWidthTextParser.Seismic.SpsParser import Sps21Parser, Point, Relation


def main():
    parser = Sps21Parser()
    filename = 'data/data.S'
    with open(filename) as sps:
        line = sps.readline()
        while line:
            parsed = parser.parse_point(line)
            if parsed is not None:
                point = Point(parsed)
                print(point.line, point.point)
            line = sps.readline()

    filename = 'data/data.X'

    with open(filename) as sps:
        line = sps.readline()
        while line:
            parsed = parser.parse_relation(line)
            if parsed is not None:
                relation = Relation(parsed)
                print(relation.type,relation.line,relation.ffid)
            line = sps.readline()


if __name__ == '__main__':
    main()
