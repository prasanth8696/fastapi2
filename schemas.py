from enum import Enum
from pydantic import BaseModel,Field
from datetime import datetime
class SignUpModel(BaseModel):
   username : str
   email : str
   password : str

   class Config :
     orm_mode = True
     example = {
        'example' : {
      'username' : 'Shan',
      'email'    :  'ayyappand464@gmail.com',
       'password' : '12345'

             }

           }

class LoginModel(BaseModel):
   username :str
   password : str


class OrderModel(BaseModel) :
  Payment_method : str
  Address : str
  quantity : int = Field(default=1,ge=1,le=10)
  class Config :
    orm_mode = True

"""    schema_extra = {

            'example' : {
                  'payment_method' : 'Cash on delivery',
                  'address' : 'chennai'}
              } """

class ItemModel(BaseModel):
  name : str
  price : int
  discount : int = Field(default=0,ge=0,le=90)
  quantity = int
  class Config :
    orm_mode = True

class ShowItemModel(BaseModel) :
  id : int
  name : str
  discount : int
  original_price : float
  discounted_price : float
  quantity : int 
  class Config :
    orm_mode = True

class UpdateModel(BaseModel) :
  id : int
  discount : int = Field(default=0,ge=0,le=100)
  quantity : int = Field(default=10)
  class Config :
     orm_mode = True

class ShowAdminModel(BaseModel):
  username : str
  admin : bool
  class Config :
    orm_mode = True

class ShowOrderModel(BaseModel):
  id : int
  item_id : int
  payment_method : str
  amt : float
  quantity : int
  discount : int
  total_amt : float
  procss : str
  address : str
  order_posted : datetime
  order_updated : datetime
  delivered_in : datetime
  class Config :
    orm_mode = True

class UpdateModel(BaseModel) :
  address : str
  class Config :
    orm_mode = True

class ShowUserModel(ShowAdminModel):
  pass
