#!/usr/bin/python3
"""User class that inherits from base model"""

from models.base_model import BaseModel


class User(BaseModel):
    """defines the user"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
