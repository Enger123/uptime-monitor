from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from main import app
from app.db.session import get_db
 
test_db = create_engine(
    "postgresql+psycopg://postgres:Enger123@localhost:5432/monitor_api_test"
    , poolclass=NullPool
    )
TestSession = sessionmaker(bind=test_db)

def test_get_db():
    db = TestSession()
    try:
        yield db
    finally: 
        db.close() 

app.dependency_overrides[get_db] = test_get_db
