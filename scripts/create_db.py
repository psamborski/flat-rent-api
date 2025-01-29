from database.database import Base, engine
from database.schemas import *


try:
    Base.metadata.create_all(bind=engine)
    print("Database created successfully")
except Exception as e:
    print(f"Error occurred during database creation: {e}")
finally:
    engine.dispose()