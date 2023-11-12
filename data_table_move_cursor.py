from textual.app import App
from textual.widgets import DataTable

class TestMove(App):

    def compose(self):
        yield DataTable()

    def on_mount(self):
        dt = self.query_one(DataTable)
        dt.add_column("thecolumn")

        for row in range(1000):
            dt.add_row(f"row number {row}")

        dt.move_cursor(row=500, column=1, animate=True)

TestMove().run()
