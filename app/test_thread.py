import sys
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread

print(f"1. Python 启动时的线程: {threading.current_thread().name}")


def run_app():
    # 这里的代码是在子线程里跑的
    print(f"2. 准备创建 QApplication 的线程: {threading.current_thread().name}")

    # 【关键时刻】在这里创建 app，那么这个子线程就会变成 Qt 眼里的“主线程”
    app = QApplication(sys.argv)

    print(f"3. Qt 认为的主线程是: {app.instance().thread()}")
    print(f"4. 当前执行线程对象: {QThread.currentThread()}")

    # 如果这里对比一致，说明 Qt 认准了这条线程
    if app.instance().thread() == QThread.currentThread():
        print("✅ 验证成功：谁创建了 app，谁就是老大！")


# 我们故意搞事，不开在主线程，而是开一个子线程去启动 Qt
t = threading.Thread(target=run_app, name="MySubThread")
t.start()
t.join()