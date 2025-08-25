import os
from psycopg import connect
from dotenv import load_dotenv
load_dotenv()

def connectDB():
    return connect(
        host=os.getenv("PGHOST"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        port=os.getenv("PGPORT"),
        sslmode="require"
    )

def loadAPI():
    return os.getenv("API")

def loadURL():
   return f"postgresql+psycopg2://{os.getenv("PGUSER")}:{os.getenv("PGPASSWORD")}@{os.getenv("PGHOST")}:{os.getenv("PGPORT")}/{os.getenv("PGDATABASE")}"