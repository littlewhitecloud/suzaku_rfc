### Suzaku (Refactor)

original repo link: `https://github.com/XiangQinxi/suzaku`

### Gallery
<img width="202" height="332" alt="image" src="https://github.com/user-attachments/assets/871b0792-686d-41e4-af68-177a752a7667" />
<img width="202" height="332" alt="image" src="https://github.com/user-attachments/assets/e3453657-9159-452e-b800-348fa4e50f35" />


### Develop
```console
git clone https://github.com/littlewhitecloud/suzaku_rfc.git
cd suzaku_rfc
pip install -r requirements.txt
python -m suzaku
```

### How does suzaku work?
First, we have these libraries for backend:
> glfw (OpenGl/Vulkan context and the window)
> skia (Functions that draw rect and more)
> OpenGL (Basic support)

We make an glfw window and store it in a class named `Window` and base on it to make our own specific class named `SWindow`
Moreover, we would also make a class named `Applicaton` for message loop and window update
Last, we can register our own widgets which draws by skia and let the window call the defined draw function for update

By following these steps, you can get a minimal suzaku example:
```python
from suzaku import SWindow, Application

app = Application()
window = SWindow(app=app, title="Minimal suzaku example")

app.mainloop()
```


