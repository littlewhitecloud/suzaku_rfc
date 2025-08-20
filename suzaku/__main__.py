from ._application import Application
from .widgets import SBadge, SButton, SImage, SLabel, SText  # noqa: F401
from .window import SWindow

app = Application()
window = SWindow(
    app=app, title="Suzaku refacter demonstrate", theme="light", size=(200, 300)
)

# from win32material import ApplyDarkMode
# if window.theme.name == "dark":
#    ApplyDarkMode(glfw.get_win32_window(window.window))

# def setsize(event):
#     global image
#     image.width = event.width
#     image.height = event.height

light_toggle = SButton(
    parent=window,
    text="Toggle light theme",
    size=(175, 35),
    command=lambda: window.apply_theme("light"),
).place(12.5, 35 + 12.5)

dark_toggle = SButton(
    parent=window,
    text="Toggle dark theme",
    size=(175, 35),
    command=lambda: window.apply_theme("dark"),
).place(13.5, 35 + 35 + 35)

label_example = SLabel(parent=window, text="Hi! This is suzaku label!").place(
    13.5 + 90, 35 * 5
)

exit_button = SButton(
    parent=window,
    text="Exit demonstrate",
    size=(175, 35),
    command=lambda: app.destroy_application(),
).place(12.5, 300 - 15)

# image = SImage(parent=window, image="background.png", size=(1175, 675)).place(0, 0)
# badge = SBadge(parent=window, text="Suzaku Badge", size=(120, 35)).place(100, 200)
# text = SText(parent=window, size=(300, 200)).place(100, 300)

# window.after(1000, window.apply_theme, "light")

# image.bind_event(image.id, "resize", setsize)
app.mainloop()
