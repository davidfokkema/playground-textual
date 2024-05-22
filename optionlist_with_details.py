from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Label, OptionList

ITEMS = ["str", "int", "float", "list", "dict", "set"]


class ShowDetailsApp(App[None]):
    CSS = """
        OptionList {
            width: 15;
            height: 1fr;
        }
        VerticalScroll {
            width: 1fr;
            height: 1fr;
        }
        Label {
            width: 100%;
        }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield OptionList(*ITEMS)
            with VerticalScroll():
                yield Label(id="details")

    def on_option_list_option_highlighted(
        self, event: OptionList.OptionHighlighted
    ) -> None:
        obj = getattr(__builtins__, event.option.prompt)
        details = getattr(obj, "__doc__")
        self.query_one("#details").update(details)


if __name__ == "__main__":
    ShowDetailsApp().run()
