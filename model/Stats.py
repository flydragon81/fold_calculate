from typing import final
from class_attr_check import auto_attr_check


@auto_attr_check
@final
class Stats:
    ln = float  # line number
    n = int  # number of points per line
    fp = float  # first point number at line
    lp = float  # last point number at line


