# SocialReply-Assistant

## 📖 项目简介
SocialReply Assistant 是一个基于 **PyQt5** 和 **混合AI模型**（本地逻辑回归 + 云端 LLM）开发的桌面端辅助工具。
它旨在帮助“社恐”人群或职场人士快速分析社交文本的语气倾向，并提供得体、高情商的回复建议。

**主要功能：**
* **划词分析**：全局热键 `Ctrl+Shift+C` 一键唤起，无缝衔接微信/QQ/网页。
* **双模引擎**：
  * 本地模型（Sklearn）：毫秒级判断情感（积极/消极/中性）。
  * 云端模型（DeepSeek/OpenAI）：生成三种不同风格的回复策略。
* **交互优化**：鼠标跟随弹窗、一键复制、动态主题配色。

---

## 🛠️ 环境要求 (Prerequisites)

为了确保系统正常运行，请满足以下环境要求：

* **操作系统**：Windows 10/11 (推荐)，macOS 或 Linux (需自行配置热键权限)
* **Python 版本**：Python 3.8 及以上
* **网络**：需要连接互联网以调用 LLM API
  * 本项目默认调用的模型为ChatECNU，可查看说明文档👉[华东师范大学开发者平台](https://developer.ecnu.edu.cn/vitepress/llm/model.html)

---

## 🚀 安装与部署步骤 (Installation)

### 1. 获取项目代码
解压提交的代码包，或进入项目根目录：
```bash
cd SocialReplyAssistant
```

### 2. 安装依赖库
建议使用虚拟环境，在终端中执行以下命令安装所需依赖：
```bash
pip install -r requirements.txt
```

### 模型文件检查
请确保根目录下包含 data 文件夹，且内部包含以下预训练模型文件（已随代码提交）：
- `data/sentiment_model.pkl` (逻辑回归模型)
- `data/tfidf_vectorizer.pkl` (TF-IDF 向量化器)

### 4. 配置文件设置 (重要!)
本项目通过环境变量管理 API 密钥。
1. 在项目根目录找到 .env.example 文件（如果没有，请新建一个 .env 文件）。
2. 将文件重命名为 .env。
3. 编辑 .env 文件，填入你的 API Key 和 Base URL：
```Ini
# .env 文件配置示例
SCHOOL_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxx
SCHOOL_API_URL=[https://api.deepseek.com/v1](https://api.deepseek.com/v1)
SCHOOL_MODEL_NAME=deepseek-chat
```

## ▶️ 运行说明 (Usage)

1. **启动程序：** 在终端执行：
```bash
python main.py
```

_若看到控制台输出 "🚀 程序启动成功！监听 Ctrl+Shift+C 中..." 代表启动成功。_

2. **使用方法：**

- 保持程序后台运行。

- 在任意界面（如微信、记事本）选中一段文字 **并复制到剪贴板**。

- 按下快捷键 `Ctrl + Shift + C`。

- 助手窗口将自动在鼠标旁弹出，显示语气分析结果，并可以选择生成建议回复。

## 📂 目录结构说明

```plaintext
SocialReplyAssistant/
├── assets/             # 资源文件 (图标, 主题配置)
├── data/               # 模型数据 (pkl文件)
├── services/           # 业务逻辑层 (情感分析, LLM调用)
├── ui/                 # 界面层 (主窗口, 卡片组件)
├── config.py           # 全局配置管理
├── main.py             # 程序启动入口
├── requirements.txt    # 项目依赖
└── README.md           # 说明文档
```

---
## ⚠️ 注意事项

- **热键冲突**：如果 `Ctrl+Shift+C` 无法唤起，可能是与其他软件（如显卡驱动）热键冲突，可在 `main.py` 中修改热键组合。

- **API 额度**：请确保 `.env` 中的 API Key 有剩余额度，否则无法生成回复建议。
- **⚠️冗余文件**：项目目录下的`./app`和`./backup`文件夹为开发过程中的实验性代码，**仅作存档保留，请勿运行**，所有核心功能均通过 `main.py` 启动。

## 📢 致谢与引用 (Acknowledgments)

* **图标素材**：本项目使用的 `chat.png` 下载自 [阿里巴巴矢量图标库 (Iconfont)](https://www.iconfont.cn/)，版权归原作者所有。
* **开源库**：感谢 PyQt5, Jieba, Scikit-learn 等开源社区提供的强大工具支持。