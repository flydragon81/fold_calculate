from FixedWidthTextParser.Seismic.SpsParser import Point


def create_new_point(line, point, idx):
    data = [
        None,
        line,
        point,
        idx,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None
    ]
    return Point(data)

def create_new_point0(line, point):
    data = [
        None,
        line,
        point,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None
    ]
    return Point(data)
