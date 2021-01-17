from sqlalchemy import Column, Float, Integer
from SpsDataDb.entity.Base import Base


class Bin(Base):
    __tablename__ = 'bin'
    id = Column(Integer, primary_key=True)
    column = Column(Integer)
    row = Column(Integer)
    fold = Column(Integer)
    easting = Column(Float)
    northing = Column(Float)
    easting_r = Column(Float)
    northing_r = Column(Float)
