from textual import on
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Checkbox


class CheckboxApp(App[None]):
    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Checkbox("All", id="all")
            yield Checkbox("Arrakis  :sweat:")
            yield Checkbox("Caladan")
            yield Checkbox("Chusuk")
            yield Checkbox("Giedi Prime")
            yield Checkbox("Ginaz")
            yield Checkbox("Grumman", True)
            yield Checkbox("Kaitain", id="initial_focus")
            yield Checkbox("Novebruns", True)

    def on_mount(self):
        self.query_one("#initial_focus", Checkbox).focus()

    @on(Checkbox.Changed)
    def handle_checkbox_change(self, event: Checkbox.Changed) -> None:
        if event.checkbox.id == "all":
            self.set_all_checkboxes(event.checkbox.value)
        else:
            self.set_other_checkbox()

    def set_all_checkboxes(self, value: bool) -> None:
        with self.prevent(Checkbox.Changed):
            for checkbox in self.query(Checkbox):
                if checkbox.id != "all":
                    checkbox.value = value
        self.filter()

    def set_other_checkbox(self) -> None:
        """Set the 'All' checkbox based on the state of the other checkboxes."""
        all_checkbox = self.query_one("#all", Checkbox)
        other_checkboxes = self.query(Checkbox).exclude("#all")
        all_checked = all(checkbox.value for checkbox in other_checkboxes)
        with self.prevent(Checkbox.Changed):
            all_checkbox.value = all_checked
        self.filter()

    def filter(self) -> None:
        self.notify("Filtering...")


if __name__ == "__main__":
    CheckboxApp().run()
