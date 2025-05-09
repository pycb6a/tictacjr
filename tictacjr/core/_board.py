from collections.abc import Generator
from pathlib import Path

import pygame

from tictacjr.core import settings


class _BoardButton:
    """Button base class for the control board.

    Args:
        name (str): The name identifier for the button, used for loading sprites.
        x (int): The X coordinate of the button on the board.
        y (int): The Y coordinate of the button on the board.
    """

    def __init__(self, name: str, x: int, y: int) -> None:
        self._x: int = x
        self._y: int = y
        costume_folder = Path(__file__).resolve().parent.parent / "images/controls"
        self._sprite_index: int = 0
        self._sprites: list[pygame.Surface] = [
            pygame.image.load(str(costume_folder / f"{name}1.svg")),
            pygame.image.load(str(costume_folder / f"{name}2.svg")),
        ]
        self._rect: pygame.Rect | None = None

    @property
    def sprite(self) -> pygame.Surface:
        """Get the current sprite surface for the button.

        Returns:
            pygame.Surface: The currently displayed sprite.
        """
        return self._sprites[self._sprite_index]

    @property
    def rect(self) -> pygame.Rect:
        """Get the bounding rectangle for the button.

        Returns:
            pygame.Rect: The rectangle aligned with the button sprite.
        """
        if self._rect is None:
            self._rect = self.sprite.get_rect(topleft=(self._x, self._y))
        return self._rect

    def _next_sprite(self) -> None:
        """Advance to the next sprite (for toggling button appearance)."""
        self._sprite_index = (self._sprite_index + 1) % len(self._sprites)


class _GreenFlagButton(_BoardButton):
    """Button class representing the green flag (start/play control)."""

    def __init__(self, name: str, x: int, y: int) -> None:
        super().__init__(name, x, y)
        self.playing: bool = False

    def press(self) -> None:
        """Simulate pressing the green flag button.

        Toggles the sprite and updates the playing status.
        """
        self._next_sprite()
        self.playing = bool(self._sprite_index)


class _ResetButton(_BoardButton):
    """Button class representing the reset control."""

    def press(self) -> Generator:
        """Simulate pressing the reset button.

        This toggles the sprite, yields control for animation,
        then toggles back.

        Yields:
            None: Used for animation in event loop.
        """
        self._next_sprite()
        yield
        self._next_sprite()


class _ControlBoard:
    """Control board containing interactive buttons.

    Args:
        scene_width (int): The width of the scene, used for positioning.
    """

    def __init__(self, scene_width: int) -> None:
        spacing = 3 * settings.SQUARE
        top_y = settings.SQUARE
        reset_x = scene_width - spacing
        green_flag_x = reset_x - spacing

        self.green_flag = _GreenFlagButton(
            name="green_flag",
            x=green_flag_x,
            y=top_y,
        )
        self.reset = _ResetButton(
            name="reset",
            x=reset_x,
            y=top_y,
        )

    def items(self) -> Generator[_BoardButton, None, None]:
        """Yield all control board buttons.

        Yields:
            _BoardButton: Each button on the control board.
        """
        for attr in ("green_flag", "reset"):
            yield getattr(self, attr)
