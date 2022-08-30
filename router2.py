
from fastapi import APIRouter,HTTPException,Depends
from models import orders,users,items
from database import sessionlocal
import auth
from auth import get_db
from sqlalchemy.orm import Session
from admin import discount
from schemas import OrderModel,ShowOrderModel,OrderUpdateModel
from typing import List
from datetime import datetime


handler = auth.handler()
protected = Depends(handler.verify)
order = APIRouter(
         prefix = '/order',
         tags = ['ORDERS'] )

def get_current_user(payload):
  return session.query(users).filter(users.username==payload['username']).first()


#post the order

@order.post('/place_order/{item_id}',status_code = 201,response_model=ShowOrderModel) 
def place_order(item_id : int ,request: OrderModel,payload = protected,session:Session=Depends(get_db)) :
    current_user = payload['username']

  
    user_details = session.query(users).filter(users.username == current_user).first()
    item = session.query(items).filter(items.id == item_id).first()
    if item is None :
      raise HTTPException(status_code=400,detail='Item Not Found')

    discount = item.discount
    if request.quantity > item.quantity :
      raise HTTPException(status_code=400,detail='check available quantity')

    discount_amt = request.quantity * (item.discounted_price) 
    #if admin discount is 10 % more
    if payload['admin'] :
        discount_amt = discount(item.discounted_price,10)
        discount += 10
    new_order = orders(
              payment_method = request.Payment_method,
              total_amt = discount_amt,
              amt = item.discounted_price,
              address = request.Address,
              item_id = item_id,
              quantity = request.quantity,
              discount = discount
              )
    
    new_order.user = user_details
    new_order.procss  = 'Order Confirmed'
    session.add(new_order)
    item.quantity = item.quantity - request.quantity
    session.commit()
    session.refresh(new_order)

    return new_order


#Get order details
@order.get('/get_order/{order_id}',status_code=200,response_model=ShowOrderModel)
async def get_order(order_id : int,payload = protected,session:Session=Depends(get_db)):
  order_details = session.query(orders).filter(orders.id == order_id).first()
  if order_details is  None :
    raise HTTPException(status_code=400,detail = 'Item Not Found')
  #users only have permission to view own orders only
  if payload['username'] != order_details.user.username :
    raise HTTPException(status_code=400,detail=f'you dont have orders with id {item_id}')
  else :
    return order_details


# get user--> all orders
@order.get('/get_orders',status_code=200,response_model = List[ShowOrderModel])
async def get_orders(payload =  protected,session:Session=Depends(get_db)):
  current_user = get_current_user(payload)

  # get orders using relationships
  orders_all = current_user.orders
  if orders_all is None  :
    raise HTTPException(status_code=404,detail='Orders Not Found...')
  return orders_all


#update the orders
@order.put('/update_order/{order_id}',status_code=201,response_model=ShowOrderModel)
async def update_order(order_id : int,request:OrderUpdateModel,payload=protected,session:Session=Depends(get_db)):
   current_user = get_current_user(payload)

   curr_order = session.query(orders).filter(orders.id == order_id).first()
   if curr_order is None or curr_order.user != current_user :
     raise  HTTPException(status_code=404,detail=f'you dont have orders with id {order_id}')
   curr_order.address = request.address
   curr_order.order_updated = datetime.utcnow()
   session.commit()
   session.refresh(curr_order)
   return curr_order

#Delete the orders

@order.delete('/delete/{order_id}',status_code=204)
async def delete_order(order_id :int,payload = protected,session:Session=Depends(get_db)):
  current_user = get_current_user(payload)
  curr_order = session.query(orders).filter(orders.id==order_id).first()
  if curr_order is None or curr_order.user != current_user:
    raise HTTPException(status_code=404,detail='Order Not Found')

  #else delete the order
  session.delete(curr_order)
  session.commit()


