from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Tree

CHARACTERS = {
    "Paul": "Son of Leto Atreides",
    "Jessica": "Mother of Paul Atreides",
    "Chani": "Daughter of Liet-Kynes",
}


class MyTree(Tree):
    def watch_hover_line(self, previous: int, line: int) -> None:
        super().watch_hover_line(previous, line)
        try:
            self.tooltip = self.get_node_at_line(line).data
        except KeyError:
            self.tooltip = None


class TreeScreen(Screen):
    CSS = """
        TreeScreen {
            Tooltip {
                visibility: hidden;
            }
            
            &.show_tooltips Tooltip {
                visibility: visible;
            }
        }
    """
    BINDINGS = [("t", "toggle_tooltips", "Toggle Tooltips")]

    DEFAULT_CLASSES = "show_tooltips"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield MyTree("Dune")

    def on_mount(self) -> None:
        tree = self.query_one(MyTree)
        tree.root.expand()
        characters = tree.root.add("Characters", expand=True)
        for name, description in CHARACTERS.items():
            characters.add_leaf(name, data=description)

    def action_toggle_tooltips(self) -> None:
        self.toggle_class("show_tooltips")
        if self.has_class("show_tooltips"):
            self.notify("Showing tooltips")
        else:
            self.notify("Tooltips disabled")


class TreeApp(App):
    def on_mount(self) -> None:
        self.push_screen(TreeScreen())


if __name__ == "__main__":
    app = TreeApp()
    app.run()
