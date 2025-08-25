from textual.app import App, ComposeResult
from textual.coordinate import Coordinate
from textual.events import Click
from textual.widgets import DataTable

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


class MyDataTable(DataTable):
    def on_click(self, event: Click) -> None:
        self.notify(
            f"Clicked at coordinates {event.x}, {event.y} with button {event.button}"
        )
        if event.button == 3:
            meta = event.style.meta
            if "row" not in meta or "column" not in meta:
                return
            row_index = meta["row"]
            column_index = meta["column"]

            value = self.get_cell_at(Coordinate(row_index, column_index))
            self.notify(
                f"Right-clicked on cell at row {row_index}, column {column_index}: {value}"
            )


class TableApp(App):
    def compose(self) -> ComposeResult:
        yield MyDataTable()

    def on_mount(self) -> None:
        table = self.query_one(MyDataTable)
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])


app = TableApp()
if __name__ == "__main__":
    app.run()
