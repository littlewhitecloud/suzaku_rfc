# import glfw
# from win32material import ApplyDarkMode

from ._application import Application
from .widgets import SBadge, SButton, SImage, SLabel, SText  # noqa: F401
from .window import SWindow

app = Application()
window = SWindow(app=app, title="test", theme="dark")

# if window.theme.name == "dark":
#    ApplyDarkMode(glfw.get_win32_window(window.window))


def setsize(event):
    global image
    image.width = event.width
    image.height = event.height


button = SButton(parent=window, text="Hello, refactored suzaku!", size=(175, 35)).place(
    100, 100
)
# image = SImage(parent=window, image="background.png", size=(1175, 675)).place(0, 0)
# badge = SBadge(parent=window, text="Suzaku Badge", size=(120, 35)).place(100, 200)
# text = SText(parent=window, size=(300, 200)).place(100, 300)
# label = SLabel(parent=window, text="Suzaku Label").place(100, 300)


# print(threading.active_count())
window.after(1000, window.apply_theme, "light")

# window.after(2000, lambda: print("after callback 1"))
# window.after(3000, lambda: print("after callback 2"))

# image.bind_event(image.id, "resize", setsize)

app.mainloop()

# snapshot = tracemalloc.take_snapshot()
# top_stats = snapshot.statistics('lineno')


# print("[ Top 10 memory allocations ]")
# for stat in top_stats[:10]:
#     print(stat)
