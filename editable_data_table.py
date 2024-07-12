"""Example to demonstrate an editable data table widget.

A regular DataTable is not editable. You _can_ update cells, but that has to be
done in code. This example demonstrates a widget with a key binding ('e') to
edit cells. If you press the edit key a modal screen is displayed with a single
Input widget containing the cell's original value. The widget is placed such
that the value of the Input widget precisely overlays the value in the cell.
Visually, pressing the edit key just draws a border around the cell and dims the
rest of the screen. You can edit the cell to your hearts content, but the type
must remain the same. So if you edit an integer, you cannot replace it with a
string (or even a float).
"""

from typing import Any

from textual import work
from textual.app import App, ComposeResult
from textual.coordinate import Coordinate
from textual.geometry import Offset, Region
from textual.screen import ModalScreen
from textual.widgets import DataTable, Footer, Input

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


class EditWidgetScreen(ModalScreen):
    """A modal screen with a single input widget."""

    CSS = """
        Input {
            border: solid $secondary-darken-3;
            padding: 0;

            &:focus {
                border: round $secondary;
            }
        }
    """

    def __init__(self, value: Any, region: Region, *args, **kwargs) -> None:
        """Initialization.

        Args:
            value (Any): the original value.
            region (Region): the region available for the input widget contents.
        """
        super().__init__(*args, **kwargs)
        self.value = value
        # store type to later cast the new value to the old type
        self.value_type = type(value)
        self.widget_region = region

    def compose(self) -> ComposeResult:
        yield Input(value=str(self.value))

    def on_mount(self) -> None:
        """Calculate and set the input widget's position and size.

        This takes into account any padding you might have set on the input
        widget, although the default padding is 0.
        """
        input = self.query_one(Input)
        input.offset = Offset(
            self.widget_region.offset.x - input.styles.padding.left - 1,
            self.widget_region.offset.y - input.styles.padding.top - 1,
        )
        input.styles.width = (
            self.widget_region.width
            + input.styles.padding.left
            + input.styles.padding.right
            # include the borders _and_ the cursus at the end of the line
            + 3
        )
        input.styles.height = (
            self.widget_region.height
            + input.styles.padding.top
            + input.styles.padding.bottom
            # include the borders
            + 2
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Return the new value.

        The new value is cast to the original type. If that is not possible
        (e.g. you try to replace a number with a string), returns None to
        indicate that the cell should _not_ be updated.
        """
        try:
            self.dismiss(self.value_type(event.value))
        except ValueError:
            self.dismiss(None)


class EditableDataTable(DataTable):
    """A datatable where you can edit cells."""

    BINDINGS = [("e", "edit", "Edit Cell")]

    def action_edit(self) -> None:
        self.edit_cell(coordinate=self.cursor_coordinate)

    @work()
    async def edit_cell(self, coordinate: Coordinate) -> None:
        """Edit cell contents.

        Args:
            coordinate (Coordinate): the coordinate of the cell to update.
        """
        region = self._get_cell_region(coordinate)
        # the region containing the cell contents, without padding
        contents_region = Region(
            region.x + self.cell_padding,
            region.y,
            region.width - 2 * self.cell_padding,
            region.height,
        )

        new_value = await self.app.push_screen_wait(
            EditWidgetScreen(value=self.get_cell_at(coordinate), region=contents_region)
        )
        if new_value is not None:
            self.update_cell_at(coordinate, new_value, update_width=True)


class TableApp(App):
    def compose(self) -> ComposeResult:
        yield Footer()
        yield EditableDataTable()

    def on_mount(self) -> None:
        table = self.query_one(EditableDataTable)
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])


app = TableApp()
if __name__ == "__main__":
    app.run()
