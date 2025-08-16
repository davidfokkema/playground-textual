from textual.app import App, ComposeResult
from textual.widgets import Label, ListItem, ListView


class MinimalApp(App[None]):
    def compose(self) -> ComposeResult:
        yield ListView()

    async def on_mount(self) -> None:
        list_view = self.query_one(ListView)
        for i in range(5):
            item = ListItem(Label(f"Item {i}"), id=f"ID{i}")
            list_view.append(item)

        await list_view.clear()

        for i in range(5):
            item = ListItem(Label(f"Duplicate item {i}"), id=f"ID{i}")
            list_view.append(item)


MinimalApp().run()
