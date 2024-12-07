"""Fake RSS reader app using a ContentSwitcher."""

from faker import Faker
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widgets import (
    ContentSwitcher,
    Footer,
    Header,
    Label,
    ListItem,
    ListView,
    Markdown,
    Placeholder,
)


def get_feed_list() -> list[str]:
    Faker.seed(1)
    fake = Faker()
    return [f"{fake.word()} Feed" for _ in range(4)]


def get_article_list(feed: str) -> list[str]:
    fake = Faker()
    fake.seed_instance(feed)
    return [fake.sentence() for _ in range(7)]


def get_article(feed: str, article: str) -> str:
    fake = Faker()
    fake.seed_instance(feed + article)
    return "\n\n".join(fake.paragraphs(5))


class ArticleView(Markdown):
    BINDINGS = [("escape", "go_back", "Return to article list")]

    can_focus = True

    class GoBack(Message): ...

    def action_go_back(self) -> None:
        self.post_message(self.GoBack())


class ArticleItem(ListItem):
    def __init__(self, article: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.article = article

    def compose(self) -> ComposeResult:
        yield Label(self.article)


class ArticleList(ListView):
    BINDINGS = [("escape", "go_back", "Return to feed list")]

    class GoBack(Message): ...

    feed: str

    def update_articles(self, feed: str, articles: list[str]) -> None:
        self.clear()
        self.feed = feed
        for article in articles:
            self.append(ArticleItem(article))

    def action_go_back(self) -> None:
        self.post_message(self.GoBack())


class FeedItem(ListItem):
    def __init__(self, feed: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.feed = feed

    def compose(self) -> ComposeResult:
        yield Label(self.feed)


class FeedList(ListView):
    def update_feeds(self, feeds: list[str]) -> None:
        self.clear()
        for feed in feeds:
            self.append(FeedItem(feed))


class FeedReaderApp(App[None]):
    CSS = """
        Vertical > Placeholder {
            height: 10%;
        }

        Horizontal > Placeholder {
            width: 10%;
        }

        ListItem > Label {
            padding: 1 2;
        }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Vertical():
            yield Placeholder()
            with Horizontal():
                yield Placeholder()
                with ContentSwitcher(initial="feed_list"):
                    yield FeedList(id="feed_list")
                    yield ArticleList(id="article_list")
                    yield ArticleView(id="article_view")
                yield Placeholder()
            yield Placeholder()

    def on_mount(self) -> None:
        self.query_one(FeedList).update_feeds(get_feed_list())

    @on(ListView.Selected, "#feed_list")
    def select_feed(self, event: ListView.Selected) -> None:
        feed = event.item.feed
        self.query_one(ArticleList).update_articles(feed, get_article_list(feed))
        self.query_one(ContentSwitcher).current = "article_list"

    @on(ListView.Selected, "#article_list")
    def select_article(self, event: ListView.Selected) -> None:
        self.query_one("#article_view", Markdown).update(
            get_article(event.list_view.feed, event.item.article)
        )
        self.query_one(ContentSwitcher).current = "article_view"

    @on(ArticleList.GoBack)
    def return_to_feed_list(self) -> None:
        self.query_one(ContentSwitcher).current = "feed_list"

    @on(ArticleView.GoBack)
    def return_to_article_list(self) -> None:
        self.query_one(ContentSwitcher).current = "article_list"


FeedReaderApp().run()
