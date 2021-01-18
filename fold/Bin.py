from sqlalchemy import Column, Float, Integer


class Bin:
    bn = int
    column = int
    row = int
    fold = int
    easting = float
    northing = float
    easting_r = float
    northing_r = float
