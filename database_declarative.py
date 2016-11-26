
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
class StockQuote(Base):
    __tablename__ = 'contacts'
    # Here we define columns for the contact people
    # Each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    indice = Column(String(250), nullable = False)
    latest_value = Column(Float, nullable = False)
    local_value = Column(Float, nullable  = False)
    date_modified = Column(DateTime, nullable= False)
 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_backend.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)