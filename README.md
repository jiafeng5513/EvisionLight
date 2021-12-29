<div align=center><img width="100" height="100" src="./doc/Evision.ico"/></div>

<div align=center>EvisionLight 双目视觉系统(轻量版)</div>
<div align=center></div>
<div align=center>如果您觉得有帮助,请为该项目点star.以便于及时收到最新更新.</div>

*本项目致力于构建一个轻量化,图形化,高效率的机器视觉Demo,目的是为机器视觉初学者提供一份良好的入门参考代码.*

### About
1. ui采用PySide2-Widget模式编写,界面定义使用ui文件.
2. 界面逻辑使用python编写.
3. 有性能要求的算法使用C++实现,输出动态链接库.

### Requirements
1. PyCharm, a free python IDE.
2. python3, We strongly recommend using Anaconda3 as your python env.
3. pyside2, you can install it by `pip install pyside2`
4. opencv-python, you can install it by `pip install opencv-python`

### Build
1. `python3 init.py` to generate *_ui.py and *_rc.py from *.ui and *.qrc.
2. `python3 main.py` to start sandbox.

### Bugs

### References
1. [gitignore模板](https://github.com/github/gitignore).
2. [清华大学开源镜像站: pypi源](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)
3. [清华大学开源镜像站: Anaconda源](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)
4. [bug fix: This application failed to start because no Qt platform plugin could be initialized](https://blog.csdn.net/zouxin_88/article/details/106052228)