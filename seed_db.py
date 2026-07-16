# seed_db.py
from models import SessionLocal, User, Base, engine

# Ensure tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Check if user already exists
if not db.query(User).filter(User.id == 1).first():
    db.add(User(id=1, username="sumit", monthly_income=5000))
    db.commit()
    print("Test user created.")
else:
    print("User already exists.")

db.close()