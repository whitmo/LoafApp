from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import MetaData
from sqlalchemy import *
import geoalchemy as geo
from loafapp.model import DeclarativeBase


class Spot(DeclarativeBase):
    __tablename__ = 'spots'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    height = Column(Integer)
    created = Column(DateTime, default=datetime.now())
    geom = geo.GeometryColumn(geo.Point(2))


class Path(DeclarativeBase):
    __tablename__ = 'paths'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    width = Column(Integer)
    created = Column(DateTime, default=datetime.now())
    geom = geo.GeometryColumn(geo.LineString(2))


class Area(DeclarativeBase):
    __tablename__ = 'areas'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    depth = Column(Integer)
    created = Column(DateTime, default=datetime.now())
    geom = geo.GeometryColumn(geo.Polygon(2))

geo.GeometryDDL(Spot.__table__)
geo.GeometryDDL(Path.__table__)
geo.GeometryDDL(Area.__table__)
