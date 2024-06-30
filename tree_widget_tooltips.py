from textual.app import App, ComposeResult
from textual.widgets import Tree

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


class TreeApp(App):
    def compose(self) -> ComposeResult:
        tree: MyTree[dict] = MyTree("Dune")
        tree.root.expand()
        characters = tree.root.add("Characters", expand=True)
        for name, description in CHARACTERS.items():
            characters.add_leaf(name, data=description)
        yield tree


if __name__ == "__main__":
    app = TreeApp()
    app.run()
