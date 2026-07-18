def simulate_budget_change(user, extra_savings_per_month):
    current_savings = user.monthly_income * 0.2  # assuming 20% savings rate
    new_savings = current_savings + extra_savings_per_month
    emergency_fund_goal = 1000  # example
    months_to_ef = emergency_fund_goal / new_savings if new_savings > 0 else float("inf")
    impact = (
        f"If you save an extra ${extra_savings_per_month}/month:\n"
        f"- Monthly savings would be ${new_savings:.0f}.\n"
        f"- Emergency fund of $1000 reached in {months_to_ef:.1f} months."
    )
    return impact