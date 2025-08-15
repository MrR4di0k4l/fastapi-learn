from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# ایجاد مدل پایه برای SQLAlchemy
Base = declarative_base()

# URL پایگاه داده SQLite
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# for postgres or other relational databases
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver:5432/db"
# SQLALCHEMY_DATABASE_URL = "mysql://username:password@localhost/db_name"


# ایجاد موتور برای اتصال به پایگاه داده
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# ساخت session ساز برای تعامل با پایگاه داده
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ایجاد جداول در پایگاه داده (در صورت نیاز)
# Base.metadata.create_all(bind=engine)


# تابع برای گرفتن session از SessionLocal
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()