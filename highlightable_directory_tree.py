"""Highlightable DirectoryTree.

Implements a DirectoryTree which has the ability to highlight a path that may be
nested several levels deep in the tree. This can be done at all times, even when
the tree has never been expanded and thus the directory contents containing the
path have not been cached yet. The implementation will walk the tree, expanding
nodes when necessary and waiting on the contents before taking another step
until it arrives at the requested path. The node containing the path is
subsequently highlighted.
"""

from pathlib import Path

from textual import on
from textual.app import App, ComposeResult
from textual.await_complete import AwaitComplete
from textual.errors import TextualError
from textual.widgets import Button, DirectoryTree
from textual.widgets._directory_tree import DirEntry
from textual.widgets._tree import TreeNode


class HighlightableDirectoryTree(DirectoryTree):
    """DirectoryTree with path highlighting support."""

    class PathNotFoundError(TextualError):
        def __init__(self, path: Path) -> None:
            self.path = path

    def highlight_path(self, path: Path) -> AwaitComplete:
        """Highlight a path in the tree.

        Highlights a path that may be nested several levels deep in the tree.
        This can be done at all times, even when the tree has never been
        expanded and thus the directory contents containing the path have not
        been cached yet. This method will walk the tree, expanding nodes when
        necessary and waiting on the contents before taking another step until
        it arrives at the requested path. The node containing the path is
        subsequently highlighted.

        Args:
            path (Path): the path to highlight.

        Returns:
            AwaitComplete: An optionally awaitable that ensures the path is
                highlighted.
        """
        return AwaitComplete(self._highlight_path(path))

    async def _highlight_path(self, path: Path) -> None:
        """Highlight a path in the tree, while expanding parents.

        Args:
            path (Path): the path to highlight.
        """
        node = await self._expand_parents_and_find_node(path)
        self.move_cursor(node)

    async def _expand_parents_and_find_node(self, path: Path) -> TreeNode[DirEntry]:
        """Traverse all parts of the path and expand all parents.

        This method will traverse all parts of the path and expand all parents
        in the tree when necessary. Finally, the node containing the requested
        path is returned.

        Args:
            path (Path): the requested path that must become visible.

        Returns:
            TreeNode[DirEntry]: the tree node containing the requested path.
        """
        node = self.root
        for part in Path(path).parts:
            node = self._find_node_from_path(node, part)
            if not node.children:
                await self.reload_node(node)
            node.expand()
        return node

    def _find_node_from_path(
        self, parent: TreeNode[DirEntry], path: str
    ) -> TreeNode[DirEntry]:
        """Search a node's children for a specific path.

        The path must be a direct child of the parent. For example, if the
        parent's path is /home/alice, then the path may be /home/alice/work, or
        /home/alice/documents, but _not_ /home/alice/work/software since that is
        not a direct child of /home/alice.

        Args:
            parent (TreeNode[DirEntry]): the parent node.
            path (str): the path to search for.

        Raises:
            PathNotFoundError: raised when the path is not found.

        Returns:
            TreeNode[DirEntry]: the node containing the requested path.
        """
        root = parent.data.path.absolute()
        for node in parent.children:
            if str(node.data.path.relative_to(root)) == path:
                return node
        raise self.PathNotFoundError(path)


class MyApp(App[None]):
    def compose(self) -> ComposeResult:
        yield HighlightableDirectoryTree(".")
        yield Button("Press me", variant="primary")

    @on(Button.Pressed)
    def highlight_path(self) -> None:
        """Highlight an example path."""
        (tree := self.query_one(HighlightableDirectoryTree)).highlight_path(
            ".git/refs/heads/main"
        )
        tree.focus()


MyApp().run()
