from rich.style import Style
from textual.app import App, ComposeResult, RenderResult
from textual.color import Gradient
from textual.renderables.bar import Bar as BarRenderable
from textual.widgets import ProgressBar
from textual.widgets._progress_bar import Bar, ETAStatus, PercentageStatus


class GradientBar(Bar):
    def render(self) -> RenderResult:
        """Render the bar with the correct portion filled."""
        if self.percentage is None:
            return self.render_indeterminate()
        else:
            bar_style = (
                self.get_component_rich_style("bar--bar")
                if self.percentage < 1
                else self.get_component_rich_style("bar--complete")
            )
            return BarRenderable(
                highlight_range=(0, self.size.width * self.percentage),
                highlight_style=Style.from_color(
                    self.gradient.get_rich_color(self.percentage)
                ),
                background_style=Style.from_color(bar_style.bgcolor),
            )


class GradientProgressBar(ProgressBar):
    def compose(self) -> ComposeResult:
        if self.show_bar:
            yield (
                GradientBar(id="bar", clock=self._clock)
                .data_bind(ProgressBar.percentage)
                .data_bind(ProgressBar.gradient)
            )
        if self.show_percentage:
            yield PercentageStatus(id="percentage").data_bind(ProgressBar.percentage)
        if self.show_eta:
            yield ETAStatus(id="eta").data_bind(eta=ProgressBar._display_eta)


class DemoApp(App[None]):
    def compose(self) -> ComposeResult:
        yield GradientProgressBar(
            total=100, gradient=Gradient.from_colors("red", "orange", "#4EBF71")
        )
        yield ProgressBar(total=100)

    def on_mount(self) -> None:
        self.progress_timer = self.set_interval(1 / 10, self.make_progress)

    def make_progress(self) -> None:
        for bar in self.query(ProgressBar):
            bar.advance(1)


DemoApp().run()
