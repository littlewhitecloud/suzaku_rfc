import glfw

from ._application import Application
from win32material import ApplyDarkMode
from .widgets import *
from .window import SWindow

app = Application()
window = SWindow()
window.set_application(app)

window.apply_theme("dark")


if window.theme.name == "dark":
    ApplyDarkMode(glfw.get_win32_window(window.window))


widget = SButton(parent=window, text="Hello, refactored suzaku!", size=(175, 35))
test = SBadge(parent=window, text="Suzaku Badge", x=100, y=175, size=(120, 35))
label = SLabel(parent=window, text="Suzaku Label", x=90, y=250)


app.mainloop()
