from textual.app import App, ComposeResult
from textual.widgets import Label, OptionList

ITEMS = ["apple", "banana", "orange", "pineapple", "strawberry"]


class ShowHighlightApp(App[None]):
    def compose(self) -> ComposeResult:
        yield OptionList(*ITEMS)
        yield Label(id="details")

    def on_option_list_option_highlighted(
        self, event: OptionList.OptionHighlighted
    ) -> None:
        self.query_one("#details").update(event.option.prompt)


if __name__ == "__main__":
    ShowHighlightApp().run()
