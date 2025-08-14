import glfw
import OpenGL.GL as gl

from ._window import Window
from .event import SEvent, SEventHandler

"""
SWindow -> glfw -> generate_event 
产生对应事件
Widget -> generate_event -> register
注册对应组件的trigger
generate_event -> triggered -> call back registed function
"""

mods_dict = {
    glfw.MOD_CONTROL: "control",
    glfw.MOD_ALT: "alt",
    glfw.MOD_SHIFT: "shift",
    glfw.MOD_SUPER: "super",
    glfw.MOD_NUM_LOCK: "num_lock",
    glfw.MOD_CAPS_LOCK: "caps_lock",
}


class SWindow(Window):
    def __init__(self, title: str = "Suzaku Application"):
        super().__init__(title=title)

        self.create_binds()

        self.bind_event(self.id, "mouse_press", self._mouse)
        self.bind_event(self.id, "mouse_motion", self._mouse)

    def _on_mouse_pos(self, window: any) -> None:
        """Set mouse pos"""
        pos = glfw.get_cursor_pos(window)
        self.mouse_x = pos[0]
        self.mouse_y = pos[1]
        self.mouse_rootx = pos[0] + self.x
        self.mouse_rooty = pos[1] + self.y

    def _on_framebuffer_size(self, _: any, width: int, height: int) -> None:
        """Flush canvas"""
        glfw.make_context_current(_)
        with self.create_surface(_) as surface:
            with surface as canvas:
                # do the draw function of the window
                self.draw(canvas)

            # update
            surface.flushAndSubmit()
            glfw.swap_buffers(_)

    def _on_resizing(self, window: any, width: int, height: int) -> None:
        """Generate reszie event

        :param window: glfw window
        :param width: the width of the window
        :param height: the height of the window
        """
        gl.glViewport(0, 0, width, height)
        self._on_framebuffer_size(window, width, height)
        self.width = width
        self.height = height
        self.generate_event(
            "resize", SEvent(event_type="resize", width=width, height=height)
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
        except:
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
                event_type,
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
        if focused:
            self.focus = True
            self.generate_event("focus_in", SEvent(event_type="focus_in"))
        else:
            self.focus = False
            self.generate_event("focus_out", SEvent(event_type="focus_out"))

    def _on_char(self, _: any, char: str) -> None:
        """Generate char event

        :param _: glfw window
        :param char: char
        """

        self.generate_event("char", SEvent(event_type="char", char=chr(char)))

    def _mouse(self, event: "SEvent") -> None:
        for widget in self.children:
            if (
                widget.x <= event.x <= widget.x + widget.width
                and widget.y <= event.y <= widget.y + widget.height
            ):
                widget.focus = True
                break
            widget.focus = False

    def create_binds(self) -> None:
        """Create binds from glfw"""
        glfw.make_context_current(self.window)
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
