from textual.app import App, ComposeResult
from textual.containers import Horizontal, ScrollableContainer
from textual.widgets import Label, OptionList

ITEMS = ["str", "int", "float"]


class ShowDetailsApp(App[None]):
    CSS = """
        OptionList {
            width: 1fr;
            height: 1fr;
        }
        VerticalScroll {
            width: 1fr;
            height: 1fr;
        }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield OptionList(*ITEMS)
            with ScrollableContainer():
                yield Label(id="details")

    def on_option_list_option_highlighted(
        self, event: OptionList.OptionHighlighted
    ) -> None:
        obj = getattr(__builtins__, event.option.prompt)
        details = getattr(obj, "__doc__")
        self.query_one("#details").update(details)


if __name__ == "__main__":
    ShowDetailsApp().run()
