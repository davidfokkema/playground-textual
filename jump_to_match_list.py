from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input, OptionList
from thefuzz import process

OPTIONS = "apple banana strawberry orange pineapple lemon".split(" ")


class SearchApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for a match...")
        yield OptionList(*OPTIONS)

    @on(Input.Changed)
    def jump_to_item(self, event: Input.Changed) -> None:
        search = event.value
        best_match, _ = process.extractOne(search, OPTIONS)
        idx = OPTIONS.index(best_match)
        self.query_one(OptionList).highlighted = idx


SearchApp().run()
