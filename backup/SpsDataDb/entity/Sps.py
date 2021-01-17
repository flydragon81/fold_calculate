from SpsDataDb.entity.Base import Base
from SpsDataDb.entity.Point import Point


class Sps(Base, Point):
    __tablename__ = 'sps'
