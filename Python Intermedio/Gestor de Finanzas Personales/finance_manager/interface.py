import FreeSimpleGUI as sg


def create_main_window(table_data, balance, row_colors):
    headers = ["Date", "Title", "Amount", "Category", "Type"]

    layout = [
        [sg.Text("Personal Finance Manager", font=("Helvetica", 14))],
        [sg.Text(f"Current Balance: {balance}", key="BALANCE")],
        [
            sg.Text("Start Date:"),
            sg.Input(key="START_DATE", size=(12, 1)),
            sg.Text("End Date:"),
            sg.Input(key="END_DATE", size=(12, 1)),
            sg.Button("Filter"),
            sg.Button("Show All")
        ],
        [
            sg.Table(
                values=table_data,
                headings=headers,
                auto_size_columns=True,
                justification="left",
                num_rows=8,
                key="TRANSACTIONS_TABLE",
                expand_x=True,
                expand_y=True,
                row_colors=row_colors
            )
        ],
        [
            sg.Button("Add Category"),
            sg.Button("Edit Category"),
            sg.Button("Add Expense"),
            sg.Button("Add Income"),
            sg.Button("Export to CSV"),
            sg.Button("Exit")
        ]
    ]

    return sg.Window("Finance Manager", layout, resizable=True)


def add_category_window():
    layout = [
        [sg.Text("New Category")],
        [sg.Text("Name"), sg.Input(key="NAME")],
        [
            sg.Text("Color"),
            sg.Input("#DDEBF7", key="COLOR", size=(12, 1)),
            sg.ColorChooserButton("Choose Color", target="COLOR")
        ],
        [sg.Button("Save"), sg.Button("Cancel")]
    ]

    window = sg.Window("Add Category", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Cancel":
            window.close()
            return None

        if event == "Save":
            window.close()
            return {
                "name": values["NAME"],
                "color": values["COLOR"] or "#DDEBF7"
            }


def edit_category_window(categories):
    layout = [
        [sg.Text("Select Category")],
        [sg.Combo(categories, key="CATEGORY", readonly=True)],
        [
            sg.Text("New Color"),
            sg.Input("#DDEBF7", key="COLOR", size=(12, 1)),
            sg.ColorChooserButton("Choose Color", target="COLOR")
        ],
        [sg.Button("Save"), sg.Button("Cancel")]
    ]

    window = sg.Window("Edit Category", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Cancel":
            window.close()
            return None

        if event == "Save":
            window.close()
            return values


def add_transaction_window(categories, type_):
    layout = [
        [sg.Text(f"Add {type_.capitalize()}")],
        [sg.Text("Title"), sg.Input(key="TITLE")],
        [sg.Text("Amount"), sg.Input(key="AMOUNT")],
        [sg.Text("Category"), sg.Combo(categories, key="CATEGORY", readonly=True)],
        [sg.Text("Date (dd/mm/yyyy)"), sg.Input(key="DATE")],
        [sg.Button("Save"), sg.Button("Cancel")]
    ]

    window = sg.Window(f"Add {type_.capitalize()}", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Cancel":
            window.close()
            return None

        if event == "Save":
            window.close()
            return values