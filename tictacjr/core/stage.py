from collections.abc import Generator
from typing import Callable, Protocol, TYPE_CHECKING

import pygame

from tictacjr.core import settings
from tictacjr.core._board import _ControlBoard
from tictacjr.core.character import CharacterDoer
from tictacjr.core.script import Event
from tictacjr.en import Color
from tictacjr.en import TextSize

if TYPE_CHECKING:
    from tictacjr.en import Page


class _XYProtocol(Protocol):
    """Protocol for objects with x, y coordinates."""

    @property
    def x(self) -> int: ...
    @property
    def y(self) -> int: ...


class _PageKeeper:
    """Keeps track of pages and manages the current page."""

    def __init__(self, pages: list["Page"], width: int, height: int) -> None:
        """
        Args:
            pages (list[Page]): All available pages.
            width (int): Scene width (for boundary checking).
            height (int): Scene height (for boundary checking).
        """
        self._pages: list["Page"] = self._keep_on_scene(pages, width, height)
        self._current_page: "Page" = self._pages[0]

    @property
    def current(self) -> "Page":
        """Get the currently active page.

        Returns:
            Page: The current page object.
        """
        return self._current_page

    def store_states(self) -> None:
        """Store the state of all characters in the current page."""
        for character in self._current_page.characters:
            character.store_state()

    def reset_states(self) -> None:
        """Reset the state of all characters in the current page."""
        for character in self._current_page.characters:
            character.reset_state()

    @staticmethod
    def _keep_on_scene(pages: list["Page"], width: int, height: int) -> list["Page"]:
        """Filter page labels and characters to keep them within scene bounds.

        Args:
            pages (list[Page]): List of all pages.
            width (int): Scene width.
            height (int): Scene height.

        Returns:
            list[Page]: List of all pages with filtered page labels and characters.
        """

        def _inside(
            obj: _XYProtocol,
        ) -> bool:
            return 0 <= obj.x <= width and 0 <= obj.y <= height

        for page in pages:
            page.labels = [label for label in page.labels if _inside(label)]
            page.characters = [
                character for character in page.characters if _inside(character.state)
            ]

        return pages


class _SceneDrawer:
    """Handles drawing the current scene and its elements."""

    def __init__(
        self,
        scene: pygame.Surface,
        board: _ControlBoard,
        page_keeper: _PageKeeper,
        grid_on: bool,
    ) -> None:
        """
        Args:
            scene (pygame.Surface): The main scene surface.
            board (_ControlBoard): The control board.
            page_keeper (_PageKeeper): Page keeper.
            grid_on (bool): Whether to draw the grid overlay.
        """
        self._scene = scene
        self._control_board = board
        self._page_keeper = page_keeper
        self._grid_on = grid_on

    def draw(self) -> None:
        """Draw the current scene, including background, grid, labels, characters, and controls."""
        self._scene.fill(Color.WHITE.value)
        page = self._page_keeper.current

        if page.background:
            bg = pygame.transform.scale(
                pygame.image.load(page.background.value), self._scene.get_size()
            )
            self._scene.blit(bg, (0, 0))

        if self._grid_on:
            self._draw_grid()

        for label in page.labels:
            font = pygame.font.Font(None, label.size.value)
            surf = font.render(label.text, True, label.color.value)
            self._scene.blit(surf, surf.get_rect(center=(label.x, label.y)).topleft)

        for character in page.characters:
            if character.state.visible:
                self._scene.blit(character.state.sprite, character.state.rect.topleft)
                if character.state.say_text:
                    self._draw_bubble(character)

        for control in self._control_board.items():
            self._scene.blit(control.sprite, control.rect.topleft)

    def _draw_grid(self) -> None:
        """Draw the grid lines and labels on the scene."""
        square = settings.SQUARE
        width, height = self._scene.get_size()
        cols, rows = width // square, height // square
        font_size = TextSize.A.value // 2
        font = pygame.font.Font(None, font_size)
        color = Color.GRAY.value

        for i in range(cols + 1):
            x = i * square
            pygame.draw.line(self._scene, color, (x, 0), (x, height))
        for j in range(rows + 1):
            y = j * square
            pygame.draw.line(self._scene, color, (0, y), (width, y))
        for i in range(cols):
            x = i * square + square // 2
            number_surf = font.render(str(i + 1), True, color)
            number_rect = number_surf.get_rect(center=(x, 10))
            self._scene.blit(number_surf, number_rect)
        for j in range(1, rows):
            y = j * square + square // 2
            number_surf = font.render(str(j + 1), True, color)
            number_rect = number_surf.get_rect(center=(10, y))
            self._scene.blit(number_surf, number_rect)

    def _draw_bubble(self, character: CharacterDoer) -> None:
        """Draw a speech bubble above a character.

        Args:
            character (CharacterDoer): The character whose speech is to be rendered.
        """
        text = character.state.say_text
        if not text:
            return

        font_size = TextSize.A.value
        half, quarter = font_size // 2, font_size // 4

        pos_x, pos_y = character.state.rect.midtop
        bubble_y = pos_y - font_size

        font = pygame.font.Font(None, font_size)
        text_surf = font.render(text, True, Color.WHITE.value)
        text_rect = text_surf.get_rect()

        bubble_width = text_rect.width + font_size
        bubble_height = text_rect.height + font_size
        bubble_rect = pygame.Rect(0, 0, bubble_width, bubble_height)
        bubble_rect.midbottom = (pos_x, bubble_y - quarter)
        pygame.draw.rect(
            self._scene, Color.SKY.value, bubble_rect, border_radius=quarter
        )
        tail_top_y = bubble_y - half
        tail_points = [
            (pos_x - half, tail_top_y),
            (pos_x + half, tail_top_y),
            (pos_x, bubble_y),
        ]
        pygame.draw.polygon(self._scene, Color.SKY.value, tail_points)
        text_pos = (bubble_rect.x + half, bubble_rect.y + half)
        self._scene.blit(text_surf, text_pos)


class _EventHandler:
    """Handles user input events and script execution."""

    def __init__(self, control_board: _ControlBoard, page_keeper: _PageKeeper) -> None:
        """
        Args:
            control_board (_ControlBoard): Control board.
            page_keeper (_PageKeeper): Page keeper.
        """
        self._control_board = control_board
        self._page_keeper = page_keeper
        self._current_scripts: list[Generator] = []

    def handle_taps(self, stop: Callable) -> None:
        """Handle tap and quit events, dispatching to respective handlers.

        Args:
            stop (Callable): Function to call on quit event.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._on_green_flag(event.pos)
                self._on_reset(event.pos)
                self._on_tap(event.pos)
        self._play_scripts()

    def _on_green_flag(self, pos: tuple[int, int]) -> None:
        """Handle green flag button press event.

        Args:
            pos (tuple[int, int]): Position of the mouse event.
        """
        if self._control_board.green_flag.rect.collidepoint(pos):
            self._control_board.green_flag.press()

            if self._control_board.green_flag.playing:
                for character in self._page_keeper.current.characters:
                    for script in character.state.scripts:
                        if script.event == Event.START_ON_GREEN_FLAG:
                            self._current_scripts.append(script.play(character))
            else:
                self._current_scripts.clear()

    def _on_reset(self, pos: tuple[int, int]) -> None:
        """Handle reset button press event.

        Args:
            pos (tuple[int, int]): Position of the mouse event.
        """
        if self._control_board.reset.rect.collidepoint(pos):
            for character in self._page_keeper.current.characters:
                character.reset_state()
            self._current_scripts.clear()

            if self._control_board.green_flag.playing:
                self._control_board.green_flag.press()
            self._current_scripts.append(self._control_board.reset.press())

    def _on_tap(self, pos: tuple[int, int]) -> None:
        """Handle tap event on characters.

        Args:
            pos (tuple[int, int]): Position of the mouse event.
        """
        for character in self._page_keeper.current.characters:
            for script in character.state.scripts:
                if (
                    script.event == Event.START_ON_TAP
                    and character.state.rect.collidepoint(pos)
                ):
                    self._current_scripts.append(script.play(character))

    def _play_scripts(self) -> None:
        """Advance all currently running scripts by one step."""

        def _do_next(gen: Generator) -> bool:
            try:
                next(gen)
                return True
            except StopIteration:
                return False

        self._current_scripts[:] = [
            gen for gen in self._current_scripts if _do_next(gen)
        ]


class Stage:
    """Main class for running the game stage and event loop."""

    def __init__(
        self, title: str, window: tuple[int, int], pages: list["Page"], grid_on: bool
    ) -> None:
        """
        Args:
            title (str): Window title.
            window (tuple[int, int]): Window size (width, height).
            pages (list[Page]): List of pages for the stage.
            grid_on (bool): Whether to draw the grid.
        """
        self._width, self._height = window
        self._grid_on = grid_on
        self._playing: bool = True
        self._frame_rate: int = settings.FRAME_RATE
        self._clock = pygame.time.Clock()

        pygame.init()
        pygame.display.set_caption(title)
        self._scene: pygame.Surface = pygame.display.set_mode(
            (self._width, self._height)
        )
        self._page_keeper = _PageKeeper(pages, self._width, self._height)
        self._control_board = _ControlBoard(self._width)
        self._scene_drawer = _SceneDrawer(
            self._scene, self._control_board, self._page_keeper, self._grid_on
        )
        self._event_handler = _EventHandler(self._control_board, self._page_keeper)

    def play(self) -> None:
        """Start the main event loop and play the stage."""
        self._page_keeper.store_states()

        while self._playing:
            self._scene_drawer.draw()
            self._event_handler.handle_taps(self._stop)

            pygame.display.flip()
            self._clock.tick(self._frame_rate)

        pygame.quit()

    def _stop(self):
        """Stop the main event loop."""
        self._playing = False
