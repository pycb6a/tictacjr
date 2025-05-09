from collections.abc import Generator
from typing import Protocol, TYPE_CHECKING

from tictacjr.core import settings

if TYPE_CHECKING:
    from tictacjr.core.character import CharacterState


class _MotionActionProtocol(Protocol):
    """Protocol for motion-related actions on a character."""

    state: "CharacterState"
    _stored_state: "CharacterState"

    def _move(self, steps: int, dx: int, dy: int) -> Generator: ...
    def _walk(self, steps: int, dx: int, dy: int) -> Generator: ...
    def _stand(self) -> None: ...
    def _rotate(self, angle_delta: int) -> None: ...
    def reset_state(self) -> None: ...


class _MotionAction:
    """Implements character movement actions."""

    def _move(self: _MotionActionProtocol, steps: int, dx: int, dy: int) -> Generator:
        """Move the character by a number of steps in a direction.

        Args:
            steps (int): Number of steps to move.
            dx (int): X delta per step.
            dy (int): Y delta per step.

        Yields:
            None: Each yield represents a frame of movement.
        """
        if self.state.rect:
            for _ in range(steps):
                self.state.x += dx
                self.state.y += dy
                self.state.rect.center = (
                    self.state.x * settings.SQUARE,
                    self.state.y * settings.SQUARE,
                )
                yield

    def _walk(self: _MotionActionProtocol, steps: int, dx: int, dy: int) -> Generator:
        """Walk (move with sprite change) for a number of steps.

        Args:
            steps (int): Number of steps to walk.
            dx (int): X delta per step.
            dy (int): Y delta per step.

        Yields:
            None: Each yield represents a frame of walking.
        """
        if self.state.rect:
            for _ in range(steps):
                count = len(self.state.sprites)
                if count == 0:
                    return

                self.state.sprite_index = (self.state.sprite_index + 1) % count
                yield from self._move(1, dx, dy)

    def _stand(self: _MotionActionProtocol) -> None:
        """Set the standing (first) sprite for the character."""
        self.state.sprite_index = 0

    def move_right(self: _MotionActionProtocol, steps: int) -> Generator:
        """Move the character to the right.

        Args:
            steps (int): Number of steps to move.

        Yields:
            None: Each yield represents a frame of movement.
        """
        self.state.facing_right = True
        yield from self._walk(steps, dx=1, dy=0)
        self._stand()

    def move_left(self: _MotionActionProtocol, steps: int) -> Generator:
        """Move the character to the left.

        Args:
            steps (int): Number of steps to move.

        Yields:
            None: Each yield represents a frame of movement.
        """
        self.state.facing_right = False
        yield from self._walk(steps, dx=-1, dy=0)
        self._stand()

    def move_up(self: _MotionActionProtocol, steps: int) -> Generator:
        """Move the character up.

        Args:
            steps (int): Number of steps to move up.

        Yields:
            None: Each yield represents a frame of movement.
        """
        yield from self._walk(steps, dx=0, dy=-1)
        self._stand()

    def move_down(self: _MotionActionProtocol, steps: int) -> Generator:
        """Move the character down.

        Args:
            steps (int): Number of steps to move down.

        Yields:
            None: Each yield represents a frame of movement.
        """
        yield from self._walk(steps, dx=0, dy=1)
        self._stand()

    def hop(self: _MotionActionProtocol, height: int) -> Generator:
        """Make the character hop (jump up then down).

        Args:
            height (int): Height of the hop.

        Yields:
            None: Each yield represents a frame of the hop.
        """
        yield from self._move(height, dx=0, dy=-1)
        yield from self._move(height, dx=0, dy=1)

    def go_home(self: _MotionActionProtocol) -> Generator:
        """Move the character to its original/home state.

        Yields:
            None: Single yield after resetting state.
        """
        self.reset_state()
        yield

    def _rotate(self: _MotionActionProtocol, angle_delta: int) -> None:
        """Rotate the character by a given angle.

        Args:
            angle_delta (int): Angle in degrees to rotate.
        """
        self.state.angle = (self.state.angle + angle_delta) % 360

    def turn_right(self: _MotionActionProtocol, steps: int) -> Generator:
        """Turn the character right by 30 degrees per step.

        Args:
            steps (int): Number of steps (30 degrees per step).

        Yields:
            None: Each yield represents a frame of rotation.
        """
        for _ in range(steps):
            self._rotate(30)
            yield

    def turn_left(self: _MotionActionProtocol, steps: int) -> Generator:
        """Turn the character left by 30 degrees per step.

        Args:
            steps (int): Number of steps (30 degrees per step).

        Yields:
            None: Each yield represents a frame of rotation.
        """
        for _ in range(steps):
            self._rotate(-30)
            yield
