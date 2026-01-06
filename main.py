import sys
import keyboard
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal

# 导入各个模块
from services import SentimentEngine, LLMEngine
from ui import MainWindow

# 键盘监听必须通过信号与 GUI 通信
class HotkeyBridge(QObject):
    triggered = pyqtSignal()

def main():
    app = QApplication(sys.argv) # 创建QApplication的线程是主线程

    # 1. 实例化业务层 (Model/Service)
    print("正在初始化引擎...")
    sentiment_engine = SentimentEngine()
    llm_engine = LLMEngine()

    # 2. 实例化界面层 (View)，并注入业务层
    window = MainWindow(sentiment_engine, llm_engine) # 这处代码就是依赖注入，我依赖需要的引擎作为参数送进来，降低耦合，方便更新
    # 非依赖注入：要用的东西自己准备

    # 3. 设置控制器逻辑 (Controller Logic) - 这里通过简单的信号连接
    bridge = HotkeyBridge()
    #bridge.triggered.connect(window.handle_clipboard)
    bridge.triggered.connect(window.toggle_window) # 触发窗口

    def on_hotkey():
        bridge.triggered.emit() # Qt不允许在后台线程控制GUI窗口/界面，必须保留在主线程

    try:
        keyboard.add_hotkey('ctrl+shift+c', on_hotkey, suppress=False)
        print("🚀 程序启动成功！监听 Ctrl+Shift+C 中...")
        print("💡 提示：按一次弹出分析，再按一次即可快速关闭窗口")
    except Exception as e:
        print(f"⚠️ 热键注册失败: {e}")

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()