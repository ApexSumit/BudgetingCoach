from models import Base, engine, SessionLocal, User

# Ensure all tables exist (safe to call multiple times)
Base.metadata.create_all(bind=engine)
print("Tables checked/created.")

db = SessionLocal()
user = db.query(User).filter(User.id == 1).first()

if user is None:
    db.add(User(id=1, username="sumit", monthly_income=5000))
    db.commit()
    print("Test user (sumit) created with $5000 income.")
else:
    print(f"User already exists: {user.username}, income=${user.monthly_income:.0f}")

db.close()