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

    def parse_date(self, date_text):
        try:
            return datetime.strptime(date_text, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError("The date must have dd/mm/yyyy format.")

    def format_date(self, date_value):
        return date_value.strftime("%d/%m/%Y")

    def add_category(self, name, color="#DDEBF7"):
        name = name.strip()

        if not name:
            raise ValueError("The category name cannot be empty.")

        if name in [category.name for category in self.categories]:
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
        return [category.name for category in self.categories]

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

        parsed_date = self.parse_date(date)
        today = datetime.today().date()

        if parsed_date > today:
            raise ValueError("The date cannot be in the future.")

        self.transactions.append(
            Transaction(title, amount, category, type_, parsed_date)
        )

    def calculate_balance(self):
        balance = 0

        for transaction in self.transactions:
            if transaction.type == "income":
                balance += transaction.amount
            else:
                balance -= transaction.amount

        return balance

    def transactions_to_table(self, transactions=None):
        if transactions is None:
            transactions = self.transactions

        table = []

        for transaction in transactions:
            table.append([
                self.format_date(transaction.date),
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
                "date": self.format_date(transaction.date)
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
        self.transactions = []

        for item in data:
            parsed_date = self.parse_date(item["date"])

            self.transactions.append(
                Transaction(
                    item["title"],
                    item["amount"],
                    item["category"],
                    item["type"],
                    parsed_date
                )
            )

    def validate_date(self, date_text):
        try:
            parsed_date = self.parse_date(date_text)
            today = datetime.today().date()

            return parsed_date <= today
        except ValueError:
            return False

    def filter_transactions_by_date(self, start_date, end_date):
        start = self.parse_date(start_date)
        end = self.parse_date(end_date)
        today = datetime.today().date()

        if start > today or end > today:
            raise ValueError("Dates cannot be in the future.")

        if start > end:
            raise ValueError(
                "The start date cannot be later than the end date."
            )

        return [
            transaction
            for transaction in self.transactions
            if start <= transaction.date <= end
        ]