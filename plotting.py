from time import sleep

import plotext as plt
from rich.ansi import AnsiDecoder
from rich.console import Group
from rich.jupyter import JupyterMixin
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text


def make_plot(width, height, phase=0, title=""):
    plt.clf()
    l, frames = 1000, 30
    x = range(1, l + 1)
    y = plt.sin(periods=2, length=l, phase=2 * phase / frames)
    plt.scatter(x, y, marker="hd")
    plt.plotsize(width, height)
    plt.xaxes(1, 0)
    plt.yaxes(1, 0)
    plt.title(title)
    plt.theme("dark")
    plt.ylim(-1, 1)
    # plt.cls()
    return plt.build()


class plotextMixin(JupyterMixin):
    def __init__(self, phase=0, title=""):
        self.decoder = AnsiDecoder()
        self.phase = phase
        self.title = title

    def __rich_console__(self, console, options):
        self.width = options.max_width or console.width
        self.height = options.height or console.height
        canvas = make_plot(self.width, self.height, self.phase, self.title)
        self.rich_canvas = Group(*self.decoder.decode(canvas))
        yield self.rich_canvas


def make_layout():
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=1),
        Layout(name="main", ratio=1),
    )
    layout["main"].split_column(
        Layout(name="static", ratio=1),
        Layout(name="dynamic"),
    )
    return layout


layout = make_layout()

header = layout["header"]
title = (
    plt.colorize("Pl✺ text ", "cyan+", "bold")
    + "integration with "
    + plt.colorize("rich_", style="dim")
)
header.update(Text(title, justify="left"))

static = layout["static"]
phase = 0
mixin_static = Panel(plotextMixin(title="Static Plot"))
static.update(mixin_static)

dynamic = layout["dynamic"]

with Live(layout, refresh_per_second=0.0001) as live:
    while True:
        phase += 1
        mixin_dynamic = Panel(plotextMixin(phase, "Dynamic Plot"))
        dynamic.update(mixin_dynamic)
        sleep(0.02)
        live.refresh()
