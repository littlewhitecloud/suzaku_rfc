import asyncio
import threading
import typing


class SAfterV1:
    def __init__(self) -> None: ...

    def after_thread(self, ms: int, callback: typing.Callable) -> None:
        """Call a function after {time}ms

        :param time: control the time to call callback
        :param callback: the callback function
        """
        _ = threading.Timer(ms / 1000, callback)
        _.start()


class SAfterV2:
    def __init__(self) -> None:
        self._loop = None
        self._lock = threading.Lock()

    def ensure_loop(self) -> None:
        """Make sure the loop is maked"""
        if self._loop is None:
            with self._lock:
                if self._loop is None:
                    self._loop = asyncio.new_event_loop()
                    threading.Thread(target=self._loop.run_forever, daemon=True).start()

    def after(self, ms: int, callback: typing.Callable, *args) -> None:
        """After a few ms to callback the function

        :param ms: time, milliseconds
        :param callback: function to callback
        """
        self.ensure_loop()
        self._loop.call_later(ms / 1000.0, callback, *args)


SAfter = SAfterV2
