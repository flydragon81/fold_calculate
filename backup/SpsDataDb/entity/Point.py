from sqlalchemy import Column, Float, Integer


class Point:
    id = Column(Integer, primary_key=True)
    line = Column(Float)
    point = Column(Float)
    idx = Column(Integer)
    easting = Column(Float)
    northing = Column(Float)
