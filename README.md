# Music Download Skill

供 Claude Code、Codex 等具备本地命令执行能力的 agent 使用的音乐搜索与下载 skill。用户可以指定平台，也可以让 agent 根据需求选择平台。运行时独立于桌面 musicDownload 项目，直接调用 musicdl，无需 Qt 图形界面。

## 功能

- 搜索歌曲，返回便于 agent 使用的 JSON 候选。
- 按候选 ID 下载单曲或批量下载，逐项报告成功与失败。
- 解析歌单，按用户要求继续选择和下载。
- 保存原生歌曲对象，支持平台专用音频对象与跨命令调用。
- 支持用户提供的本地账号配置，并报告已观测到的解析方式。

平台范围：酷我、酷狗、咪咕、网易云、QQ音乐、千千、汽水、Apple Music、Deezer、5sing、Jamendo、Joox、Qobuz、SoundCloud、StreetVoice、Spotify、TIDAL，共 17 个。

存在适配器不代表平台在任何时间、地区和账号条件下都可用。部分平台依赖第三方解析，部分平台需要账号或额外配置。详见 [平台与配置](references/platforms.md)。

## 安装

需要 Git 和 uv。安装脚本通过 uv 创建独立的 Python 3.13 环境，并安装 requirements.txt 中固定版本的依赖。当前实测环境为 macOS arm64；脚本使用 POSIX shell。

### Claude Code

```sh
git clone https://github.com/ln2146/music-download.git ~/.claude/skills/music-download
sh ~/.claude/skills/music-download/scripts/setup.sh
~/.claude/skills/music-download/scripts/music sources
```

### Codex

```sh
git clone https://github.com/ln2146/music-download.git ~/.codex/skills/music-download
sh ~/.codex/skills/music-download/scripts/setup.sh
~/.codex/skills/music-download/scripts/music sources
```

自定义了 CODEX_HOME 时，将 Codex 安装路径替换为对应的 skills 目录。目标目录已存在时，先检查已有安装，不覆盖其中的本地修改。两边分别执行 setup，不能直接复制已创建的 .venv 到另一目录。

安装后在新会话中请求：

> 使用 music-download，帮我搜索周杰伦演唱的《晴天》，平台你来选。

> 使用 music-download，从网易云下载我选中的歌曲，保存到当前项目的已下载音乐目录。

完整调用规则见 [SKILL.md](SKILL.md)。

## 直接调用

以下命令在仓库根目录执行：

```sh
# 平台 ID、别名及配置情况
./scripts/music sources

# 仅在指定平台搜索
./scripts/music search --query "晴天 周杰伦" --sources netease,qq --limit 3

# 将返回的搜索 ID 和候选 ID 填入对应参数
./scripts/music download --search-id <search_id> --items qq:1 --output /absolute/output/directory

# 解析歌单，返回候选，不自动下载
./scripts/music playlist --sources netease --url 'https://music.163.com/#/playlist?id=7583298906' --timeout 300
```

脚本要求显式传入搜索平台；未指定平台的自然语言请求由 agent 决定如何调用，不在脚本内设置固定的平台优先顺序或自动替代源。

stdout 输出 JSON。退出码 1 可能表示部分成功，仍应读取 JSON 中各平台、各文件的状态。每个平台默认运行期限为 120 秒，可用 --timeout 调整。歌单解析可能耗时较长。

## 本地配置与状态

- 可选配置文件：`~/.config/music-download/config.json`。
- 默认状态目录：`~/.local/share/music-download`。
- 自定义参数：子命令前使用 `--config <文件>`、`--state-dir <目录>`。

账号凭据由用户在本地配置，不包含在本仓库。状态包含原始歌曲对象快照与私有后端日志，可能带有临时授权信息；不要分享状态目录，也不要加载他人提供的 pickle 或状态库。

## 测试

```sh
.venv/bin/python -m unittest discover -s tests -v
```

4 项离线集成测试覆盖平台映射、原生对象快照、真实本地 HTTP 下载与批量部分失败、未知候选错误。测试音频由测试代码生成，不冒充平台资源。

2026-10-27 的本机联网测试中，11 个平台完成搜索和实际下载，StreetVoice 歌单解析出 14 首候选。其余平台的网络、认证或超时情况，以及测试条件，见 [完整测试记录](references/test-results.md)。这些是带日期的实测结果，不构成持续可用性保证。

## 底层项目

核心平台能力来自 [musicdl](https://github.com/CharlesPikachu/musicdl)。本 skill 的早期需求参考了 [MrsEWE44/musicDownload](https://github.com/MrsEWE44/musicDownload) 桌面项目的功能范围。

本仓库不附带歌曲文件、共享账号或第三方解析服务的凭据。依赖项目有各自的许可证；musicdl 2.14.2 随包提供 PolyForm Noncommercial License 1.0.0，使用时请阅读其许可证。
