# 马斯克访谈中文全文阅读网站

根据用户提供的英文文字稿制作的静态阅读网站，包含 394 段中英对照、14 个主题章节和完整中文译文。

在线阅读：https://musk-interview-zh-reader.dearpony18.chatgpt.site

## 功能

- 舒适阅读：合并连续发言，区分主持人提问与马斯克回答。
- 中英对照：保留原稿逐段对应。
- 全文搜索、字号调整、章节导航、阅读位置记忆。
- 下载中文全文；适配手机和桌面。
- 无前端依赖，纯 HTML、CSS 与 JavaScript。

## 本地使用

直接用浏览器打开 `dist/index.html`，或运行：

```sh
python3 -m http.server 8000 --directory dist
```

然后访问 http://localhost:8000 。

## 修改与构建

需要 Python 3，无须安装第三方包。在仓库根目录运行：

```sh
python3 build.py
```

`build.py` 先生成中英对照页面，再调用 `readability.py` 生成舒适阅读版。

## 文件

- `source.json`：上传文字稿提取出的 394 段英文原文。
- `translations.json`：按原文顺序逐段对应的中文译文。
- `build.py`：静态页面生成器。
- `readability.py`：连续对话排版与阅读工具。
- `dist/`：可直接使用的静态网站及中文文本。

## 翻译说明

原视频：[The full-length interview with Elon Musk | The Economist](https://www.youtube.com/watch?v=XuoqKYxDHVc)。译文依据用户上传的 Word 文字稿整理，保留完整对话并整理口头重复。原稿没有时间码，且存在语音识别错误；不确定内容已标注，未逐句核对视频音轨。章节标题为方便阅读而添加。
