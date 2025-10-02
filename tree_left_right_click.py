from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.events import Click
from textual.widgets import Label, Tree


class TreeApp(App):
    CSS = """
    #my-tree, Label {
        width: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            tree: Tree[str] = Tree("Dune", id="my-tree")
            tree.root.expand()
            characters = tree.root.add("Characters", expand=True)
            characters.add_leaf("Paul")
            characters.add_leaf("Jessica")
            characters.add_leaf("Chani")
            yield tree
            yield Label(id="info-label")

    @on(Click, "#my-tree")
    def show_tree_info(self, event: Click) -> None:
        node = self.query_one("#my-tree", Tree).get_node_at_line(event.y)
        if node is not None:
            if event.button == 1:
                self.query_one("#info-label", Label).update(
                    f"Clicked on node: {node.label}"
                )
            elif event.button == 3:
                self.notify(f"Right-clicked on node: {node.label}")


if __name__ == "__main__":
    app = TreeApp()
    app.run()
