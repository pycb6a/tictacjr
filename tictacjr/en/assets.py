from enum import Enum
from pathlib import Path

from tictacjr.core import settings


class Background(Enum):
    """Enum for available page backgrounds.

    Each value is the file path to a background SVG image.
    """

    BEDROOM = "bedroom"
    PARK = "park"
    SAVANNAH = "savannah"
    SPRING = "spring"
    SUBURBS = "suburbs"
    SUMMER = "summer"
    THEATRE = "theatre"
    UNDERWATER = "underwater"
    WINTER = "winter"
    WOODS = "woods"

    def __init__(self, value: str) -> None:
        """Set the enum value to the absolute path for the background SVG."""
        self._value_ = str(
            Path(__file__).resolve().parent.parent
            / "images/backgrounds"
            / f"{value}.svg"
        )


class Costume(Enum):
    """Enum for available character costumes.

    Provides file paths for primary and secondary costume SVG images.
    """

    TIC = "tic"
    TAC = "tac"
    TOC = "toc"

    def __init__(self, value: str) -> None:
        """Set primary and secondary costume image file paths."""
        self._value_ = value
        costume_folder = Path(__file__).resolve().parent.parent / "images/characters"
        self.primary = str(costume_folder / f"{value}1.svg")
        self.secondary = str(costume_folder / f"{value}2.svg")


class Color(Enum):
    """Enum for supported colors in the project."""

    BLACK = "black"
    BLUE = "blue"
    BROWN = "brown"
    GRAY = "gray"
    GREEN = "green"
    ORANGE = "orange"
    PINK = "pink"
    PURPLE = "purple"
    RED = "red"
    SKY = "deepskyblue"
    WHITE = "white"
    YELLOW = "yellow"


class Size(Enum):
    """Enum for supported character sizes (percent of medium)."""

    XXS = 25
    XS = 50
    S = 75
    M = 100
    L = 125
    XL = 150
    XXL = 175


class TextSize(Enum):
    """Enum for supported text sizes (multiples of SQUARE)."""

    A = settings.SQUARE
    AA = 2 * settings.SQUARE
    AAA = 3 * settings.SQUARE
    AAAA = 4 * settings.SQUARE
    AAAAA = 5 * settings.SQUARE
