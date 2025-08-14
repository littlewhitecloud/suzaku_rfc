import glfw

from ._window import Window
from .event import SEventHandler


class Application:
    def __init__(self) -> None:
        self.windows: list("Window") = []
        self.alive = False
        self.init()

    def mainloop(self) -> None:
        """The mainloop"""
        self.alive = True

        # Mainloop
        while self.alive and self.windows:
            glfw.poll_events()

            # _w: Window class _w.window: glfw window
            for _w in self.windows:
                window = _w.window

                # check if the window is still alive
                if not _w.alive or glfw.window_should_close(window):
                    _w.destroy()
                    self.windows.remove(_w)
                    continue

                if not glfw.get_window_attrib(window, glfw.FOCUSED):
                    continue

                _w._on_framebuffer_size(window, _w.height, _w.width)

                # press esc to close
                if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
                    glfw.set_window_should_close(window, True)

        self.destroy_application()

    def init(self) -> None:
        """Initilzation the glfw"""
        glfw.init()

    def destroy_application(self) -> None:
        """Destroy the application"""
        self.alive = False
        for _ in self.windows:
            _.window.destroy()
        glfw.terminate()

    destroy = destroy_application
