import jwt
from fastapi import HTTPException,Depends,Security
from datetime import datetime,timedelta
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from passlib.context import CryptContext

def get_db():
  session = sessionlocal()
  try :
    yield session
  finally :
     session.close()
    


class handler :
  secret = '51df9e6ea2cfea119c4073e301cce7c9'
  security = HTTPBearer()
  pwd_context = CryptContext(['bcrypt'],deprecated ='auto')

  def get_pass_hash(self,password):
    return self.pwd_context.hash(password)
  def verify_password(self,plain_password,hash_password):
    return self.pwd_context.verify(plain_password,hash_password)


  def encode_token(self,sub):
    payload = {
                'exp' : datetime.utcnow()+timedelta(days=0,minutes=10),
                'iat' : datetime.utcnow(),
                 'sub' : sub }
    token = jwt.encode(
          payload,
          self.secret,
          algorithm = 'HS256')
    return token


  def decode_token(self,token) :
     try :
       payload = jwt.decode(token,self.secret,algorithms=['HS256'])
     
     except jwt.ExpiredSignatureError :

       raise HTTPException(status_code=401,detail='Token Expired')

     except jwt.InvalidTokenError :

       raise HTTPException(status_code=401,detail='Invalid Token')

     return payload['sub']

  def verify(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
