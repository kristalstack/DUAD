import unittest
from datetime import date
from logic import FinanceManager


class TestFinanceManager(unittest.TestCase):

    def setUp(self):
        self.manager = FinanceManager()

    def test_add_valid_category(self):
        self.manager.add_category("Food")
        self.assertEqual(len(self.manager.categories), 1)
        self.assertEqual(self.manager.categories[0].name, "Food")

    def test_do_not_allow_empty_category(self):
        with self.assertRaises(ValueError):
            self.manager.add_category("")

    def test_do_not_allow_duplicate_category(self):
        self.manager.add_category("Food")
        with self.assertRaises(ValueError):
            self.manager.add_category("Food")

    def test_update_category_color(self):
        self.manager.add_category("Food", "#DDEBF7")
        self.manager.update_category_color("Food", "#FFA500")
        self.assertEqual(self.manager.categories[0].color, "#FFA500")

    def test_has_categories(self):
        self.assertFalse(self.manager.has_categories())
        self.manager.add_category("Transport")
        self.assertTrue(self.manager.has_categories())

    def test_add_valid_expense(self):
        self.manager.add_category("Food")
        self.manager.add_transaction(
            "Lunch",
            20,
            "Food",
            "expense",
            "03/07/2025"
        )

        self.assertEqual(len(self.manager.transactions), 1)
        self.assertEqual(self.manager.transactions[0].title, "Lunch")
        self.assertEqual(self.manager.transactions[0].type, "expense")
        self.assertEqual(self.manager.transactions[0].date, date(2025, 7, 3))

    def test_add_valid_income(self):
        self.manager.add_category("Salary")
        self.manager.add_transaction(
            "Payment",
            1000,
            "Salary",
            "income",
            "02/07/2025"
        )

        self.assertEqual(len(self.manager.transactions), 1)
        self.assertEqual(self.manager.transactions[0].title, "Payment")
        self.assertEqual(self.manager.transactions[0].type, "income")
        self.assertEqual(self.manager.transactions[0].date, date(2025, 7, 2))

    def test_do_not_allow_non_numeric_amount(self):
        self.manager.add_category("Food")
        with self.assertRaises(ValueError):
            self.manager.add_transaction(
                "Dinner",
                "hello",
                "Food",
                "expense",
                "03/07/2025"
            )

    def test_do_not_allow_zero_or_negative_amount(self):
        self.manager.add_category("Food")
        with self.assertRaises(ValueError):
            self.manager.add_transaction(
                "Dinner",
                0,
                "Food",
                "expense",
                "03/07/2025"
            )

    def test_do_not_allow_nonexistent_category(self):
        self.manager.add_category("Food")
        with self.assertRaises(ValueError):
            self.manager.add_transaction(
                "Taxi",
                15,
                "Transport",
                "expense",
                "03/07/2025"
            )

    def test_do_not_add_transaction_without_categories(self):
        with self.assertRaises(ValueError):
            self.manager.add_transaction(
                "Taxi",
                15,
                "Transport",
                "expense",
                "03/07/2025"
            )

    def test_calculate_balance_correctly(self):
        self.manager.add_category("Salary")
        self.manager.add_category("Food")

        self.manager.add_transaction(
            "Payment",
            1000,
            "Salary",
            "income",
            "02/07/2025"
        )
        self.manager.add_transaction(
            "Dinner",
            100,
            "Food",
            "expense",
            "03/07/2025"
        )

        self.assertEqual(self.manager.calculate_balance(), 900)

    def test_validate_correct_past_date(self):
        self.assertTrue(self.manager.validate_date("10/07/2024"))

    def test_validate_incorrect_format_date(self):
        self.assertFalse(self.manager.validate_date("2025-07-10"))

    def test_validate_future_date_as_invalid(self):
        self.assertFalse(self.manager.validate_date("31/12/2099"))

    def test_do_not_allow_invalid_date_when_adding_transaction(self):
        self.manager.add_category("General")
        with self.assertRaises(ValueError):
            self.manager.add_transaction(
                "Test",
                50,
                "General",
                "expense",
                "2025-07-10"
            )

    def test_do_not_allow_future_date_when_adding_transaction(self):
        self.manager.add_category("General")
        with self.assertRaises(ValueError):
            self.manager.add_transaction(
                "Future test",
                50,
                "General",
                "expense",
                "31/12/2099"
            )

    def test_filter_transactions_by_date(self):
        self.manager.add_category("General")

        self.manager.add_transaction(
            "Salary",
            1000,
            "General",
            "income",
            "02/07/2025"
        )
        self.manager.add_transaction(
            "Food",
            20,
            "General",
            "expense",
            "03/07/2025"
        )
        self.manager.add_transaction(
            "Clothes",
            50,
            "General",
            "expense",
            "12/07/2025"
        )

        result = self.manager.filter_transactions_by_date(
            "01/07/2025",
            "10/07/2025"
        )

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "Salary")
        self.assertEqual(result[1].title, "Food")

    def test_do_not_allow_inverted_date_range(self):
        with self.assertRaises(ValueError):
            self.manager.filter_transactions_by_date(
                "15/07/2025",
                "10/07/2025"
            )

    def test_transactions_to_table_formats_dates_as_text(self):
        self.manager.add_category("General")
        self.manager.add_transaction(
            "Food",
            20,
            "General",
            "expense",
            "03/07/2025"
        )

        table = self.manager.transactions_to_table()

        self.assertEqual(table[0][0], "03/07/2025")

    def test_transactions_to_dict_formats_dates_as_text(self):
        self.manager.add_category("General")
        self.manager.add_transaction(
            "Food",
            20,
            "General",
            "expense",
            "03/07/2025"
        )

        data = self.manager.transactions_to_dict()

        self.assertEqual(data[0]["date"], "03/07/2025")


if __name__ == "__main__":
    unittest.main()