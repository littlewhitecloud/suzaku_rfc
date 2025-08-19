import typing
import gc
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
        self.handle = glfw.poll_events

        # Init windows
        for _ in self.windows:

            _.create_binds() # create glfw window binds
            _.get_context() # set context
            _._on_framebuffer_size() # make sure every window is drawed


        # Mainloop
        # Only message loop, no window update
        while self.alive and self.windows:
            self.handle()

            # _w: Window class _w.window: glfw window
            for _w in self.windows:
                # check if the window is still alive
                if not _w.alive or glfw.window_should_close(_w.window):
                    _w.destroy_window()
                    self.windows.remove(_w)
                    continue

                # auto wait if not focused
                if not glfw.get_window_attrib(_w.window, glfw.FOCUSED):
                    self.handle = glfw.wait_events
                    continue
                else:
                    self.handle = glfw.poll_events

                # decrease CPU usage
                glfw.wait_events_timeout(0.01)
                gc.collect()

        self.destroy_application()

    def init(self) -> None:
        """Initilzation the glfw"""
        glfw.init()

    def destroy_application(self) -> None:
        """Destroy the application"""
        self.alive = False
        glfw.terminate()

    destroy = destroy_application
