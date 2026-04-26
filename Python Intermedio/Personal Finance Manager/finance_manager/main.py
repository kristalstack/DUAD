import FreeSimpleGUI as sg
from logic import FinanceManager
from persistence import (
    save_data,
    load_data,
    export_transactions_csv
)
from interface import (
    create_main_window,
    add_category_window,
    edit_category_window,
    add_transaction_window
)

CATEGORIES_PATH = "categories.json"
TRANSACTIONS_PATH = "transactions.json"
CSV_PATH = "exported_transactions.csv"


def update_interface(window, manager):
    table = manager.transactions_to_table()
    colors = manager.get_row_colors()

    window["TRANSACTIONS_TABLE"].update(
        values=table,
        row_colors=colors
    )
    window["BALANCE"].update(
        f"Current Balance: {manager.calculate_balance()}"
    )


def show_filtered_transactions(window, manager, filtered_transactions):
    table = manager.transactions_to_table(filtered_transactions)
    colors = manager.get_row_colors(filtered_transactions)

    window["TRANSACTIONS_TABLE"].update(
        values=table,
        row_colors=colors
    )


def process_add_transaction(manager, window, type_):
    if not manager.has_categories():
        sg.popup("You must create a category first.")
        return

    data = add_transaction_window(
        manager.get_category_names(),
        type_
    )

    if not data:
        return

    try:
        manager.add_transaction(
            data["TITLE"],
            data["AMOUNT"],
            data["CATEGORY"],
            type_,
            data["DATE"]
        )

        save_data(TRANSACTIONS_PATH, manager.transactions_to_dict())
        update_interface(window, manager)

    except Exception as error:
        sg.popup(str(error))


manager = FinanceManager()

categories = load_data(CATEGORIES_PATH)
transactions = load_data(TRANSACTIONS_PATH)

manager.load_categories(categories)
manager.load_transactions(transactions)

window = create_main_window(
    manager.transactions_to_table(),
    manager.calculate_balance(),
    manager.get_row_colors()
)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Exit":
        break

    if event == "Add Category":
        category_data = add_category_window()

        if category_data:
            try:
                manager.add_category(
                    category_data["name"],
                    category_data["color"]
                )
                save_data(CATEGORIES_PATH, manager.categories_to_dict())
                update_interface(window, manager)
            except Exception as error:
                sg.popup(str(error))

    if event == "Edit Category":
        if not manager.has_categories():
            sg.popup("There are no categories to edit.")
            continue

        data = edit_category_window(
            manager.get_category_names()
        )

        if data:
            try:
                manager.update_category_color(
                    data["CATEGORY"],
                    data["COLOR"] or "#DDEBF7"
                )
                save_data(CATEGORIES_PATH, manager.categories_to_dict())
                update_interface(window, manager)
            except Exception as error:
                sg.popup(str(error))

    if event == "Add Expense":
        process_add_transaction(manager, window, "expense")

    if event == "Add Income":
        process_add_transaction(manager, window, "income")

    if event == "Filter":
        start_date = values["START_DATE"]
        end_date = values["END_DATE"]

        try:
            filtered_transactions = manager.filter_transactions_by_date(
                start_date,
                end_date
            )
            show_filtered_transactions(
                window,
                manager,
                filtered_transactions
            )
        except Exception as error:
            sg.popup(str(error))

    if event == "Show All":
        update_interface(window, manager)

    if event == "Export to CSV":
        try:
            export_transactions_csv(CSV_PATH, manager.transactions)
            sg.popup(f"CSV file exported successfully: {CSV_PATH}")
        except Exception as error:
            sg.popup(str(error))

window.close()