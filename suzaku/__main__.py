
# import glfw
# from win32material import ApplyDarkMode

from ._application import Application
from .widgets import SBadge#, SButton, SLabel, SImage
from .window import SWindow

app = Application()
window = SWindow()
window.set_application(app)
window.apply_theme("dark")

# if window.theme.name == "dark":
#     ApplyDarkMode(glfw.get_win32_window(window.window))
# import tracemalloc

# tracemalloc.start()


def setsize(event):
    image.width = event.width
    image.height = event.height


#image = SImage(parent=window, image="background.png", size=(1175, 675))
#button = SButton(parent=window, text="Hello, refactored suzaku!", size=(175, 35))
badge = SBadge(parent=window, text="Suzaku Badge", size=(120, 35))
#label = SLabel(parent=window, text="Suzaku Label")

#button.place(100, 100)
badge.place(100, 200)
#image.place(0, 0)
#label.place(100, 300)


# print(threading.active_count())
# window.after(1000, window.apply_theme, "light")

# print(threading.active_count())
# window.after(2000, lambda: print("after callback 1"))
# print(threading.active_count())
# window.after(3000, lambda: print("after callback 2"))

#image.bind_event(image.id, "resize", setsize)

app.mainloop()

# snapshot = tracemalloc.take_snapshot()
# top_stats = snapshot.statistics('lineno')


# print("[ Top 10 memory allocations ]")
# for stat in top_stats[:10]:
#     print(stat)