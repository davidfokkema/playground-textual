from textual.app import App, ComposeResult
from textual.widgets import Label, RadioButton, RadioSet


class NoRadioSet(RadioSet):
    DEFAULT_CSS = RadioSet.DEFAULT_CSS.replace("RadioSet", "NoRadioSet")

    class Changed(RadioSet.Changed): ...

    def _on_radio_button_changed(self, event: RadioButton.Changed) -> None:
        """Respond to the value of a button in the set being changed.

        Args:
            event: The event.
        """
        # We're going to consume the underlying radio button events, making
        # it appear as if they don't emit their own, as far as the caller is
        # concerned. As such, stop the event bubbling and also prohibit the
        # same event being sent out if/when we make a value change in here.
        # We also _don't_ want the default RadioSet behaviour.
        event.prevent_default()
        event.stop()
        with self.prevent(RadioButton.Changed):
            # If the message pertains to a button being clicked to on...
            if event.radio_button.value:
                # If there's a button pressed right now and it's not really a
                # case of the user mashing on the same button...
                if (
                    self._pressed_button is not None
                    and self._pressed_button != event.radio_button
                ):
                    self._pressed_button.value = False
                # Make the pressed button this new button.
                self._pressed_button = event.radio_button
            else:
                # We're being clicked off, we _do_ want that.
                # if self._pressed_button:
                #     self._pressed_button.value = False
                self._pressed_button = None
            # Emit a message to say our state has changed.
            self.post_message(self.Changed(self, event.radio_button))

    def _on_no_radio_set_changed(self, event: Changed) -> None:
        """Handle a change to which button in the set is pressed.

        This handler ensures that, when a button is pressed, it's also the
        selected button.
        """
        self._selected = self._nodes.index(event.pressed)


class NoRadioApp(App[None]):
    def compose(self) -> ComposeResult:
        with NoRadioSet():
            yield RadioButton("Apple")
            yield RadioButton("Banana")
            yield RadioButton("Pineapple")
        yield Label()

    def on_mount(self) -> None:
        self.query_one(Label).update("None selected")

    def on_no_radio_set_changed(self, event: NoRadioSet.Changed):
        self.query_one(Label).update(
            f"Selected: {event.radio_set.pressed_index=}\n{event.radio_set._selected=}\n{event.radio_set.pressed_button=}"
        )


NoRadioApp().run()
