import os
import datetime
import tempfile
import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from crud import (
    get_all_users, get_user, create_user, update_user,
    add_transaction, get_transactions_last_30_days, get_all_transactions,
    get_goals, add_goal,
    get_recurring_expenses, add_recurring_expense, delete_recurring_expense,
    save_message, get_chat_history, clear_chat_history
)
from tracker import smart_categorize
from simulator import simulate_budget_change
from retriever import retrieve
from prompt_builder import build_prompt
from llm import generate, analyze_image
from config import CURRENCY_SYMBOL, MARKET_CONTEXT

# Import model classes needed for the delete user route
from models import User, Transaction, Goal, RecurringExpense, ChatHistory, SessionLocal

app = Flask(__name__)
CORS(app)

# ---------- Serve the frontend ----------
@app.route("/")
def index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "templates", "index.html")
    if not os.path.exists(html_path):
        return f"Error: index.html not found at {html_path}", 404
    return send_file(html_path)

@app.route("/debug")
def debug():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_path = os.path.join(base_dir, "templates")
    try:
        files = os.listdir(templates_path)
    except FileNotFoundError:
        return f"Folder '{templates_path}' does not exist."
    return f"Files in templates: {files}"

# ---------- User APIs ----------
@app.route("/api/users", methods=["GET"])
def api_get_users():
    users = get_all_users()
    return jsonify([{"id": u.id, "name": u.name, "monthly_income": u.monthly_income} for u in users])

@app.route("/api/users", methods=["POST"])
def api_create_user():
    data = request.json
    name = data.get("name", "New Profile")
    income = data.get("monthly_income", 0)
    user = create_user(name, income)
    return jsonify({"id": user.id, "name": user.name, "monthly_income": user.monthly_income})

@app.route("/api/users/<int:user_id>", methods=["PUT"])
def api_update_user(user_id):
    data = request.json
    update_user(user_id, **data)
    user = get_user(user_id)
    return jsonify({"id": user.id, "name": user.name, "monthly_income": user.monthly_income})

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def api_delete_user(user_id):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        db.close()
        return jsonify({"error": "User not found"}), 404

    # Delete all associated data first (to maintain referential integrity)
    db.query(Transaction).filter(Transaction.user_id == user_id).delete()
    db.query(Goal).filter(Goal.user_id == user_id).delete()
    db.query(RecurringExpense).filter(RecurringExpense.user_id == user_id).delete()
    db.query(ChatHistory).filter(ChatHistory.user_id == user_id).delete()
    # Finally delete the user itself
    db.delete(user)
    db.commit()
    db.close()
    return jsonify({"status": "ok"})

# ---------- Transactions ----------
@app.route("/api/transactions", methods=["POST"])
def api_add_transaction():
    data = request.json
    user_id = data["user_id"]
    add_transaction(user_id, data["amount"], data["category"],
                    datetime.date.fromisoformat(data["date"]),
                    data["description"], data.get("type", "expense"))
    return jsonify({"status": "ok"})

@app.route("/api/transactions/<int:user_id>", methods=["GET"])
def api_get_transactions(user_id):
    days = request.args.get("days", "30")
    if days == "all":
        txns = get_all_transactions(user_id)
    else:
        txns = get_transactions_last_30_days(user_id)
    return jsonify([{
        "id": t.id,
        "amount": t.amount,
        "category": t.category,
        "date": str(t.date),
        "description": t.description,
        "type": t.type
    } for t in txns])

# ---------- Expenses (recurring) ----------
@app.route("/api/expenses/<int:user_id>", methods=["GET"])
def api_get_expenses(user_id):
    exps = get_recurring_expenses(user_id)
    return jsonify([{
        "id": e.id,
        "description": e.description,
        "amount": e.amount,
        "frequency": e.frequency,
        "category": e.category
    } for e in exps])

@app.route("/api/expenses", methods=["POST"])
def api_add_expense():
    data = request.json
    add_recurring_expense(data["user_id"], data["description"],
                          data["amount"], data["frequency"],
                          data.get("category", "bills"))
    return jsonify({"status": "ok"})

@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def api_delete_expense(expense_id):
    delete_recurring_expense(expense_id)
    return jsonify({"status": "ok"})

# ---------- Goals ----------
@app.route("/api/goals/<int:user_id>", methods=["GET"])
def api_get_goals(user_id):
    goals = get_goals(user_id)
    return jsonify([{
        "id": g.id,
        "name": g.name,
        "target_amount": g.target_amount,
        "current_saved": g.current_saved
    } for g in goals])

@app.route("/api/goals", methods=["POST"])
def api_add_goal():
    data = request.json
    add_goal(data["user_id"], data["name"], data["target_amount"])
    return jsonify({"status": "ok"})

# ---------- Chat History ----------
@app.route("/api/history/<int:user_id>", methods=["GET"])
def api_get_history(user_id):
    msgs = get_chat_history(user_id)
    return jsonify([{"role": m.role, "content": m.content, "timestamp": str(m.timestamp)} for m in msgs])

@app.route("/api/history/<int:user_id>", methods=["DELETE"])
def api_clear_history(user_id):
    clear_chat_history(user_id)
    return jsonify({"status": "ok"})

# ---------- Chat (RAG) ----------
@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json
    user_id = data["user_id"]
    prompt = data["prompt"]
    image_b64 = data.get("image")

    save_message(user_id, "user", prompt)

    user = get_user(user_id)
    txns = get_transactions_last_30_days(user_id)
    spend_by_cat = {}
    total_spent = 0
    for t in txns:
        if t.type == "expense":
            spend_by_cat[t.category] = spend_by_cat.get(t.category, 0) + t.amount
            total_spent += t.amount

    expenses = get_recurring_expenses(user_id)
    rec_parts = []
    for e in expenses:
        freq = "once" if e.frequency == "never" else f"per {e.frequency}"
        rec_parts.append(f"{e.description} ₹{e.amount} ({freq})")
    rec_str = "; ".join(rec_parts) if rec_parts else "none"

    goals = get_goals(user_id)
    goal_str = ", ".join([f"{g.name} (₹{g.current_saved}/₹{g.target_amount})" for g in goals]) if goals else "none"

    summary = (
        f"User: {user.name}. Income: ₹{user.monthly_income:.0f}/month. "
        f"Last 30 days: expenses ₹{total_spent:.0f} ({spend_by_cat}). "
        f"Planned expenses: {rec_str}. Goals: {goal_str}. {MARKET_CONTEXT}"
    )

    docs, sources = retrieve(prompt)
    full_prompt = build_prompt(prompt, docs, summary, "")

    temp_path = None
    if image_b64:
        img_data = base64.b64decode(image_b64)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(img_data)
            temp_path = tmp.name

    answer = generate(full_prompt, image_path=temp_path)
    if temp_path:
        os.unlink(temp_path)

    if sources:
        answer += "\n\n📚 *Sources: " + ", ".join(sources) + "*"

    save_message(user_id, "assistant", answer)
    return jsonify({"answer": answer})

# ---------- Simulator ----------
@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    data = request.json
    user = get_user(data["user_id"])
    extra = data["extra_savings"]
    result = simulate_budget_change(user, extra)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True, port=8501)