from SpsDataDb.entity.Base import Base
from SpsDataDb.entity.Point import Point


class Rps(Base, Point):
    __tablename__ = 'rps'
