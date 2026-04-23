from datetime import datetime


class Category:
    def __init__(self, name, color="#DDEBF7"):
        self.name = name
        self.color = color


class Transaction:
    def __init__(self, title, amount, category, type_, date):
        self.title = title
        self.amount = amount
        self.category = category
        self.type = type_
        self.date = date


class FinanceManager:
    def __init__(self):
        self.categories = []
        self.transactions = []

    def add_category(self, name, color="#DDEBF7"):
        name = name.strip()

        if not name:
            raise ValueError("The category name cannot be empty.")

        if name in [c.name for c in self.categories]:
            raise ValueError("The category already exists.")

        self.categories.append(Category(name, color))

    def update_category_color(self, name, new_color):
        for category in self.categories:
            if category.name == name:
                category.color = new_color
                return

        raise ValueError("Category not found.")

    def has_categories(self):
        return len(self.categories) > 0

    def get_category_names(self):
        return [c.name for c in self.categories]

    def get_category_color(self, category_name):
        for category in self.categories:
            if category.name == category_name:
                return category.color
        return "#DDEBF7"

    def add_transaction(self, title, amount, category, type_, date):
        title = title.strip()

        if not title:
            raise ValueError("The title cannot be empty.")

        if not self.has_categories():
            raise ValueError("No categories available.")

        try:
            amount = float(amount)
        except ValueError:
            raise ValueError("Invalid amount.")

        if amount <= 0:
            raise ValueError("The amount must be greater than 0.")

        if category not in self.get_category_names():
            raise ValueError("Category does not exist.")

        if type_ not in ["income", "expense"]:
            raise ValueError("Invalid type.")

        if not self.validate_date(date):
            raise ValueError(
                "The date must have dd/mm/yyyy format and cannot be in the future."
            )

        self.transactions.append(
            Transaction(title, amount, category, type_, date)
        )

    def calculate_balance(self):
        balance = 0

        for transaction in self.transactions:
            if transaction.type == "income":
                balance += transaction.amount
            else:
                balance -= transaction.amount

        return balance

    def get_transactions_table(self):
        table = []

        for transaction in self.transactions:
            table.append([
                transaction.date,
                transaction.title,
                transaction.amount,
                transaction.category,
                transaction.type
            ])

        return table

    def transactions_to_table(self, transactions):
        table = []

        for transaction in transactions:
            table.append([
                transaction.date,
                transaction.title,
                transaction.amount,
                transaction.category,
                transaction.type
            ])

        return table

    def get_row_colors(self, transactions=None):
        if transactions is None:
            transactions = self.transactions

        row_colors = []

        for index, transaction in enumerate(transactions):
            color = self.get_category_color(transaction.category)
            row_colors.append((index, "black", color))

        return row_colors

    def categories_to_dict(self):
        return [
            {
                "name": category.name,
                "color": category.color
            }
            for category in self.categories
        ]

    def transactions_to_dict(self):
        return [
            {
                "title": transaction.title,
                "amount": transaction.amount,
                "category": transaction.category,
                "type": transaction.type,
                "date": transaction.date
            }
            for transaction in self.transactions
        ]

    def load_categories(self, data):
        self.categories = []

        for item in data:
            if isinstance(item, str):
                self.categories.append(Category(item, "#DDEBF7"))
            else:
                self.categories.append(
                    Category(
                        item["name"],
                        item.get("color", "#DDEBF7")
                    )
                )

    def load_transactions(self, data):
        self.transactions = [
            Transaction(
                item["title"],
                item["amount"],
                item["category"],
                item["type"],
                item["date"]
            )
            for item in data
        ]

    def validate_date(self, date_text):
        try:
            entered_date = datetime.strptime(date_text, "%d/%m/%Y").date()
            today = datetime.today().date()

            if entered_date > today:
                return False

            return True
        except ValueError:
            return False

    def filter_transactions_by_date(self, start_date, end_date):
        if not self.validate_date(start_date):
            raise ValueError(
                "The start date must have dd/mm/yyyy format and cannot be in the future."
            )

        if not self.validate_date(end_date):
            raise ValueError(
                "The end date must have dd/mm/yyyy format and cannot be in the future."
            )

        start = datetime.strptime(start_date, "%d/%m/%Y")
        end = datetime.strptime(end_date, "%d/%m/%Y")

        if start > end:
            raise ValueError(
                "The start date cannot be later than the end date."
            )

        return [
            transaction
            for transaction in self.transactions
            if start <= datetime.strptime(transaction.date, "%d/%m/%Y") <= end
        ]