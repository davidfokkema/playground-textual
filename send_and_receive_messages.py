import queue
import threading
import time
from typing import Callable

from textual import on
from textual.app import App, ComposeResult
from textual.message import Message
from textual.widgets import Input, RichLog


class SerialDevice:
    """Simulate a serial device which responds to messages."""

    def __init__(self) -> None:
        self.data = queue.SimpleQueue()
        self._device = threading.Thread(target=self._device_event_loop, daemon=True)
        self._device.start()

    def _device_event_loop(self) -> None:
        while True:
            message = self.data.get()
            time.sleep(1)
            self._callback(f"Hi, I received this message: {message}, thanks!")

    def send_and_receive(self, message: str, callback: Callable) -> None:
        self._callback = callback
        self.data.put(message)


class CommunicationApp(App[None]):
    class MessageReceived(Message):
        """Message received event."""

        def __init__(self, message: str) -> None:
            super().__init__()
            self.message = message

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.device = SerialDevice()

    def compose(self) -> ComposeResult:
        yield RichLog(markup=True)
        yield Input(placeholder="Type message to send")

    @on(Input.Submitted)
    def send_message(self, event: Input.Submitted) -> None:
        def receive_message_callback(message: str) -> None:
            self.post_message(self.MessageReceived(message))

        self.device.send_and_receive(event.value, callback=receive_message_callback)
        self.query_one(RichLog).write(f"Message sent: {event.value}")
        event.input.clear()

    @on(MessageReceived)
    def receive_message(self, event: MessageReceived) -> None:
        self.notify("New message")
        self.query_one(RichLog).write(f"[bold green]Message received: {event.message}.")


CommunicationApp().run()
