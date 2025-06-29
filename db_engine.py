from sqlalchemy import create_engine
import os


# ✅ Get DATABASE_URL from your .env or Render deployment
DATABASE_URL = "postgresql://ghanagokulgabburi:Saibaba3123@127.0.0.1:5432/housing_db"

# ✅ Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
