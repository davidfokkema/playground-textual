from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Label
from textual.widgets.data_table import RowKey

ROWS = [
    ("lane", "swimmer", "country", "time"),
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),
]


class DeleteConfirmationDialog(ModalScreen):
    def __init__(self, msg: str) -> None:
        super().__init__()
        self.msg = msg

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(self.msg)
            with Horizontal():
                yield Button("Delete", id="delete", variant="error")
                yield Button("Cancel", id="cancel", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete":
            self.dismiss(True)
        else:
            self.dismiss(False)


class TableApp(App):
    CSS = """
        DeleteConfirmationDialog {
            align: center middle;

            & Vertical {
                width: auto;
                height: auto;
                background: $panel;
                border: $secondary round;
            }

            & Label {
                margin: 1 2;
            }

            & Horizontal {
                width: 100%;
                height: auto;
                align: center middle;
                margin: 1 2;

                & Button {
                    width: auto;
                    margin: 0 2;
                }
            }
        }
    """

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        self.delete_button = "[bold red]Delete"
        table = self.query_one(DataTable)
        table.add_columns(*ROWS[0])
        table.add_column("", key="delete")  # delete buttons
        table.add_rows([row + (self.delete_button,) for row in ROWS[1:]])

    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None:
        if event.value == self.delete_button:
            self.remove_row(event.data_table, event.cell_key.row_key)

    @work
    async def remove_row(self, data_table: DataTable, row_key: RowKey) -> None:
        row_values = [str(value) for value in data_table.get_row(row_key)[:-1]]
        confirmed = await self.push_screen_wait(
            DeleteConfirmationDialog(
                f"Are you sure you want to delete this row:\n{" / ".join(row_values)}"
            )
        )
        if confirmed:
            data_table.remove_row(row_key)


app = TableApp()
if __name__ == "__main__":
    app.run()
