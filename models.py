from database import Base

from sqlalchemy import Column,Integer,String,Text,Boolean,ForeignKey,Float,DateTime

from sqlalchemy.orm import relationship

from datetime import datetime,timedelta

class users(Base):
   __tablename__ = 'user'

   id = Column(Integer,primary_key=True)
   username = Column(String,unique=True ,nullable=False)
   email = Column(String,nullable=False)
   admin = Column(Boolean,default=False)
   owner = Column(Boolean,default=False)
   password = Column(Text)
   orders = relationship('orders',backref='user')

class orders(Base) :
  __tablename__ = 'order'
  id = Column(Integer,primary_key=True)
  item_id = Column(Integer)
  procss = Column(String,default='pending')
  payment_method = Column(String)
  discount = Column(Integer)
  quantity = Column(Integer)
  order_posted = Column(DateTime,default=datetime.utcnow())
  order_updated = Column(DateTime,default=datetime.utcnow())
  delivered_in = Column(DateTime,default=datetime.utcnow() + timedelta(days=10))
  address = Column(String,nullable=False)
  amt = Column(Float)
  total_amt = Column(Float)
  user_id = Column(Integer,ForeignKey('user.id'))

class items(Base) :
  __tablename__ = 'item'
  id = Column(Integer,primary_key=True)
  name = Column(String(255),unique=True)
  discount = Column(Integer,default= 0)
  original_price = Column(Float)
  discounted_price = Column(Float)
  quantity = Column(Integer,default = 10)

