from pathlib import Path
from typing import Iterable

from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree


class FilteredDirectoryTree(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        suffixes = {".wav", ".mp3", ".m4a", ".ogg", ".flac", ".opus"}
        return [
            path
            for path in paths
            if not path.name.startswith(".")
            and (path.is_dir() or path.suffix in suffixes)
        ]


class DirectoryTreeApp(App):
    def compose(self) -> ComposeResult:
        yield FilteredDirectoryTree("./")


if __name__ == "__main__":
    app = DirectoryTreeApp()
    app.run()
