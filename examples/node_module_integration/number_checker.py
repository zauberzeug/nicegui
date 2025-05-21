from nicegui import ui


class NumberChecker(ui.element, component='number_checker.js', dependencies=['dist/is-odd.js']):

    def __init__(self) -> None:
        """NumberChecker

        A number checker based on the `is-odd <https://www.npmjs.com/package/is-odd>`_ NPM package.
        """
        super().__init__()

    async def is_odd(self, number: int) -> bool:
        """Check if a number is odd."""
        return await self.run_method('isOdd', number)

    async def is_even(self, number: int) -> bool:
        """Check if a number is even."""
        return await self.run_method('isEven', number)
