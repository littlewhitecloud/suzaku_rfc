import asyncio
import threading
import typing


class SAfterV1:
    def __init__(self) -> None: ...

    def after(self, ms: int, callback: typing.Callable) -> None:
        """Call a function after {time}ms

        :param time: control the time to call callback
        :param callback: the callback function
        """
        threading.Timer(ms / 1000, callback).start()


class SAfterV2:

    _loop = None  # work thread
    _lock = threading.Lock()  # work thread lock

    def __init__(self) -> None: ...

    def ensure_loop(self) -> None:
        """Make sure the loop is maked"""
        # check twice for the first time init
        if self._loop is None:
            with self._lock:  # get lock
                if self._loop is None:
                    self._loop = (
                        asyncio.new_event_loop()
                    )  # make a new loop from asyncio
                    threading.Thread(
                        target=self._loop.run_forever, daemon=True
                    ).start()  # start loop

    def after(self, ms: int, callback: typing.Callable, *args) -> asyncio.TimerHandle:
        """After a few ms to callback the function

        :param ms: time, milliseconds
        :param callback: function to callback
        """
        self.ensure_loop()
        return self._loop.call_later(ms / 1000.0, callback, *args)

    def cancel(self, handle: asyncio.TimerHandle):
        handle.cancel()


SAfter = SAfterV2
