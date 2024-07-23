from textual.app import App, ComposeResult
from textual.widgets import RadioButton, RadioSet


class MyRadioButton(RadioButton):
    BUTTON_INNER = "X"


class RadioChoicesApp(App[None]):
    CSS = """
        Screen {
            align: center middle;
        }

        RadioSet {
            width: auto;
            layout: horizontal;
        }
    """

    def compose(self) -> ComposeResult:
        with RadioSet():
            yield MyRadioButton("Battlestar Galactica")
            yield MyRadioButton("Dune 1984")
            yield MyRadioButton("Dune 2021", id="focus_me")
            yield MyRadioButton("Serenity", value=True)
            yield MyRadioButton("Star Trek: The Motion Picture")
            yield MyRadioButton("Star Wars: A New Hope")
            # yield MyRadioButton("The Last Starfighter")
            # yield MyRadioButton(
            #     "Total Recall :backhand_index_pointing_right: :red_circle:"
            # )
            # yield MyRadioButton("Wing Commander")

    def on_mount(self) -> None:
        self.query_one(RadioSet).focus()


if __name__ == "__main__":
    RadioChoicesApp().run()
