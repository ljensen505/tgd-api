import os
from dotenv import load_dotenv

load_dotenv()

db: str = os.getenv("db")  # type: ignore
if db is None:
    raise Exception("could not find db name")
