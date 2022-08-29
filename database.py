from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://up9yoqg3nwrxfd3ivvhn:KmLZT8cfN6PxXBjCLGCI@bxhnxyjsoujhavq4refz-postgresql.services.clever-cloud.com:5432/bxhnxyjsoujhavq4refz'

engine = create_engine(SQLALCHEMY_DATABASE_URL)


sessionlocal  = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()
