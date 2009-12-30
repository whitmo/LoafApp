from datetime import datetime
from loafapp.model import DeclarativeBase
from sqlalchemy import *
import geoalchemy as geo

import pdb;pdb.set_trace()
class Spot(DeclarativeBase):
    __tablename__ = 'spots'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=True)
    text = Column(UnicodeText, nullable=True)
    image_path = Column(Unicode, nullable=True)
    altitude = Column(Float)
    accuracy = Column(Float)
    alt_accuracy = Column(Float)
    heading = Column(Integer)
    speed = Column(Float)
    created = Column(DateTime, default=datetime.now())
    geom = geo.GeometryColumn(geo.Point(2))

geo.GeometryDDL(Spot.__table__)

## class Path(DeclarativeBase):
##     __tablename__ = 'paths'
##     id = Column(Integer, primary_key=True)
##     name = Column(Unicode, nullable=False)
##     width = Column(Integer)
##     created = Column(DateTime, default=datetime.now())
##     geom = geo.GeometryColumn(geo.LineString(2))


## class Area(DeclarativeBase):
##     __tablename__ = 'areas'
##     id = Column(Integer, primary_key=True)
##     name = Column(Unicode, nullable=False)
##     depth = Column(Integer)
##     created = Column(DateTime, default=datetime.now())
##     geom = geo.GeometryColumn(geo.Polygon(2))
