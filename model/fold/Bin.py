from class_attr_check import auto_attr_check
from typing import final


@auto_attr_check
@final
class Bin:
    column = int
    row = int
    number = int
    fold = int
    x = float
    y = float
    xr = float
    yr = float
