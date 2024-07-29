from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import DataTable

ROWS = [
    ("lane  ", "swimmer  ", "country  ", "time  "),
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


class TableApp(App):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])

    @on(DataTable.HeaderSelected)
    def rename_column(self, event: DataTable.HeaderSelected) -> None:
        data_table = self.query_one(DataTable)
        column = data_table.columns[event.column_key]
        column.label = Text(str(column.label)[:-1] + "▼")
        data_table._clear_caches()
        data_table.refresh()


app = TableApp()
if __name__ == "__main__":
    app.run()
