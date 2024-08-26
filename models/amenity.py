#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchhemy import Column, String


class Amenity(BaseModel):
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
