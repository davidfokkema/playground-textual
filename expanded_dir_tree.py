from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree


class ExpandedDirTreeApp(App[None]):
    def compose(self) -> ComposeResult:
        yield DirectoryTree(".")

    def on_mount(self) -> None:
        tree: DirectoryTree = self.query_one(DirectoryTree)
        tree.root.expand_all()


ExpandedDirTreeApp().run()
