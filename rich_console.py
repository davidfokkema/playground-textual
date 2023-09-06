from rich import print
from rich.console import Console
from rich.text import Text

console = Console()

console.out(Text.from_ansi("Foo"))
console.out(Text.from_ansi("Bar"))
console.out(Text.from_ansi("\033[2FMoo"))
console.out(Text.from_ansi("Bax"))

# print("Hi")
# print("There")
# print("\033[1mMy text overwriting the previous line.")
# print("\033[FMy text overwriting the previous line.")
