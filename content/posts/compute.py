
def compute_years_till_retirement(saving_rate, investment_return_after_inflation, live_on_goal):
    income = 1
    investment_return_monthly = (1 + investment_return_after_inflation) ** (1/12) - 1
    live_on_goal_monthly = (1 + live_on_goal) ** (1/12) - 1
    can_live_on = (1 - saving_rate) * income
    months = 0
    current_savings = 0
    while current_savings * live_on_goal_monthly < can_live_on:
        current_savings += saving_rate * income
        current_savings *= (1 + investment_return_monthly)
        months += 1
    return months / 12

print("Saving rate: Years till retirement")
for saving_rate in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]:
    print(f"{saving_rate}: {compute_years_till_retirement(saving_rate, 0.05, 0.04):.2f}")