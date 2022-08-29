from fastapi import APIRouter,HTTPException
from database import sessionlocal
from models import items
from typing import List
from schemas import ShowItemModel
from starlette.responses import RedirectResponse
session = sessionlocal()

home = APIRouter(
                 tags = ['HOME'])

@home.get('/')
async def get_doc():
 return RedirectResponse('/docs')

@home.get('/items',status_code=200,response_model=List[ShowItemModel])
async def get_items():
  items_values = session.query(items).all()
  if items_values :
    return items_values
  else :
   raise HTTPException(status_code=404,detail='Currently dont have items...')
@home.get('/{item_id}',status_code=200,response_model=ShowItemModel)
async def get_item_one(item_id : int):
  current_item = session.query(items).filter(items.id == item_id).first()
  if current_item :
    return current_item
  else :
    raise HTTPException(status_code=404,detail='Item Not Found...')
