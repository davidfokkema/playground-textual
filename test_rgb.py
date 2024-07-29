import asyncio

from textual.color import Color

from rgb import RGBApp


async def test_keys():
    """Test pressing keys has the desired result."""
    app = RGBApp()
    async with app.run_test(headless=False) as pilot:
        # Test pressing the R key
        await pilot.press("r")
        assert app.screen.styles.background == Color.parse("red")
        await pilot.pause(delay=0.5)

        # Test pressing the G key
        await pilot.press("g")
        assert app.screen.styles.background == Color.parse("green")
        await pilot.pause(delay=0.5)

        # Test pressing the B key
        await pilot.press("b")
        assert app.screen.styles.background == Color.parse("blue")

        # Test pressing the X key
        await pilot.press("x")
        # No binding (so no change to the color)
        assert app.screen.styles.background == Color.parse("blue")


async def test_buttons():
    """Test pressing keys has the desired result."""
    app = RGBApp()
    async with app.run_test() as pilot:
        # Test clicking the "red" button
        await pilot.click("#red")
        assert app.screen.styles.background == Color.parse("red")

        # Test clicking the "green" button
        await pilot.click("#green")
        assert app.screen.styles.background == Color.parse("green")

        # Test clicking the "blue" button
        await pilot.click("#blue")
        assert app.screen.styles.background == Color.parse("blue")


asyncio.run(test_keys())
