---
layout: post
title: "“特效编程”笔记 -- 计算机图形学 OPENGL 入门"
author:
location: "珠海"
categories: ["特效"]
tags: ["特效", "OpenGL"]
toc: true
toclistyle:
comments:
visibility:
mathjax: true
mermaid:
glslcanvas:
---

以前随便找点代码，改吧改吧就能跑，今天算是入门学习了一下。
顶点着色器、几何着色器、片段着色器。又酷又通透，身心愉悦 ——

本文源码 <a href="{% include gitsrc.html url="/source/shader/LearnOpenGL-Introduction" %}" target="_blank">LearnOpenGL-Introduction</a>

* 相关代码

    * 课程完整源码：<https://github.com/hawkhai/LearnOpenGL.git>
    * 用到第三方库：<https://gitee.com/hawkhai/opengl-3rd.git>


## uni-marburg.de 课程

<https://www.uni-marburg.de/en/fb12/research-groups/grafikmultimedia/lectures/graphics>

<https://www.mathematik.uni-marburg.de/~thormae/lectures/graphics1/graphics_9_1_eng_web.html>

[OpenGL Step by Step - OpenGL Development](http://ogldev.atspace.co.uk/index.html)


## 历史

1988 年 5 月，Pixar 公布了第三版 RenderMan 规范，将「着色器」的使用推广到了我们目前所知的各大应用领域。

随着图形处理器的进步，OpenGL 和 Direct3D 等主要的图形软件库都开始支持着色器。
第一批支持着色器的 GPU 仅支持像素着色器，但随着开发者逐渐认识到着色器的强大，很快便出现了顶点着色器。
2000 年，第一款支持可编程像素着色器的显卡 Nvidia GeForce 3（NV20）问世。Direct3D 10 和 OpenGL 3.2 则引入了几何着色器。

{% include image.html url="/images/OpenGL-GLSL/faa27c0e4a3a4b7eb3436c016ce606f1.jpeg"
caption= "利用 gpu 渲染一个巨人的图像" %}

[计算机图形学 OPENGL 入门 {% include relref_bili.html %}](https://www.bilibili.com/video/BV1px41197A5)

<https://ke.qq.com/course/package/25480?flowToken=1019441>

<https://learnopengl-cn.github.io/>


## Others

- 包含部分第三方库：<https://github.com/Groovounet/ogl-samples>

- 几个完整得范例：<https://github.com/hawkhai/openglcpp.git>

    * computeShaderParticleSystem.vcxproj / computeShader.sln
        * OpenGL Compute Shader Particle System
        * \#define GL_COMPUTE_SHADER 0x91B9
        * \#define GL_VERTEX_SHADER 0x8B31
        * \#define GL_FRAGMENT_SHADER 0x8B30
        * This compute shader implements a very basic attraction based particle system that changes velocities to move the particles towards the target position.
        * 40 帧，2048 个粒子，CPU & GPU 都能大概控制在 5%。
        * 平常我们使用的 Shader 有顶点着色器、几何着色器、片段着色器，这几个都是为光栅化图形渲染服务的，**OpenGL 4.3（发布日期：2012 年 8 月 6 日）**之后新出了一个 Compute Shader，用于通用计算并行加速。[link](https://www.cnblogs.com/chen9510/p/12000320.html)
        * OpenGL ES 3.1 使用计算着色器（Compute Shader）[link](https://blog.csdn.net/qq_39561000/article/details/103112147)

    * ?eglExample.vcxproj / eglExample.sln
        * [Using OpenGL ES on windows desktops via EGL](https://www.saschawillems.de/blog/2015/04/19/using-opengl-es-on-windows-desktops-via-egl/)
        * [SimpleGL Example](https://wiki.maemo.org/SimpleGL_example)
        * [OpenGL ES EGL 简介 -- 完整的一个文档用例](https://blog.csdn.net/iEearth/article/details/71180457)
        * [EGL 1.5 implementation for Windows and X11 supporting OpenGL.](https://github.com/McNopper/EGL)

    * geometryShaderSimple.vcxproj / geometryShader.sln
        * This geometry shader takes a single GL_POINT as input and generates triangles for a complete circle.

    * ?instancing.vcxproj

    * ?raypicking.vcxproj / raypicking.sln

    * ?SPIRVShader.vcxproj / SPIRVShader.sln

    * triangle.vcxproj / triangle.sln
        * OpenGL example - Indexed triangle rendering
        * <https://learnopengl-cn.github.io/04%20Advanced%20OpenGL/08%20Advanced%20GLSL/#uniform>
        * [Unform Buffer Objecct(UBO)](https://www.cnblogs.com/chen9510/p/11447292.html)
        * [Uniform Buffer Object](https://www.khronos.org/opengl/wiki/Uniform_Buffer_Object)
        * error LNK2019: 无法解析的外部符号 _stbi_load -> 需要在 #include <stb_image.h> 前增加一句 #define STB_IMAGE_IMPLEMENTATION。

{% include image.html url="/images/OpenGL-GLSL/ComputeShaderParticleSystem.gif" %}
{% include image.html url="/images/OpenGL-GLSL/20201203151447.png" %}

- __imp__vsnprintf

错误 LNK2019 无法解析的外部符号 \_\_imp\_\_vsnprintf，该符号在函数 \_\_glfwInputError 中被引用 LearnOpenGL E:\kSource\LearnOpenGLk\LearnOpenGL\glfw3.lib(init.obj) 1

原因：问题是 glfw 静态 libs 是用与您正在使用的版本不同的 visual studio 版本构建的。
> 你也可以添加一个额外的库到你的链接器输入，即 legacy_stdio_definitions.lib。进入“属性”>“链接器”>“输入”。在其他依赖项中添加上面提到的库。<https://zgserver.com/parsing-6.html>


## 第一课

- 状态机上下文软件环境

    状态机：当前绘制状态、光照设置、纹理设置、材质设置。

- GLFW 窗口

    生成窗口，支持 OpenGL 上下文。

- GLAD

    用户画图。

- 顶点数组对象 VAO 顶点缓冲对象 VBO

    * 顶点数组对象：Vertex Array Object，VAO
    * 顶点缓冲对象：Vertex Buffer Object，VBO
    * 索引缓冲对象：Element Buffer Object，EBO 或 Index Buffer Object，IBO

    输入：3D 坐标；输出：2D 像素。

{% include image.html url="/images/OpenGL-GLSL/20201112141055.png" %}

- FragmentShader 片段着色器

    1. 将着色器源码存入字符串
    2. 创建着色器对象
    3. 将源码字符串赋予着色器对象
    4. 编译着色器
    5. 创建着色器程序对象
    6. 将编译好的着色器附加到程序对象上
    7. 链接生成程序

- VertexShader 顶点着色器

- 索引缓冲对象 EBO

    其中在渲染的时候有多重的组合方式：

    VBO / VAO / EBO

    建议使用顶点缓冲区，但是是否索引可以参考他们的优劣：

    * `glDrawArrays` 传输或指定的数据是最终的真实数据，在绘制时效能更好
    * `glDrawElements` 指定的是真实数据的调用索引，在内存 / 显存占用上更节省

- GLSL 数据传输

- VBO 中存放多种属性

- 一个 VAO 对应多个 VBO

[OpenGL ES in iOS - 2. 画一个三角形](https://www.uiimage.com/post/blog/opengl-es/opengl-es-2-draw-a-triangle/)

```cpp
// Default VAO needed for OpenGL 3.3+ core profiles
void setVertexEnv() {
    float vertices[] = {
        -0.5f, -0.5f, 0.0f, // left, down
        0.5f, -0.5f, 0.0f,  // right, down
        -0.5f, 0.5f, 0.0f,  // left, top
    };
    float colors[] = {
        1, 0, 0, // left, down
        0, 1, 0, // right, down
        0, 0, 1, // left, top
    };

    unsigned int VAO; // VAO: vertex array object
    unsigned int VBO[2]; // VBO: vertex buffer object

    glGenVertexArrays(1, &VAO);
    glGenBuffers(2, VBO);

    // 绑定当前上下文
    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO[0]);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    glBindBuffer(GL_ARRAY_BUFFER, VBO[1]);
    glBufferData(GL_ARRAY_BUFFER, sizeof(colors), colors, GL_STATIC_DRAW);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(1);
}
```

- 图元连接方式

{% include image.html url="/images/OpenGL-GLSL/23e3ac4c617.jpg" %}

1. GL_POINTS 每个顶点在屏幕上都是单独的点。
2. GL_LINES 每一对顶点定义一个线段。
3. GL_LINE_STRIP 一个从第一个顶点依次经过每一个后续顶点而绘制的线条。
4. GL_LINE_LOOP 和 GL_LINE_STRIP 相同，但是最后一个顶点和第一个顶点连接起来了。
5. GL_TRIANGLES 每三个顶点构成一个三角形。
6. GL_TRIANGLE_STRIP 三角形带，新增一个顶点，就复用前面的两个顶点，构成一个新的三角形。
7. GL_TRIANGLE_FAN 以一个原点为中心，呈扇形排列，公用相邻顶点的一组三角形。


## 第二课

- shader 类封装

- 加载显示纹理

- 纹理过滤

- 纹理单元

- 齐次坐标

- 线性代数基础：三维里沿着 x 轴旋转

- 线性代数基础：变换

- glm

- 缩放旋转位移顺序问题

- 坐标系统


### 坐标系统

- <https://learnopengl-cn.readthedocs.io/zh/latest/01%20Getting%20started/08%20Coordinate%20Systems/>
- <https://www.mdeditor.tw/pl/pZYE>
- <https://mp.weixin.qq.com/s/0HZgyZra90LQLFAq6dQJ9A>

- 局部空间 (Local Space，或者称为物体空间 (Object Space))
- 世界空间 (World Space)
- 观察空间 (View Space，或者称为视觉空间 (Eye Space))
- 裁剪空间 (Clip Space)
- 屏幕空间 (Screen Space)

$$
V_{clip} = M_{projection} \cdot M_{view} \cdot M_{model} \cdot V_{local}
$$

{% include image.html url="/images/OpenGL-GLSL/coordinate_systems2.png" %}

{% include image.html url="/images/OpenGL-GLSL/173184e0cdd334b3.jpg" %}

在上图中，OpenGL 定义了后三个坐标系（裁剪坐标、NDC 坐标、屏幕坐标），前三个坐标（物体坐标、世界坐标、摄像机坐标）是为了用户方便而自定义的坐标。

{% include image.html url="/images/OpenGL-GLSL/173184b55b0849f7.jpg" %}

$$
\left[\begin{array}{l}
x^{\prime} \\
y^{\prime} \\
z^{\prime} \\
1
\end{array}\right]
=
\left[\begin{array}{llll}
1 & 0 & 0 & \Delta x \\
0 & 1 & 0 & \Delta y \\
0 & 0 & 1 & \Delta z \\
0 & 0 & 0 & 1
\end{array}\right]
\left[\begin{array}{l}
x \\
y \\
z \\
1
\end{array}\right]
=
\left[\begin{array}{c}
x+\Delta x \\
y+\Delta y \\
z+\Delta z \\
1
\end{array}\right]
$$

OpenGL 在每次顶点着色器运行之后，希望可见的顶点都可以转化为标准化设备坐标 (Normalized Device Coordinate, NDC)，也就是说，每个顶点的 x，y，x 坐标都应该在（-1.0，1，0）之间，超出这个坐标范围的顶点都将不可见。通常我们会自定一个坐标的范围，之后再在顶点着色器中将这些坐标转换为标准化设备坐标。然后将这些标准化的坐标传入光栅器，变换为屏幕上的二维坐标或者像素。

物体坐标到世界坐标，主要是位移；世界坐标到视觉坐标，主要包含位移和旋转。最终要换算到 NDC 立方体内，显卡完成后继工作。
glm::mat4 内存结构是列保存的：

```
 1[0][0]  2[0][1]  3[0][2]  4[0][3]
 5[1][0]  6[1][1]  7[1][2]  8[1][3]
 9[2][0] 10[2][1] 11[2][2] 12[2][3]
13[3][0] 14[3][1] 15[3][2] 16[3][3]
```

原始坐标：

```cpp
float vertices[] = {
    -0.5f,-0.5f,0.0f, // left,down
     0.5f,-0.5f,0.0f, // right,down
     0.5f, 0.5f,0.0f, // right,top
    -0.5f, 0.5f,0.0f, // left,top
};
```

{% include image.html url="/images/OpenGL-GLSL/20201210173525.png" %}

```cpp
glm::mat4 model=glm::mat4(1.0f);
// 默认应该是正交投影，饶 x 轴逆时针旋转 55°
model=glm::rotate(model,glm::radians(55.0f),glm::vec3(1.0f,0.0f,0.0f));
```

{% include image.html url="/images/OpenGL-GLSL/20201210173853.png" %}

```cpp
glm::mat4 view = glm::mat4(1.0f);
// 往上平移 0.5f，往后平移 1.0f。
// 只能看到半截，因为默认是一个 [-1,1] 的立方体正交，另外半截超出边界了。
view=glm::translate(view,glm::vec3(0.0f,0.5f,-1.0f));
```

{% include image.html url="/images/OpenGL-GLSL/20201210174245.png" %}

```cpp
glm::mat4 projection = glm::mat4(1.0f);
// 最终结果，是一个摄像机在原点的透视。
// 摄像机位置应该在 原点。
projection=glm::perspective(glm::radians(90.0f),800.0f/600.0f,0.1f,10.0f);
```

{% include image.html url="/images/OpenGL-GLSL/20201210174453.png" %}


## 第三课

- 坐标系实例

- 立方体

- 摄像机

- LookAt

- 摄像机 WASD 空指

- 摄像机旋转缩放

- 代码整理 Camera 封装


## 运行结果

相机源码：<https://github.com/JoeyDeVries/LearnOpenGL/blob/master/src/1.getting_started/7.4.camera_class/camera_class.cpp>

{% include image.html url="/images/OpenGL-GLSL/boxtest.gif" %}

{% include image.html url="/images/OpenGL-GLSL/glIntroGrab.gif" %}

-----

<font class='ref_snapshot'>Reference snapshot, script generated automatically.</font>

- [1] [https://github.com/hawkhai/LearnOpenGL.git]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/github.com/1371fb1d.git" %})
- [2] [https://gitee.com/hawkhai/opengl-3rd.git]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/gitee.com/3cdcc6e8.git" %})
- [3] [https://www.uni-marburg.de/en/fb12/research-groups/grafikmultimedia/lectures/graphics]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/www.uni-marburg.de/2b3b5349.html" %})
- [4] [https://www.mathematik.uni-marburg.de/~thormae/lectures/graphics1/graphics_9_1_eng_web.html]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/www.mathematik.uni-marburg.de/cda8cdff.html" %})
- [5] [http://ogldev.atspace.co.uk/index.html]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/ogldev.atspace.co.uk/dc93b5ea.html" %})
- [6] [https://www.bilibili.com/video/BV1px41197A5]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/www.bilibili.com/e1622428.html" %})
- [7] [https://ke.qq.com/course/package/25480?flowToken=1019441]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/ke.qq.com/3fd1c97a.html" %})
- [8] [https://learnopengl-cn.github.io/]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/learnopengl-cn.github.io/e0710dd2.html" %})
- [9] [https://github.com/Groovounet/ogl-samples]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/github.com/da66ecca.html" %})
- [10] [https://github.com/hawkhai/openglcpp.git]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/github.com/24544c96.git" %})
- [11] [https://www.cnblogs.com/chen9510/p/12000320.html]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/www.cnblogs.com/717083ae.html" %})
- [12] [https://blog.csdn.net/qq_39561000/article/details/103112147]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/blog.csdn.net/b11e47b9.html" %})
- [13] [https://www.saschawillems.de/blog/2015/04/19/using-opengl-es-on-windows-desktops-via-egl/]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/www.saschawillems.de/5efcfffd.html" %})
- [14] [https://wiki.maemo.org/SimpleGL_example]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/wiki.maemo.org/ceafcc8b.html" %})
- [15] [https://blog.csdn.net/iEearth/article/details/71180457]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/blog.csdn.net/6ff86f67.html" %})
- [16] [https://github.com/McNopper/EGL]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/github.com/84bf5cd8.html" %})
- [17] [https://learnopengl-cn.github.io/04%20Advanced%20OpenGL/08%20Advanced%20GLSL/#uniform]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/learnopengl-cn.github.io/f1d48aaa.html" %})
- [18] [https://www.cnblogs.com/chen9510/p/11447292.html]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/www.cnblogs.com/cfd7fec8.html" %})
- [19] [https://www.khronos.org/opengl/wiki/Uniform_Buffer_Object]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/www.khronos.org/04bc8242.html" %})
- [20] [https://zgserver.com/parsing-6.html]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/zgserver.com/060e6561.html" %})
- [21] [https://www.uiimage.com/post/blog/opengl-es/opengl-es-2-draw-a-triangle/]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/www.uiimage.com/9d22c628.html" %})
- [22] [https://learnopengl-cn.readthedocs.io/zh/latest/01%20Getting%20started/08%20Coordinate%20Systems/]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/learnopengl-cn.readthedocs.io/cfc9cf0a.html" %})
- [23] [https://www.mdeditor.tw/pl/pZYE]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/www.mdeditor.tw/c5442ada.html" %})
- [24] [https://mp.weixin.qq.com/s/0HZgyZra90LQLFAq6dQJ9A]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/mp.weixin.qq.com/25763337.html" %})
- [25] [https://github.com/JoeyDeVries/LearnOpenGL/blob/master/src/1.getting_started/7.4.camera_class/camera_class.cpp]({% include relref.html url="/backup/2020-11-11-shader-OpenGL.md/github.com/5c619a05.cpp" %})