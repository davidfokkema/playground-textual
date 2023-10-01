from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Label, ListItem, ListView


class ListViewFocusApp(App[None]):
    BINDINGS = [("f", "show_focused", "Show which widget is focused")]

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("The details of the focused widget will go here")
            yield ListView(
                *[ListItem(Label(f"This is list item {n}")) for n in range(100)]
            )
        yield Footer()

    def action_show_focused(self) -> None:
        self.query_one("Vertical > Label", Label).update(f"It's a {self.focused!r}!")


if __name__ == "__main__":
    ListViewFocusApp().run()
