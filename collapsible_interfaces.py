from textual.app import App, ComposeResult
from textual.containers import Container, Grid
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Collapsible, Header, Input, Label


class InterfaceSummary(Screen):
    def compose(self) -> ComposeResult:
        yield Header()

        for iface in ["eth0", "eth1", "wlan0", "if0"]:
            with Collapsible(collapsed=True, title=iface):
                yield Interface(interface=iface)
                # yield Label("Hi there!")


class Interface(Widget):
    def __init__(self, interface: "Interface", *children: Widget):
        super().__init__(*children)
        self.interface = interface

    def compose(self) -> ComposeResult:
        with Grid(id="interface_grid"):
            yield Label("Name:", classes="label")
            yield Input(value=self.interface, classes="box", id="iface_name")

            yield Label("Bond Type:", classes="label")
            yield Input(
                value="self.interface.bond_type", classes="box", id="iface_bond_type"
            )

            yield Label("MAC Address:", classes="label")
            yield Input(
                value="self.interface.mac_address", classes="box", id="iface_mac_addr"
            )

            yield Label("IPs:", classes="label")
            yield Input(value="str(self.interface.ips)", classes="box", id="iface_ips")

            yield Label("Bonds:", classes="label")
            yield Input(
                value="str(self.interface.bonds)", classes="box", id="iface_bonds"
            )


class CollapsibleInterfaceApp(App[None]):
    CSS_PATH = "tmp.tcss"
    SCREENS = {"summary": InterfaceSummary()}

    def on_mount(self) -> None:
        self.push_screen("summary")


CollapsibleInterfaceApp().run()
