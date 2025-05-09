import copy
from collections.abc import Generator

import pygame

from tictacjr.core import settings
from tictacjr.core._control import _ControlAction
from tictacjr.core._looks import _LooksAction
from tictacjr.core._motion import _MotionAction
from tictacjr.core.script import _BlockCmd, ScriptDoer
from tictacjr.en import Costume, Size


class CharacterState:
    """Stores the state of a character in the game."""

    def __init__(self) -> None:
        """Initialize the character state with default values."""
        self.size: Size = Size.M
        self.x: int = 20
        self.y: int = 15
        self.visible: bool = True
        self.costume: Costume = Costume.TIC
        self.sprites: list[pygame.Surface] = []
        self.sprite_index: int = 0
        self.facing_right: bool = True
        self.angle: int = 0
        self.say_text: str | None = None
        self.scripts: list[ScriptDoer] = []
        self._rect: pygame.Rect | None = None

    @property
    def sprite(self) -> pygame.Surface:
        """Get the current sprite Surface for the character, applying size, angle, and flip.

        Returns:
            pygame.Surface: The current transformed sprite surface.
        """
        if not self.sprites:
            self.sprites: list[pygame.Surface] = [
                pygame.image.load(self.costume.primary),
                pygame.image.load(self.costume.secondary),
            ]
        sprite = self.sprites[self.sprite_index]

        if self.size != Size.M:
            width = int(sprite.get_width() * self.size.value / Size.M.value)
            height = int(sprite.get_height() * self.size.value / Size.M.value)
            sprite = pygame.transform.scale(sprite, (width, height))

        sprite = pygame.transform.rotate(sprite, self.angle)

        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        return sprite

    @property
    def rect(self) -> pygame.Rect:
        """Get the current bounding rectangle for the character sprite.

        Returns:
            pygame.Rect: The rect representing the current position and size of the sprite.
        """
        if self._rect is None:
            self._rect = self.sprite.get_rect(
                center=(self.x * settings.SQUARE, self.y * settings.SQUARE)
            )
        return self._rect


class CharacterDoer(_MotionAction, _LooksAction, _ControlAction):
    """Provides methods for performing actions on a character state.

    Args:
        state (CharacterState): The character state to manipulate.
    """

    def __init__(self, state: CharacterState) -> None:
        super().__init__()
        self.state: CharacterState = state
        self._stored_state: CharacterState | None = None

    def __repr__(self):
        """Return the string representation (costume name) for the character."""
        return self.state.costume.name

    def repeat(self, times: int, blocks: list[_BlockCmd]) -> Generator:
        """Repeat a list of block commands a given number of times.

        Args:
            times (int): Number of repetitions.
            blocks (list[_BlockCmd]): Block commands to repeat.

        Yields:
            None: Each yield represents a step in the repeated execution.
        """
        for _ in range(times):
            for block in blocks:
                yield from block.do(self)

    def repeat_forever(self, blocks: list[_BlockCmd]) -> Generator:
        """Repeat a list of block commands forever.

        Args:
            blocks (list[_BlockCmd]): Block commands to repeat.

        Yields:
            None: Each yield represents a step in the repeated execution.
        """
        while True:
            for block in blocks:
                yield from block.do(self)

    def store_state(self) -> None:
        """Store a deep copy of the current state for later reset."""
        self._stored_state = copy.deepcopy(self.state)

    def reset_state(self) -> None:
        """Reset the character state to the previously stored state."""
        if self._stored_state:
            self.state = copy.deepcopy(self._stored_state)
