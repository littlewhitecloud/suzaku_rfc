import contextlib
import typing

import glfw
import OpenGL.GL as gl
import skia

from .event import SEventHandler


class Window(SEventHandler):

    _instances = 0

    def __init__(self, name: str = "Window", title: str = "hello", _id=None) -> None:
        """
        Initialize the window
        :param title: the title of the window
        """
        super().__init__()

        # region info
        self.name = name
        self.window: typing.Any = None
        self.alive: bool = False
        self.application: typing.Any = None
        # end region

        # region winfo

        # basic winfo
        self.title: str = title
        self.height, self.width = 1175, 675
        # identifier
        self.id = _id if _id else self.name + "." + str(Window._instances)
        # window & mouse pos
        self.x = self.y = 0
        self.mouse_x = self.mouse_y = 0
        self.mouse_rootx = self.mouse_rooty = 0

        self.cursor = "arrow"
        self.focus = True
        Window._instances += 1
        # end region

        self.children = []

        self.create_window()

    def draw(self, surface: typing.Any) -> None:
        """Draw both window and the children widgets"""
        surface.clear(skia.ColorTRANSPARENT)
        # draw the window's children widgets
        for child in self.children:
            child.draw(surface)

    def create_window(self) -> None:
        """Create the glfw window"""
        self.window = glfw.create_window(
            self.height, self.width, self.title, None, None
        )

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

    @contextlib.contextmanager
    def create_surface(self, window: typing.Optional[typing.Any] = None) -> typing.Any:
        """Create the skia surface"""
        # check if the window is vaild now
        window = window if window else self.window
        if not glfw.get_current_context() or glfw.window_should_close(window):
            yield None
            return

        try:
            # TODO: test vulkannnnnnn?
            # make context
            context = skia.GrDirectContext.MakeGL()
            (FB_WIDTH, FB_HEIGHT) = glfw.get_framebuffer_size(window)
            # make backend
            backend_render_target = skia.GrBackendRenderTarget(
                FB_WIDTH, FB_HEIGHT, 0, 0, skia.GrGLFramebufferInfo(0, gl.GL_RGBA8)
            )
            # make surface
            surface = skia.Surface.MakeFromBackendRenderTarget(
                context,
                backend_render_target,
                skia.kBottomLeft_GrSurfaceOrigin,
                skia.kRGBA_8888_ColorType,
                skia.ColorSpace.MakeSRGB(),
            )
            # assert surface
            if surface is None:
                raise RuntimeError("Failed to create a skia surface")
            yield surface
        finally:
            # release context
            if "context" in locals():
                context.releaseResourcesAndAbandonContext()

    def destroy_window(self) -> None:
        """Destory the window"""
        # destory window
        glfw.destroy_window(self.window)
        self.alive = False

    destroy = destroy_window


# def test():
#     glfw.init()
#     a = Window()

#     # from win32material import ApplyMica

#     def draw(canvas):
#         # 这里定义你的绘图逻辑
#         canvas.clear(skia.ColorTRANSPARENT)
#         canvas.drawCircle(100, 100, 40, skia.Paint(Color=skia.ColorGREEN))

#     glfw.make_context_current(a.window)
#     with a.create_surface() as surface:
#         with surface as canvas:
#             draw(canvas)

#             surface.flushAndSubmit()
#             glfw.swap_buffers(a.window)
#     # ApplyMica(glfw.get_win32_window(a.window), True, True)

#     while not glfw.window_should_close(a.window):
#         glfw.wait_events()


# test()
