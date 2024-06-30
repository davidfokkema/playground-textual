from textual.app import App, ComposeResult
from textual.widgets import Tree

CHARACTERS = {
    "Paul": "Son of Leto Atreides",
    "Jessica": "Mother of Paul Atreides",
    "Chani": "Daughter of Liet-Kynes",
}


class TreeApp(App):
    def compose(self) -> ComposeResult:
        tree: Tree[dict] = Tree("Dune")
        tree.root.expand()
        characters = tree.root.add("Characters", expand=True)
        for name, description in CHARACTERS.items():
            characters.add_leaf(name, data=description)
        yield tree

    def on_mount(self) -> None:
        def update_tooltip(line: int) -> None:
            tree.tooltip = tree.get_node_at_line(line).data

        tree = self.query_one(Tree)
        self.watch(tree, "hover_line", update_tooltip)


if __name__ == "__main__":
    app = TreeApp()
    app.run()
