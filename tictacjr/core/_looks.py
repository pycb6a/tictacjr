from collections.abc import Generator
from typing import Protocol, TYPE_CHECKING

from tictacjr.en import Size

if TYPE_CHECKING:
    from tictacjr.core.character import CharacterState


class _LooksActionProtocol(Protocol):
    """Protocol for looks-related actions on a character."""

    state: "CharacterState"
    _stored_state: "CharacterState"

    def _scale(self, steps: int | None = None) -> Generator: ...


class _LooksAction:
    """Implements character visual/looks actions."""

    def say(
        self: _LooksActionProtocol, text: str, ticks: int | None = None
    ) -> Generator:
        """Display speech text above the character for a given number of ticks.

        Args:
            text (str): The text to display.
            ticks (int, optional): Duration to display. Defaults to 2 * len(text).

        Yields:
            None: Each yield represents a frame with text displayed.
        """
        self.state.say_text = text
        if ticks is None:
            ticks = 2 * len(text)

        for _ in range(ticks):
            yield
        self.state.say_text = None

    def _scale(self: _LooksActionProtocol, steps: int | None = None) -> Generator:
        """Scale the character size up or down by a number of steps.

        Args:
            steps (int, optional): Number of steps to scale. If None, reset to stored size.

        Yields:
            None: Each yield represents a frame of scaling.
        """
        sizes = list(Size)
        current_index = sizes.index(self.state.size)
        target_index = (
            sizes.index(self._stored_state.size)
            if steps is None
            else max(0, min(current_index + steps, len(sizes) - 1))
        )
        if current_index == target_index:
            return

        step = 1 if target_index > current_index else -1
        for i in range(current_index + step, target_index + step, step):
            self.state.size = sizes[i]
            yield

    def grow(self: _LooksActionProtocol, steps: int = 1) -> Generator:
        """Increase the character's size.

        Args:
            steps (int, optional): Number of size steps to increase. Defaults to 1.

        Yields:
            None: Each yield represents a frame of growing.
        """
        yield from self._scale(steps)

    def shrink(self: _LooksActionProtocol, steps: int = 1) -> Generator:
        """Decrease the character's size.

        Args:
            steps (int, optional): Number of size steps to decrease. Defaults to 1.

        Yields:
            None: Each yield represents a frame of shrinking.
        """
        yield from self._scale(-steps)

    def reset_size(self: _LooksActionProtocol) -> Generator:
        """Reset the character's size to its stored/original value.

        Yields:
            None: Each yield represents a frame of resetting size.
        """
        yield from self._scale()

    def hide(self: _LooksActionProtocol) -> Generator:
        """Hide the character (make invisible).

        Yields:
            None: Single yield after hiding.
        """
        self.state.visible = False
        yield

    def show(self: _LooksActionProtocol) -> Generator:
        """Show the character (make visible).

        Yields:
            None: Single yield after showing.
        """
        self.state.visible = True
        yield
