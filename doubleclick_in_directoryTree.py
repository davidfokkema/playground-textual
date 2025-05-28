"""Double-click to select files and directories in a DirectoryTree widget."""

from textual import on
from textual.app import App
from textual.widgets import DirectoryTree, Static


class MyDirectoryTree(DirectoryTree):
    def _on_click(self, event):
        if event.chain == 1:
            # single click: prevent default behavior, don't select
            event.prevent_default()
            if (line := event.style.meta.get("line", -1)) > -1:
                # but highlight the line that was clicked
                self.cursor_line = line
                self.hover_line = line


class SelectInDirectoryTree(App):
    def compose(self):
        yield (dir_tree := MyDirectoryTree("."))
        dir_tree.auto_expand = False
        yield Static("Selected: None")

    @on(DirectoryTree.FileSelected)
    @on(DirectoryTree.DirectorySelected)
    def handle_selection(self, event):
        # If you like to use a single handler for both events,
        # you can use the `event` parameter to differentiate.
        if isinstance(event, DirectoryTree.DirectorySelected):
            msg = "Thou shall not pass!"
        elif isinstance(event, DirectoryTree.FileSelected):
            msg = f"That's {event.path.stat().st_size} bytes of data!"
        self.query_one(Static).update(msg)


SelectInDirectoryTree().run()
