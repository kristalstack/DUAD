import json
import os
import csv


def save_data(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_data(path):
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def export_transactions_csv(path, transactions):
    total_income = 0
    total_expenses = 0

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["Date", "Title", "Amount", "Category", "Type"])

        for transaction in transactions:
            csv_amount = transaction.amount
            csv_type = transaction.type.capitalize()

            if transaction.type == "expense":
                csv_amount = -transaction.amount
                total_expenses += transaction.amount
            else:
                total_income += transaction.amount

            writer.writerow([
                transaction.date,
                transaction.title,
                csv_amount,
                transaction.category,
                csv_type
            ])

        net_balance = total_income - total_expenses

        writer.writerow([])
        writer.writerow(["Totals:"])
        writer.writerow([f"Income: ₡{total_income}"])
        writer.writerow([f"Expenses: ₡{total_expenses}"])
        writer.writerow([f"Net Balance: ₡{net_balance}"])