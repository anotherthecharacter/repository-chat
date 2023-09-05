from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@127.0.0.1:5432/repository_chat")
Session = sessionmaker(bind=engine)
