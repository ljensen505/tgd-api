import os
from dotenv import load_dotenv

load_dotenv()

DB: str = os.getenv("DB")  # type: ignore
if DB is None:
    raise Exception("could not find db name")
