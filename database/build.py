from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Boolean, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import os

database = {
    'user': os.environ['DB_USERNAME'],
    'pass': os.environ['DB_PASSWORD'],
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port':  os.environ.get('DB_PORT', 5433),
    'database': os.environ.get('DB_DATABASE', 'datablaster')
}


# Build database
engine = create_engine(
    "postgresql://{user}:{pass}@{host}:{port}/{database}".format(**database))

Base = declarative_base()

class Menu(Base):
    __tablename__ = 'menu'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(Date, nullable=False)
    theme = Column(String)
    continent = Column(String)
    create_date = Column(Date, nullable=False, server_default=func.now())

class Food(Base):
    __tablename__ = 'food'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False)
    menu_id = Column(Integer, ForeignKey("menu.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    item = Column(String, nullable=False)
    allergen_string = Column(String)
    create_date = Column(Date, nullable=False, server_default=func.now())

class FoodTag(Base):
    __tablename__ = 'food_tag'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False)
    food_id = Column(Integer, ForeignKey("food.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    allergen_id = Column(Integer, ForeignKey("allergen.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
    tag = Column(String)
    create_date = Column(Date, nullable=False, server_default=func.now())

class Allergen(Base):
	__tablename__ = 'allergen'
	__table_args__ = {'extend_existing': True}
	id = Column(Integer, primary_key=True, nullable=False)
	code = Column(String)
	name = Column(String)
	create_date = Column(Date, nullable=False, server_default=func.now())


class MenuRating(Base):
    __tablename__ = 'menu_ratings'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(Date, nullable=False)
    n_scores = Column(Integer)
    score_1 = Column(Integer)
    score_2 = Column(Integer)
    score_3 = Column(Integer)
    score_4 = Column(Integer)
    create_date = Column(Date, nullable=False, server_default=func.now())

Base.metadata.create_all(engine)


