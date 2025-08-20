import gc
import typing

import glfw


class Application:
    def __init__(self) -> None:
        self.windows: typing.List("Window") = []
        self.alive = False
        self.init()

    def add_window(self, _: "Window" = None) -> None:
        """
        Attache the window to the application
        :param _: the SWindow class
        """
        # append the window itself to the application draw list
        self.windows.append(_)
        _.create_binds()  # create glfw window binds
        _.get_context()  # set context
        _._on_framebuffer_size()  # make sure every window is drawed

    def mainloop(self) -> None:
        """The mainloop"""
        # Set the alive flag to true
        self.alive = True

        # Mainloop
        # Only message loop, no window update
        while self.alive and self.windows:
            glfw.wait_events()

            # _w: Window class _w.window: glfw window
            for _w in self.windows:
                # check if the window is still alive
                if not _w.alive or glfw.window_should_close(_w.window):
                    _w.destroy_window()

                    self.windows.remove(_w)
                    continue

                # auto wait if not focused
                if not glfw.get_window_attrib(_w.window, glfw.FOCUSED):
                    continue

                _w.update()

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

        if self.windows:
            for _ in self.windows:
                _.destroy_window()

        glfw.terminate()

    destroy = destroy_application
