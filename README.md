# music-download

<p align="center">
  <img src="assets/readme-cover.png" alt="music-download：一句指令，让音乐落地。" width="100%">
</p>

**供 Claude Code、Codex 使用的音乐搜索与下载 skill。** 支持跨平台搜索、歌曲版本选择、单曲与批量下载、歌单解析，结果保存到本地。

你可以指定平台，也可以让 agent 根据需求选择。底层直接调用 musicdl，拥有独立的 Python 环境，无需桌面应用。

## 安装

需要 **Git 和 uv**。选择对应的安装目录执行，脚本会创建 Python 3.13 环境并安装固定版本依赖。当前实测环境为 macOS arm64，安装脚本使用 POSIX shell。

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

自定义了 `CODEX_HOME` 时，使用对应的 `skills` 目录。目标目录已有安装时，先检查并保留本地修改。两边分别执行 `setup.sh`；迁移目录后重新创建环境，不直接复制已有 `.venv`。

## 使用

安装后，在新会话中直接提出需求：

**让 agent 选择平台并下载**

> 使用 music-download，帮我下载周杰伦演唱的《晴天》，平台你来选，保存到当前项目的已下载音乐目录。

**指定平台，先看候选**

> 使用 music-download，只在网易云和 QQ 音乐里搜索《晴天》，先列出候选让我选。

**从歌单中选择歌曲**

> 使用 music-download，解析这个歌单并列出歌曲，下载我选中的几首。

仅要求搜索时只搜索；明确要求下载且匹配清楚时继续执行。同名歌、翻唱或现场版有歧义时，agent 会展示候选。完整调用规则见 [SKILL.md](SKILL.md)。

<details>
<summary>进阶：直接调用命令行</summary>

以下命令在仓库根目录执行。stdout 为 JSON，退出码 `1` 可能表示部分成功，仍需读取各项结果。

```sh
# 列出平台与别名
./scripts/music sources

# 在指定平台搜索
./scripts/music search --query "晴天 周杰伦" --sources netease,qq --limit 3

# 替换搜索返回的 search_id 和实际候选 ID 后下载
./scripts/music download --search-id "<search_id>" --items qq:1 --output "$PWD/已下载音乐"

# 解析歌单，返回候选，后续按需求调用下载
./scripts/music playlist --sources streetvoice --url 'https://www.streetvoice.cn/svmusic_cn/playlists/880153/' --timeout 300
```

脚本要求显式传入搜索平台。自然语言请求未指定平台时，由 agent 决定参数；脚本不内置固定的平台优先顺序或自动替代源。

</details>

## 支持平台

共 **17 个平台适配器**：

酷我 · 酷狗 · 网易云 · QQ音乐 · 咪咕 · 千千 · 汽水 · 5sing<br>
Apple Music · Deezer · Jamendo · Joox · Qobuz · SoundCloud · StreetVoice · Spotify · TIDAL

部分平台需要账号或额外配置，部分解析路径使用第三方服务。实际可用性受接口、地区、账号与网络条件影响。平台 ID、别名和配置要求见 [平台与配置](references/platforms.md)。

## 配置

- **账号配置**：`~/.config/music-download/config.json`，可选。
- **搜索状态与日志**：`~/.local/share/music-download`。
- **自定义路径**：在子命令前使用 `--config <文件>`、`--state-dir <目录>`。
- **执行期限**：每个平台默认 120 秒，用 `--timeout` 调整；较长歌单可适当增加。

账号凭据由用户在本地配置。状态包含原生歌曲对象快照和私有日志，可能带有临时授权信息，不应分享状态目录或加载他人提供的 pickle、状态库。详细字段见 [平台与配置](references/platforms.md)。

## 测试

2026-10-27 的本机测试中，**11 个平台**完成真实搜索与下载，**14 首歌曲**从一个 StreetVoice 歌单中解析为候选，**4 项离线集成测试**通过。

其余 6 个平台当次遇到网络、接口、超时或账号条件限制。完整的平台结果、测试参数与限制见 [实测记录](references/test-results.md)。记录反映当次环境，不构成持续可用性保证。

在仓库根目录运行离线集成测试：

```sh
.venv/bin/python -m unittest discover -s tests -v
```

测试覆盖平台映射、专用对象快照、本地 HTTP 下载与批量部分失败、未知候选错误。

## 项目来源与许可

核心平台能力来自 [musicdl](https://github.com/CharlesPikachu/musicdl)，早期需求参考了 [MrsEWE44/musicDownload](https://github.com/MrsEWE44/musicDownload) 桌面项目的功能范围。

本仓库不附带歌曲文件、共享账号或第三方解析服务的凭据。依赖项目有各自的许可证；musicdl 2.14.2 随包提供 PolyForm Noncommercial License 1.0.0，使用时请阅读其许可证。

---

宣传素材：[README 封面](assets/readme-cover.png) · [竖版海报](assets/promo-poster.png) · [图片生成说明与提示词](assets/image-prompts.md)
