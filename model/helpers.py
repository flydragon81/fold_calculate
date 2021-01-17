from FixedWidthTextParser.Seismic.SpsParser import Point


def create_new_point_ln_pn_idx(line, point, idx):
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


def create_new_point_ln_pn(line, point):
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


def create_new_point_x_y(x, y,idx):
    data = [
        None,
        None,
        None,
        idx,
        None,
        None,
        None,
        None,
        None,
        x,
        y,
        None,
        None,
        None,
        None
    ]
    return Point(data)
