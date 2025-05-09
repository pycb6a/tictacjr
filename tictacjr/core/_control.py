from collections.abc import Generator

from tictacjr.core import settings


class _ControlAction:
    """Implements character control actions."""

    @staticmethod
    def wait(times: int) -> Generator:
        """Wait for a specified number of 'times' in-game units.

        Args:
            times (int): Duration to wait, in game units (multiplied by frame rate).

        Yields:
            None: Yields once per frame for the calculated number of ticks.
        """
        ticks = times * settings.FRAME_RATE
        for _ in range(ticks):
            yield
