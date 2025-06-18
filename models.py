from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from datetime import datetime
from .db import db  # notice: from .db, not just from .

class Message(db.Model):
    __tablename__ = 'messages'  

    id = Column(Integer, primary_key=True)
    user_message = Column(String(500))
    bot_response = Column(String(500))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
class Product(db.Model):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String(50), nullable=False)
    image_url = Column(String(500))  # <-- ADD THIS LINE

