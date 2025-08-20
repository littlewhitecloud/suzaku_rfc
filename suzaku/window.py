import typing

import glfw
import OpenGL.GL as gl
import skia

from ._window import Window
from .event import SEvent
from .resource import STheme

# TODO: implment tab to make widget take focus

mods_dict: dict[int, str] = {
    glfw.MOD_CONTROL: "control",
    glfw.MOD_ALT: "alt",
    glfw.MOD_SHIFT: "shift",
    glfw.MOD_SUPER: "super",
    glfw.MOD_NUM_LOCK: "num_lock",
    glfw.MOD_CAPS_LOCK: "caps_lock",
}


class SWindow(Window):
    def __init__(
        self, app: typing.Any, title: str = "Suzaku Application", theme: str = "dark"
    ):
        super().__init__(app=app, title=title)

        self.theme: typing.Optional["STheme"] = None
        self.bg: skia.Color = skia.ColorTRANSPARENT

        self.apply_theme(theme)

        self.bind_event(self.id, "mouse_press", self._mouse)
        self.bind_event(self.id, "mouse_motion", self._mouse)
        # self.bind_event(self.id, "resize", self._on_framebuffer_size)
        self.bind_event(self.id, "update", self._on_framebuffer_size)

    def draw(self, surface: typing.Any) -> None:
        """SWindow default draw function"""
        surface.clear(self.bg)
        self._draw(surface)

    def _on_mouse_pos(self, window: any) -> None:
        """Set mouse pos"""
        pos = glfw.get_cursor_pos(window)
        self.mouse_x = pos[0]
        self.mouse_y = pos[1]
        self.mouse_rootx = pos[0] + self.x
        self.mouse_rooty = pos[1] + self.y

    def _on_framebuffer_size(self, *args, **kwargs) -> None:
        """Flush canvas"""
        glfw.make_context_current(self.window)
        with self.get_surface() as surface:
            with surface as canvas:
                # execute the draw function of the window
                self.draw(canvas)

            # update
            surface.flushAndSubmit()
            glfw.swap_buffers(self.window)

    update = _on_framebuffer_size

    def _on_resizing(self, window: any, width: int, height: int) -> None:
        """Generate reszie event

        :param window: glfw window
        :param width: the width of the window
        :param height: the height of the window
        """
        gl.glViewport(0, 0, width, height)
        self.width = width
        self.height = height
        # merge update with resize
        self.generate_event(
            "update", SEvent(event_type="update", width=width, height=height)
        )

    def _on_key(self, _: any, key: str, scancode: str, action: str, mods: str) -> None:
        """Generate key press event from glfw window

        :param _: glfw window
        :param key: key
        :param scancode: scan code
        :param action: action
        :param mods: mod key
        """
        keyname: str = glfw.get_key_name(key, scancode)

        try:
            if mods:
                mods = mods_dict[mods]
        except KeyError:
            mods = None
            print("TODO: fix mods")

        _ = SEvent(key=key, keyname=keyname, mods=mods)

        match action:
            case glfw.PRESS:
                _.event_type = "key_press"
            case glfw.RELEASE:
                _.event_type = "key_release"
            case glfw.REPEAT:
                _.event_type = "key_repeat"

        self.generate_event(_.event_type, _)

    def _on_mouse_button(
        self, window: any, button: any, is_pressed: bool, mod: any
    ) -> None:
        """Generate mouse pressed event or mouse released

        is_pressed:
            True -> window_mouse_press
            False -> window_mouse_release

        :param window: glfw window
        :param button: mouse button
        :param is_pressed: whether the button is pressed
        :param mod: mod
        """

        self._on_mouse_pos(window)

        event_type = f"mouse_{"press" if is_pressed else "release"}"
        self.generate_event(
            event_type,
            SEvent(
                event_type=event_type,
                x=self.mouse_x,
                y=self.mouse_y,
                rootx=self.mouse_rootx,
                rooty=self.mouse_rooty,
            ),
        )

    def _on_closed(self, _: any) -> None:
        """Generate closed event after the window is closed"""
        self.alive = False
        # self.generate_event("closed", SEvent(event_type="closed"))

    def _on_cursor_enter(self, window: any, is_entered: bool) -> None:
        """Generate mouse enter event or mose leave event

        is_entered:
            True -> window_mouse_enter
            False -> window_mouse_leave

        :param window: glfw window
        :param button: mouse button
        :param is_entered: whether entered the window
        """
        self._on_mouse_pos(window)

        self.generate_event(
            "mouse_motion",
            SEvent(
                event_type="mouse_motion",
                x=self.mouse_x,
                y=self.mouse_y,
                rootx=self.mouse_rootx,
                rooty=self.mouse_rooty,
            ),
        )

    def _on_cursor_pos(self, _: any, x: int, y: int) -> None:
        """Generate mouse motion event

        :param window: glfw window
        :param x: mouse x pos
        :param y: mouse y pos
        """
        self.mouse_x = self.mouse_rootx = x
        self.mouse_y = self.mouse_rooty = y
        self.generate_event(
            "mouse_motion",
            SEvent(
                event_type="mouse_motion",
                x=x,
                y=y,
                rootx=self.mouse_rootx,
                rooty=self.mouse_rooty,
            ),
        )

    def _on_window_pos(self, _: any, x: int, y: int) -> None:
        """Generate move event

        :param _: glfw window
        :param x: abs window x
        :param y: abs window y
        """
        self.x = x
        self.y = y
        self.generate_event("move", SEvent(event_type="move", x=self.x, y=self.y))

    def _on_focus(self, _: any, focused: bool) -> None:
        """Generate focus event

        :param _: glfw window
        :param focused: focused or not
        """
        self.focus = focused
        event_type = f"focus_{"in" if focused else "out"}"

        self.generate_event(event_type, SEvent(event_type=event_type))

    def _on_char(self, _: any, char: str) -> None:
        """Generate char event

        :param _: glfw window
        :param char: char
        """

        self.generate_event("char", SEvent(event_type="char", char=chr(char)))

    def _mouse(self, event: "SEvent") -> None:
        """Check if mouse is in any widget

        :param event: event, provide x, y pos
        """
        for widget in self.children:
            if not widget.takefocus:
                continue
            if (
                widget.x <= event.x <= widget.x + widget.width
                and widget.y <= event.y <= widget.y + widget.height
            ):
                widget.focus = True
                break
            widget.focus = False

    def apply_theme(
        self,
        theme_name: typing.Optional[str] = None,
        file_path: typing.Optional[str] = None,
        internal: bool = True,
    ) -> None:
        """Apply theme for SWindow

        :param theme_name:
            when use with filepath, specifies a loaded theme name
            when use with internal, provides a internal theme name
        :param file_path: theme file path
        :param internal: whether to use internal theme
        """
        if not internal:
            return STheme(theme_name).read_theme_from_json(file_path).parse_style()

        from .resource import dark_theme, light_theme

        self.theme = vars()[f"{theme_name}_theme"]
        self.bg = self.theme.get_style_attr("SWindow:bg")

        self.generate_event("theme_update", SEvent(event_type="theme_update"))

        del dark_theme, light_theme

    def create_binds(self) -> None:
        """Create binds from glfw"""

        glfw.make_context_current(self.window)
        glfw.window_hint(glfw.SAMPLES, 1)
        # gl.glEnable(gl.GL_MULTISAMPLE)
        glfw.swap_interval(1)
        glfw.set_window_size_callback(self.window, self._on_resizing)
        glfw.set_framebuffer_size_callback(self.window, self._on_framebuffer_size)
        glfw.set_window_close_callback(self.window, self._on_closed)
        glfw.set_mouse_button_callback(self.window, self._on_mouse_button)
        glfw.set_cursor_enter_callback(self.window, self._on_cursor_enter)
        glfw.set_cursor_pos_callback(self.window, self._on_cursor_pos)
        glfw.set_window_pos_callback(self.window, self._on_window_pos)
        glfw.set_window_focus_callback(self.window, self._on_focus)
        glfw.set_key_callback(self.window, self._on_key)
        glfw.set_char_callback(self.window, self._on_char)
