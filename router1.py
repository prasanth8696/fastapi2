from fastapi import APIRouter,Depends,HTTPException
from database import sessionlocal
from models import users
from schemas import SignUpModel,LoginModel
import auth 
from auth import get_db
from sqlalchemy.orm import Session

handler = auth.handler()

router = APIRouter(
          prefix = '/auth',
         tags = ['AUTHENDICATION'])



@router.get('/')
async def welcome():
  return {'status_code' : 200,'msg' : 'welcome to my first api project'}


#signup route
@router.post('/signup',status_code=201)
async def signup(request:SignUpModel,session:Session=Depends(get_db)) :

 db_user = session.query(users).filter(users.username == request.username).first()

 if db_user is not None :
   raise HTTPException(status_code = 500,detail = 'Username with user already exists...')
 if db_user is not None :
  if db_user.email == request.email :
    raise HTTPException(status_code = 500,detail='email with user already exists...')

 new_user = users(
            username = request.username,
            email = request.email,
#            password = handler.get_pass_hash(request.password))
            password = request.password
           )
 session.add(new_user)
 session.commit()
 return {'status_code' : 201 , 'msg' : 'User Successfully created...'}

#sign in route
@router.post('/signin',status_code=200)
async def login(request:LoginModel,session:Session=Depends(get_db)) :

  db_user = session.query(users).filter(users.username==request.username).first()

  if db_user is None :

     raise HTTPException(status_code=401,detail='user doesn\'t exist')
  if db_user :
    if db_user.password != request.password:
     raise HTTPException(status_code=401,detail='Invalid password')
    data = {'username' : db_user.username,'admin' : db_user.admin,'owner' :db_user.owner}
    token = handler.encode_token(data)
    return {'access_token' : token ,'token_type' :'bearer'}

