from textual.app import App, ComposeResult
from textual_plotext import PlotextPlot


class PlotApp(App[None]):
    def compose(self) -> ComposeResult:
        yield PlotextPlot()

    def on_mount(self) -> None:
        plt = self.query_one(PlotextPlot).plt
        plt.plot(plt.sin())


if __name__ == "__main__":
    PlotApp().run()
