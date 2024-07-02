from textual.app import App, ComposeResult
from textual.widgets import OptionList
from textual.widgets.option_list import Option


class OptionListApp(App[None]):
    def compose(self) -> ComposeResult:
        self.compression_selection_list = OptionList(id="selection_compression_mode")

        for i in range(5):
            self.compression_selection_list.add_option(Option(str(i)))
        yield self.compression_selection_list


OptionListApp().run()
