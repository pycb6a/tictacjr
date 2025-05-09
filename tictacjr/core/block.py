from typing import Self

from tictacjr.core.script import _BlockCmd, ScriptDoer


class _BlockBase:
    """Base class for all block types."""

    def _add(self, block: str, *args) -> Self:
        """Add a new block to the script.

        Args:
            block (str): Block type/name.
            *args: Arguments specific to the block.

        Returns:
            Self: Returns self for chaining.
        """
        raise NotImplementedError


class _ControlBlock(_BlockBase):
    """Adds control-related block commands."""

    def wait(self, times: int = 1) -> Self:
        """Add a wait block.

        Args:
            times (int, optional): How long to wait. Defaults to 1.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("wait", times)
        return self


class _LooksBlock(_BlockBase):
    """Adds looks-related block commands."""

    def say(self, text: str = "Hi!") -> Self:
        """Add a say block.

        Args:
            text (str, optional): Text to say. Defaults to "Hi!".

        Returns:
            Self: Returns self for chaining.
        """
        self._add("say", text)
        return self

    def grow(self, steps: int = 1) -> Self:
        """Add a grow block.

        Args:
            steps (int, optional): Steps to grow. Defaults to 1.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("grow", steps)
        return self

    def shrink(self, steps: int = 1) -> Self:
        """Add a shrink block.

        Args:
            steps (int, optional): Steps to shrink. Defaults to 1.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("shrink", steps)
        return self

    def reset_size(self) -> Self:
        """Add a reset size block.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("reset_size")
        return self

    def hide(self) -> Self:
        """Add a hide block.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("hide")
        return self

    def show(self) -> Self:
        """Add a show block.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("show")
        return self


class _MotionBlock(_BlockBase):
    """Adds motion-related block commands."""

    def move_right(self, steps: int = 1) -> Self:
        """Add a move right block.

        Args:
            steps (int, optional): Steps to move. Defaults to 1.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("move_right", steps)
        return self

    def move_left(self, steps: int = 1) -> Self:
        """Add a move left block.

        Args:
            steps (int, optional): Steps to move. Defaults to 1.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("move_left", steps)
        return self

    def move_up(self, steps: int = 1) -> Self:
        """Add a move up block.

        Args:
            steps (int, optional): Steps to move. Defaults to 1.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("move_up", steps)
        return self

    def move_down(self, steps: int = 1) -> Self:
        """Add a move down block.

        Args:
            steps (int, optional): Steps to move. Defaults to 1.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("move_down", steps)
        return self

    def hop(self, height: int = 2) -> Self:
        """Add a hop block.

        Args:
            height (int, optional): Height to hop. Defaults to 2.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("hop", height)
        return self

    def go_home(self) -> Self:
        """Add a go home block.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("go_home")
        return self

    def turn_right(self, steps: int = 1) -> Self:
        """Add a turn right block.

        Args:
            steps (int, optional): Steps to turn. Defaults to 1.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("turn_right", steps)
        return self

    def turn_left(self, steps: int = 1) -> Self:
        """Add a turn left block.

        Args:
            steps (int, optional): Steps to turn. Defaults to 1.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("turn_left", steps)
        return self


class Block(_ControlBlock, _LooksBlock, _MotionBlock):
    """Main block class for combining control, looks, and motion blocks.

    Args:
        script (ScriptDoer): The script object this block is associated with.
    """

    def __init__(self, script: ScriptDoer) -> None:
        self._script: ScriptDoer = script
        self._repeats: list[list[_BlockCmd]] = []

    def do_block(self, block: Self) -> Self:
        """Add a nested block to be executed.

        Args:
            block (Self): The block to execute.

        Returns:
            Self: Returns self for chaining.
        """
        self._add("do_block", block._script)
        return self

    def start_repeat(self) -> Self:
        """Begin a repeat block (to be closed later).

        Returns:
            Self: Returns self for chaining.
        """
        self._repeats.append([])
        return self

    def repeat(self, times: int) -> Self:
        """Repeat a set of blocks a given number of times.

        Args:
            times (int): Number of repetitions.

        Returns:
            Self: Returns self for chaining.
        """
        if self._repeats:
            cmd = self._repeats.pop()
            self._add("repeat", times, cmd)
        return self

    def repeat_forever(self) -> Self:
        """Repeat a set of blocks forever.

        Returns:
            Self: Returns self for chaining.
        """
        if self._repeats:
            cmd = self._repeats.pop()
            self._add("repeat_forever", cmd)
        return self

    def _add(self, block: str, *args) -> Self:
        """Add a block command, handling nested repeats.

        Args:
            block (str): Block type/name.
            *args: Arguments for the block.

        Returns:
            Self: Returns self for chaining.
        """
        cmd = _BlockCmd(block, *args)
        if self._repeats:
            self._repeats[-1].append(cmd)
        else:
            self._script.blocks.append(cmd)
        return self
