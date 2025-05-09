from collections.abc import Iterator

from tictacjr.core import settings
from tictacjr.core.block import Block
from tictacjr.core.character import CharacterDoer, CharacterState
from tictacjr.core.script import Event, ScriptDoer
from tictacjr.core.stage import Stage
from tictacjr.en import Background, Color, Costume, Size, TextSize


class Label:
    """A label representing a text annotation on a page."""

    def __init__(self) -> None:
        self._text: str = ""
        self._color: Color = Color.BLACK
        self._size: TextSize = TextSize.AAA
        self._x: int = 20 * settings.SQUARE
        self._y: int = 5 * settings.SQUARE

    def __iter__(self):
        """Make Label iterable (yields self)."""
        yield self

    @property
    def text(self) -> str:
        """Get or set the label's text."""
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    @property
    def color(self) -> Color:
        """Get or set the label's color."""
        return self._color

    @color.setter
    def color(self, value: Color) -> None:
        self._color = value

    @property
    def size(self) -> TextSize:
        """Get or set the label's font size."""
        return self._size

    @size.setter
    def size(self, value: TextSize) -> None:
        self._size = value

    @property
    def x(self) -> int:
        """Get or set the label's x position (in pixels)."""
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value * settings.SQUARE

    @property
    def y(self) -> int:
        """Get or set the label's y position (in pixels)."""
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value * settings.SQUARE


class Page:
    """A page containing a background, labels, and characters."""

    def __init__(self) -> None:
        self._background: Background | None = None
        self._labels: list[Label] = []
        self._characters: list[CharacterDoer] = []

    def __iter__(self):
        """Make Page iterable (yields self)."""
        yield self

    @property
    def background(self) -> Background | None:
        """Get or set the page's background."""
        return self._background

    @background.setter
    def background(self, value: Background) -> None:
        self._background = value

    @property
    def labels(self) -> list[Label]:
        """Get or set the list of labels on the page."""
        return self._labels

    @labels.setter
    def labels(self, values: list[Label]) -> None:
        self._labels = values

    @property
    def characters(self) -> list[CharacterDoer]:
        """Get or set the list of characters on the page."""
        return self._characters

    @characters.setter
    def characters(self, values: list[CharacterDoer]) -> None:
        self._characters = values


class Project:
    """A project containing title, window size, grid setting, and pages."""

    def __init__(self) -> None:
        self._title: str = "Welcome to TicTac Junior!"
        self._window: tuple[int, int] = (
            settings.WINDOW[0] * settings.SQUARE,
            settings.WINDOW[1] * settings.SQUARE,
        )
        self._grid_on: bool = False
        self._pages: list[Page] = []

    @property
    def title(self) -> str:
        """Get or set the project title."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value

    @property
    def window(self) -> tuple[int, int]:
        """Get or set the project window size."""
        return self._window

    @window.setter
    def window(self, value: tuple[int, int]) -> None:
        width = max(settings.MIN_WINDOW[0], min(value[0], settings.MAX_WINDOW[0]))
        height = max(settings.MIN_WINDOW[1], min(value[1], settings.MAX_WINDOW[1]))
        self._window = (
            width * settings.SQUARE,
            height * settings.SQUARE,
        )

    @property
    def pages(self) -> list[Page]:
        """Get or set the project's pages."""
        return self._pages

    @pages.setter
    def pages(self, values: list[Page]) -> None:
        self._pages = values

    def set_grid(self) -> None:
        """Enable grid overlay for the project."""
        self._grid_on = True

    def start(self, stage: Stage | None = None) -> None:
        """Start the project, launching the stage.

        Args:
            stage (Stage, optional): Optionally provide a pre-built Stage instance.
        """
        if not self.pages:
            self.pages += Page()
        if not stage:
            stage = Stage(
                title=self._title,
                window=self._window,
                pages=self._pages,
                grid_on=self._grid_on,
            )
        stage.play()


class Character:
    """A user-facing character for the project."""

    def __init__(self) -> None:
        self._state: CharacterState = CharacterState()

    def __iter__(self) -> Iterator[CharacterDoer]:
        """Make Character iterable, yielding a CharacterDoer."""
        yield CharacterDoer(self._state)

    @property
    def costume(self) -> Costume:
        """Get or set the character's costume."""
        return self._state.costume

    @costume.setter
    def costume(self, value: Costume) -> None:
        self._state.costume = value

    @property
    def size(self) -> Size:
        """Get or set the character's size."""
        return self._state.size

    @size.setter
    def size(self, value: Size) -> None:
        self._state.size = value

    @property
    def x(self) -> int:
        """Get or set the character's x coordinate."""
        return self._state.x

    @x.setter
    def x(self, value: int) -> None:
        self._state.x = value

    @property
    def y(self) -> int:
        """Get or set the character's y coordinate."""
        return self._state.y

    @y.setter
    def y(self, value: int) -> None:
        self._state.y = value

    @property
    def scripts(self) -> list[ScriptDoer]:
        """Get or set the character's scripts."""
        return self._state.scripts

    @scripts.setter
    def scripts(self, values: list[ScriptDoer]) -> None:
        self._state.scripts = values

    def hide(self):
        """Hide the character (set visible to False)."""
        self._state.visible = False


class Script:
    """A script builder for creating event-driven logic."""

    def __init__(self) -> None:
        self._script: ScriptDoer = ScriptDoer()

    def __iter__(self) -> Iterator[ScriptDoer]:
        """Make Script iterable, yielding its ScriptDoer."""
        yield self._script

    @staticmethod
    def make_block() -> Block:
        """Create a new block for a script (not bound to an event)."""
        return Block(ScriptDoer())

    def _start_on_event(self, event: Event) -> Block:
        """Bind the script to start on a specific event."""
        self._script.event = event
        return Block(self._script)

    def start_on_tap(self) -> Block:
        """Configure the script to start on tap."""
        return self._start_on_event(Event.START_ON_TAP)

    def start_on_green_flag(self) -> Block:
        """Configure the script to start on green flag."""
        return self._start_on_event(Event.START_ON_GREEN_FLAG)
