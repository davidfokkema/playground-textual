from textual.app import App, ComposeResult
from textual.widgets import Tree


class TreeApp(App):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.node_refs = {}

    def compose(self) -> ComposeResult:
        tree: Tree[dict] = Tree("Dune")
        tree.root.expand()
        characters = tree.root.add("Characters", expand=True)
        self.node_refs["Paul"] = characters.add_leaf("Paul")
        characters.add_leaf("Jessica")
        characters.add_leaf("Chani")
        yield tree

    def on_mount(self) -> None:
        self.node_refs["Paul"].remove()
        del self.node_refs["Paul"]
        self.notify(str(self.node_refs))


if __name__ == "__main__":
    app = TreeApp()
    app.run()
