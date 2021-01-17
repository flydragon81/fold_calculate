from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from SpsDataDb.entity.Base import Base


class Template(Base):
    __tablename__ = 'template'
    id = Column(Integer, primary_key=True)
    sline = Column(Float)
    spoint = Column(Float)
    sidx = Column(Integer)
    relations = relationship("Xps", back_populates='template')


class Xps(Base):
    __tablename__ = 'xps'
    id = Column(Integer, primary_key=True)
    sline = Column(Float)
    spoint = Column(Float)
    sidx = Column(Integer)
    from_ch = Column(Integer)
    to_ch = Column(Integer)
    rline = Column(Float)
    from_rp = Column(Float)
    to_rp = Column(Float)
    ridx = Column(Integer)
    template = relationship("Template")
    template_id = Column(Integer, ForeignKey('template.id'))
