from collections.abc import Generator
from enum import Enum
from typing import Iterator, Self, TYPE_CHECKING

if TYPE_CHECKING:
    from tictacjr.core.character import CharacterDoer


class Event(Enum):
    """Enumeration for script events."""

    START_ON_TAP = "start_on_tap"
    START_ON_GREEN_FLAG = "start_on_green_flag"


class _BlockCmd:
    """Represents a single script block command."""

    def __init__(self, block: str, *args) -> None:
        """
        Args:
            block (str): The name/type of the block.
            *args: Block arguments.
        """
        self._block: str = block
        self._args: tuple = args

    def do(self, character: "CharacterDoer") -> Generator:
        """Execute this block command for a given character.

        Args:
            character (CharacterDoer): The character to run the command on.

        Yields:
            None: Each yield represents a frame or step of execution.
        """
        if self._block == "do_block":
            sub_script: ScriptDoer = self._args[0]
            yield from sub_script.play(character)
            return

        method = getattr(character, self._block, None)
        if callable(method):
            gen = method(*self._args)
            if isinstance(gen, Generator):
                yield from gen
        yield


class ScriptDoer:
    """A class for holding a sequence of block commands and their associated event trigger."""

    def __init__(self) -> None:
        self.event: Event | None = None
        self.blocks: list[_BlockCmd] = []

    def __iter__(self) -> Iterator[Self]:
        """Iterate over the script (yields self)."""
        yield self

    def play(self, character: "CharacterDoer") -> Generator:
        """Play all blocks for a character.

        Args:
            character (CharacterDoer): The character to execute the script on.

        Yields:
            None: Each yield represents a frame or step in the script.
        """
        for block in self.blocks:
            yield from block.do(character)
