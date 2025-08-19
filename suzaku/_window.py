import contextlib
import typing
import gc

import glfw
import OpenGL.GL as gl
import skia

from .after import SAfter
from .event import SEventHandler


class Window(SEventHandler, SAfter):

    _instances = 0

    def __init__(self, name: str = "Window", title: str = "hello", _id=None) -> None:
        """
        Initialize the window
        :param title: the title of the window
        """
        SEventHandler.__init__(self)
        SAfter.__init__(self)

        # region info
        self.name = name
        self.window: typing.Any = None
        self.alive: bool = False
        self.application: typing.Any = None
        # end region

        # region winfo

        # basic winfo
        self.title: str = title
        self.width, self.height = 1175, 675
        # identifier
        self.id: str = _id if _id else self.name + "." + str(Window._instances)
        # window & mouse pos
        self.x = self.y = 0
        self.root_x = self.root_y = 0
        self.mouse_x = self.mouse_y = 0
        self.mouse_rootx = self.mouse_rooty = 0

        self.cursor: str = "arrow"
        self.focus: bool = True
        Window._instances += 1

        self._context = "None"
        self._backend_render_target = None
        self._make_srgb = skia.ColorSpace.MakeSRGB()
        # end region

        self.children: typing.List["SWidget"] = []

        self.create_window()

    def _draw(self, surface: typing.Any) -> None:
        """Draw both window and the children widgets"""
        # draw the window's children widgets
        for child in self.children:
            child.draw(surface)

    def create_window(self) -> None:
        """Create the glfw window"""
        self.window = glfw.create_window(
            self.width, self.height, self.title, None, None
        )

        (self.root_x, self.root_y) = glfw.get_window_pos(self.window)

        if not self.window and not glfw.window_should_close(self.window):
            raise RuntimeError("Failed to create a glfw window instance")

        self.alive = True

    def set_application(self, app: typing.Any = None) -> None:
        """
        Attache the window to the application
        :param app: the application
        """
        # this window is attached to the given application
        self.application = app
        # append the window itself to the application draw list
        self.application.windows.append(self)

    def add_children(self, widget: "SWidget") -> None:
        """Add children to the window
        :param widget: the widget to be added to the draw list
        """
        self.children.append(widget)

        # Tips: widget init here
        widget._on_theme_update()
        widget.bind_event(widget.id, "theme_update", widget._on_theme_update)

    def get_context(self) -> None:
        # make context
        self._context = skia.GrDirectContext.MakeGL()
        self._context.setResourceCacheLimit(16 * 1024 * 1024)

    @contextlib.contextmanager
    def get_surface(self) -> typing.Any:
        """Get/Create the skia surface"""
        # check if the window is vaild now
        if not glfw.get_current_context() or glfw.window_should_close(self.window):
            yield None
            return

        try:
            # make backend
            (FB_WIDTH, FB_HEIGHT) = glfw.get_framebuffer_size(self.window)
            if (not (self._backend_render_target and self.width == FB_WIDTH and self.height == FB_HEIGHT)):
                self.width = FB_WIDTH
                self.height = FB_HEIGHT
                self._backend_render_target = skia.GrBackendRenderTarget(
                    FB_WIDTH, FB_HEIGHT, 0, 0, skia.GrGLFramebufferInfo(0, gl.GL_RGBA8)
                )
            # make surface
            surface = skia.Surface.MakeFromBackendRenderTarget(
                self._context,
                self._backend_render_target,
                skia.kBottomLeft_GrSurfaceOrigin,
                skia.kRGBA_8888_ColorType,
                self._make_srgb,
            )
            # assert surface
            if surface is None:
                raise RuntimeError("Failed to create a skia surface")
            yield surface
        finally:
            if "_context" in locals():
                _context.freeGpuResources()
                _context.releaseResourcesAndAbandonContext()

            del FB_HEIGHT, FB_WIDTH

    def destroy_window(self) -> None:
        """Destory the window"""
        # destory window
        self.alive = False

        if glfw.get_current_context() is None:
            glfw.make_context_current(self.window)

        if self._context:
            self._context.freeGpuResources()
            self._context.releaseResourcesAndAbandonContext()
            self._context = None

        if self.window:
            glfw.destroy_window(self.window)
            self.window = None

    destroy = destroy_window
