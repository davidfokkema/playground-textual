import random

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import DirectoryTree, Label, OptionList


class FocusWithinDirectoryTreeApp(App[None]):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield DirectoryTree(".")
            with Vertical():
                yield OptionList()
                yield Label(id="current_node")

    def on_mount(self) -> None:
        # build lookup table
        tree = self.query_one(DirectoryTree)
        self.path_line_lookup = {
            str(tree.get_node_at_line(line).data.path): line
            for line in range(0, tree.last_line)
        }

        # build option list from some randomly selected paths
        random_lines = [random.randint(0, tree.last_line - 1) for _ in range(5)]
        self.query_one(OptionList).add_options(
            [str(tree.get_node_at_line(line).data.path) for line in random_lines]
        )

    @on(DirectoryTree.NodeHighlighted)
    def show_node(self) -> None:
        # YES, you can get the current path from the event, but I'm showing here
        # how to get the path by querying the DirectoryTree, which can be done
        # at any time from any method.
        self.query_one("#current_node", Label).update(
            str(self.query_one(DirectoryTree).cursor_node.data.path)
        )

    @on(OptionList.OptionSelected)
    def highlight_path_in_tree(self, event: OptionList.OptionSelected) -> None:
        # lookup the correct line and hightlight that in the DirectoryTree
        line = self.path_line_lookup[event.option.prompt]
        (tree := self.query_one(DirectoryTree)).cursor_line = line
        tree.scroll_to_line(line)
        tree.focus()


FocusWithinDirectoryTreeApp().run()
