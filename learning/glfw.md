## **GLFW是“窗口+输入+上下文”的工具库**

### 用途
- 创建和管理 **窗口**（包括全屏/窗口化）
- 初始化和管理 **OpenGL、OpenGL ES 或 Vulkan 上下文**
- 处理 **键盘、鼠标、手柄等输入事件**
- 提供 **高精度计时器、垂直同步（V-Sync）** 等底层支持功能

### 作用
| 功能类别     | 具体能力                                                                 |
|--------------|--------------------------------------------------------------------------|
| 窗口管理     | 创建窗口、设置标题、大小、全屏、窗口置顶、隐藏窗口装饰等 |
| 上下文管理   | 创建 OpenGL/Vulkan 上下文、设置版本、切换上下文                          |
| 输入处理     | 键盘、鼠标、手柄、滚轮、光标、剪贴板事件监听                |
| 事件循环     | 提供跨平台的消息循环机制，支持回调函数处理事件                           |
| 性能支持     | 支持垂直同步、双缓冲、帧率控制、高精度计时器                      |

| 特性         | GLFW                     | SDL                      | GLUT             |
|--------------|---------------------------|---------------------------|------------------|
| 主要用途     | 图形窗口 + OpenGL 上下文 | 多媒体（图形+音频+输入） | OpenGL 教学演示 |
| 是否支持音频 | ❌                        | ✅                        | ❌               |
| 是否支持游戏开发 | ✅（图形部分）         | ✅（全套）                | ❌               |
| 跨平台支持   | ✅（Win/macOS/Linux）     | ✅                        | ✅               |
| 控件/小部件  | ❌（不提供）              | ❌                        | ❌               |


```c
if (!glfwInit()) return -1;

GLFWwindow* window = glfwCreateWindow(800, 600, "Hello GLFW", NULL, NULL);
if (!window) {
    glfwTerminate();
    return -1;
}

glfwMakeContextCurrent(window);

while (!glfwWindowShouldClose(window)) {
    glClear(GL_COLOR_BUFFER_BIT);
    // 渲染代码
    glfwSwapBuffers(window);
    glfwPollEvents();
}

glfwTerminate();
```