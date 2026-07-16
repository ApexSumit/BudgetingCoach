from sqlalchemy.orm import Session
from models import SessionLocal, User, Transaction, Goal, RecurringExpense, ChatHistory
from datetime import date, timedelta

# ---------- Users ----------
def create_user(name, monthly_income=0.0):
    db = SessionLocal()
    user = User(name=name, monthly_income=monthly_income)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def get_all_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

def get_user(user_id):
    db = SessionLocal()
    return db.query(User).filter(User.id == user_id).first()

def update_user(user_id, **kwargs):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.commit()
    db.close()

# ---------- Transactions ----------
def add_transaction(user_id, amount, category, txn_date, description, txn_type="expense"):
    db = SessionLocal()
    txn = Transaction(user_id=user_id, amount=amount, category=category, date=txn_date, description=description, type=txn_type)
    db.add(txn)
    db.commit()
    db.close()

def get_transactions_last_30_days(user_id):
    db = SessionLocal()
    cutoff = date.today() - timedelta(days=30)
    txns = db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.date >= cutoff).all()
    db.close()
    return txns

def get_all_transactions(user_id):
    db = SessionLocal()
    txns = db.query(Transaction).filter(Transaction.user_id == user_id).order_by(Transaction.date.desc()).all()
    db.close()
    return txns

# ---------- Goals ----------
def get_goals(user_id):
    db = SessionLocal()
    goals = db.query(Goal).filter(Goal.user_id == user_id).all()
    db.close()
    return goals

def add_goal(user_id, name, target_amount):
    db = SessionLocal()
    goal = Goal(user_id=user_id, name=name, target_amount=target_amount)
    db.add(goal)
    db.commit()
    db.close()

def update_goal_saved(goal_id, amount):
    db = SessionLocal()
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if goal:
        goal.current_saved += amount
        db.commit()
    db.close()

# ---------- Recurring Expenses ----------
def get_recurring_expenses(user_id):
    db = SessionLocal()
    recurring = db.query(RecurringExpense).filter(RecurringExpense.user_id == user_id).all()
    db.close()
    return recurring

def add_recurring_expense(user_id, description, amount, frequency, category="bills"):
    db = SessionLocal()
    rec = RecurringExpense(user_id=user_id, description=description, amount=amount, frequency=frequency, category=category)
    db.add(rec)
    db.commit()
    db.close()

def delete_recurring_expense(expense_id):
    db = SessionLocal()
    db.query(RecurringExpense).filter(RecurringExpense.id == expense_id).delete()
    db.commit()
    db.close()

# ---------- Chat History ----------
def save_message(user_id, role, content):
    db = SessionLocal()
    msg = ChatHistory(user_id=user_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.close()

def get_chat_history(user_id):
    db = SessionLocal()
    history = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.timestamp).all()
    db.close()
    return history

def clear_chat_history(user_id):
    db = SessionLocal()
    db.query(ChatHistory).filter(ChatHistory.user_id == user_id).delete()
    db.commit()
    db.close()