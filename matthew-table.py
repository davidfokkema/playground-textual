from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Label, Markdown, TabbedContent, TabPane

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


PAUL = """
# Paul Atreides

Son of Leto and Jessica.
"""


class App(App):
    def compose(self) -> ComposeResult:
        # Add the TabbedContent widget
        with TabbedContent(initial="rows"):
            with TabPane("Rows", id="rows"):  # First tab
                yield DataTable()  # Tab content

            with TabPane("Paul", id="paul"):
                yield Markdown(PAUL)

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])


if __name__ == "__main__":
    app = App()
    app.run()
