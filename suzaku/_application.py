import typing

import glfw

from ._window import Window
from .event import SEventHandler


class Application:
    def __init__(self) -> None:
        self.windows: typing.List("Window") = []
        self.alive = False
        self.init()

    def mainloop(self) -> None:
        """The mainloop"""
        self.alive = True

        for _ in self.windows:
            _.create_binds()

        # Mainloop
        while self.alive and self.windows:
            glfw.poll_events()

            # _w: Window class _w.window: glfw window
            for _w in self.windows:
                # check if the window is still alive
                if not _w.alive or glfw.window_should_close(_w.window):
                    _w.destroy()
                    self.windows.remove(_w)
                    continue

                if not glfw.get_window_attrib(_w.window, glfw.FOCUSED):
                    continue

                _w._on_framebuffer_size(_w.window, _w.height, _w.width)

        self.destroy_application()

    def init(self) -> None:
        """Initilzation the glfw"""
        glfw.init()

    def destroy_application(self) -> None:
        """Destroy the application"""
        self.alive = False
        for _ in self.windows:
            _.destroy_window()
        glfw.terminate()

    destroy = destroy_application
