from os import environ
from dotenv import load_dotenv

load_dotenv()


DB_USER = environ["DB_USER"]
DB_PASSWORD = environ["DB_PASSWORD"]
DB_HOST = environ["DB_HOST"]
DB_NAME = environ["DB_NAME"]
TEST_DB_NAME = environ.get("TEST_DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
