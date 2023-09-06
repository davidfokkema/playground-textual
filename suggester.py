from textual.app import App
from textual.suggester import Suggester, SuggestFromList
from textual.widgets import Input
from thefuzz import process

countries = ["England", "Scotland", "Portugal", "Spain", "France"]


class FuzzySuggester(Suggester):
    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices

    async def get_suggestion(self, value):
        return process.extractOne(value, self.choices)[0]


class MyApp(App):
    def compose(self):
        yield Input(suggester=SuggestFromList(countries, case_sensitive=False))
        yield Input(suggester=FuzzySuggester(countries))


if __name__ == "__main__":
    app = MyApp()
    app.run()
