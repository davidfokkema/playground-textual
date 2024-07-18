import asyncio

import httpx
from textual import work
from textual.app import App, ComposeResult
from textual.widgets import OptionList
from textual.widgets.option_list import Option


class OptionListAPIApp(App[None]):
    def compose(self) -> ComposeResult:
        yield OptionList()

    def on_mount(self) -> None:
        option_list = self.query_one(OptionList)
        option_list.loading = True
        self.load_data(option_list)

    @work
    async def load_data(self, option_list: OptionList) -> None:
        # REMOVE THE SLEEP IN PRODUCTION
        await asyncio.sleep(2)

        async with httpx.AsyncClient() as client:
            r = await client.get("https://jsonplaceholder.typicode.com/users")
            for user in r.json():
                option_list.add_option(
                    Option(f"{user['name']} [underline]({user['email']})[/]")
                )
        option_list.loading = False


OptionListAPIApp().run()
