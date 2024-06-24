from dataclasses import dataclass
from pathlib import Path

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.message import Message
from textual.widgets import Button, Markdown
from textual.widgets._markdown import (
    HEADINGS,
    AwaitComplete,
    MarkdownBlock,
    MarkdownBlockQuote,
    MarkdownBulletList,
)
from textual.widgets._markdown import MarkdownFence as OriginalMarkdownFence
from textual.widgets._markdown import (
    MarkdownHorizontalRule,
    MarkdownIt,
    MarkdownOrderedList,
    MarkdownOrderedListItem,
    MarkdownParagraph,
    MarkdownTable,
    MarkdownTBody,
    MarkdownTD,
    MarkdownTH,
    MarkdownTHead,
    MarkdownTR,
    MarkdownUnorderedListItem,
)


class MarkdownFence(OriginalMarkdownFence):

    def __init__(self, markdown: Markdown, code: str, lexer: str) -> None:
        super(OriginalMarkdownFence, self).__init__(markdown)
        self.code = code
        self.lexer = lexer
        self.theme = self._markdown.code_dark_theme


class FasterMarkdown(Markdown):
    def update(self, markdown: str) -> AwaitComplete:
        """Update the document with new Markdown.

        Args:
            markdown: A string containing Markdown.

        Returns:
            An optionally awaitable object. Await this to ensure that all children have been mounted.
        """
        output = self.parse_markdown(markdown)
        return self.render_markdown(output)

    async def render_markdown(self, output):
        self.post_message(
            Markdown.TableOfContentsUpdated(self, self._table_of_contents).set_sender(
                self
            )
        )
        markdown_block = self.query("MarkdownBlock")

        async def await_update() -> None:
            """Update in a single batch."""

            with self.app.batch_update():
                await markdown_block.remove()
                await self.mount_all(output)

        return AwaitComplete(await_update())

    def parse_markdown(self, markdown):
        output: list[MarkdownBlock] = []
        stack: list[MarkdownBlock] = []
        parser = (
            MarkdownIt("gfm-like")
            if self._parser_factory is None
            else self._parser_factory()
        )

        block_id: int = 0
        self._table_of_contents = []

        for token in parser.parse(markdown):
            if token.type == "heading_open":
                block_id += 1
                stack.append(HEADINGS[token.tag](self, id=f"block{block_id}"))
            elif token.type == "hr":
                output.append(MarkdownHorizontalRule(self))
            elif token.type == "paragraph_open":
                stack.append(MarkdownParagraph(self))
            elif token.type == "blockquote_open":
                stack.append(MarkdownBlockQuote(self))
            elif token.type == "bullet_list_open":
                stack.append(MarkdownBulletList(self))
            elif token.type == "ordered_list_open":
                stack.append(MarkdownOrderedList(self))
            elif token.type == "list_item_open":
                if token.info:
                    stack.append(MarkdownOrderedListItem(self, token.info))
                else:
                    item_count = sum(
                        1
                        for block in stack
                        if isinstance(block, MarkdownUnorderedListItem)
                    )
                    stack.append(
                        MarkdownUnorderedListItem(
                            self,
                            self.BULLETS[item_count % len(self.BULLETS)],
                        )
                    )

            elif token.type == "table_open":
                stack.append(MarkdownTable(self))
            elif token.type == "tbody_open":
                stack.append(MarkdownTBody(self))
            elif token.type == "thead_open":
                stack.append(MarkdownTHead(self))
            elif token.type == "tr_open":
                stack.append(MarkdownTR(self))
            elif token.type == "th_open":
                stack.append(MarkdownTH(self))
            elif token.type == "td_open":
                stack.append(MarkdownTD(self))
            elif token.type.endswith("_close"):
                block = stack.pop()
                if token.type == "heading_close":
                    heading = block._text.plain
                    level = int(token.tag[1:])
                    self._table_of_contents.append((level, heading, block.id))
                if stack:
                    stack[-1]._blocks.append(block)
                else:
                    output.append(block)
            elif token.type == "inline":
                stack[-1].build_from_token(token)
            elif token.type in ("fence", "code_block"):
                (stack[-1]._blocks if stack else output).append(
                    MarkdownFence(self, token.content.rstrip(), token.info)
                )
            else:
                external = self.unhandled_token(token)
                if external is not None:
                    (stack[-1]._blocks if stack else output).append(external)
        return output


class LoadMarkdownApp(App[None]):

    CSS = """
    Markdown {
        border: solid red;
        height: auto;
        min-height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Button()
        with VerticalScroll():
            yield FasterMarkdown()

    @on(Button.Pressed)
    def start_load(self) -> None:
        self.query_one(FasterMarkdown).loading = True
        self.load_markdown()

    @dataclass
    class NewDocument(Message):
        markdown: str

    @work(thread=True)
    def load_markdown(self) -> None:
        # self.post_message(self.NewDocument(Path("test.md").read_text()))
        markdown = Path("test.md").read_text()
        output = self.query_one(FasterMarkdown).parse_markdown(markdown)
        self.post_message(self.NewDocument(output))

    @on(NewDocument)
    async def display_document(self, event: NewDocument) -> None:
        # await self.query_one(Markdown).update(event.markdown)
        await self.query_one(FasterMarkdown).render_markdown(event.markdown)
        self.query_one(FasterMarkdown).loading = False


if __name__ == "__main__":
    LoadMarkdownApp().run()
