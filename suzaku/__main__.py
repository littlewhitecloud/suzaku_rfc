import glfw
from win32material import ApplyDarkMode

from ._application import Application
from .widgets import SBadge, SButton, SLabel
from .window import SWindow

app = Application()
window = SWindow()
window.set_application(app)

window.apply_theme("dark")


if window.theme.name == "dark":
    ApplyDarkMode(glfw.get_win32_window(window.window))


button = SButton(parent=window, text="Hello, refactored suzaku!", size=(175, 35))
badge = SBadge(parent=window, text="Suzaku Badge", x=100, y=175, size=(120, 35))
label = SLabel(parent=window, text="Suzaku Label", x=90, y=250)

window.after(1000, window.apply_theme, "light")

app.mainloop()
