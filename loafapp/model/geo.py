from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from geoalchemy import *
import geoalchemy as geo

metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)


class Spot(Base):
    __tablename__ = 'spots'
    id = Column(ga.Integer, primary_key=True)
    name = Column(ga.Unicode, nullable=False)
    height = Column(ga.Integer)
    created = Column(ga.DateTime, default=datetime.now())
    geom = geo.GeometryColumn(Point(2))


class Path(Base):
    __tablename__ = 'pathes'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    width = Column(Integer)
    created = Column(DateTime, default=datetime.now())
    geom = geo.GeometryColumn(LineString(2))


class Area(Base):
    __tablename__ = 'areas'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    depth = Column(Integer)
    created = Column(DateTime, default=datetime.now())
    geom = geo.GeometryColumn(Polygon(2))

geo.GeometryDDL(Spot.__table__)
geo.GeometryDDL(Path.__table__)
geo.GeometryDDL(Area.__table__)
