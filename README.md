# music-download

<p align="center">
  <img src="assets/readme-cover.png" alt="music-download：一句指令，让音乐落地。支持 Claude Code、Codex 与 17 个音乐平台适配。" width="100%">
</p>

<p align="center">
  <strong>把找歌、选曲和下载，交给你的 Agent。</strong><br>
  Claude Code / Codex · 17 个平台适配 · JSON CLI · 独立运行
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> ·
  <a href="#支持平台">支持平台</a> ·
  <a href="#实测记录">实测记录</a> ·
  <a href="#宣传图">宣传图</a>
</p>

`music-download` 是一个供 agent 使用的音乐搜索与下载 skill。你说出想听的歌，agent 根据歌手、专辑和版本选择候选，再将音频下载到指定目录。平台由你指定，也可以交给 agent 选择。

底层直接调用 musicdl，安装后拥有自己的 Python 环境，独立运行，无需桌面应用。

## 先试着说一句

> 使用 music-download，帮我下载周杰伦演唱的《晴天》，平台你来选，保存到当前项目的已下载音乐目录。

> 只在网易云和 QQ 音乐里搜索这首歌，先列出候选让我选。

> 解析这个歌单，列出歌曲，下载我选中的几首。

明确要求搜索时，只搜索；明确要求下载且匹配清楚时，继续执行。遇到同名歌、翻唱或现场版等歧义，agent 会展示候选供你选择。

## 它能做什么

- **按你的范围找歌**：指定单个平台或多个平台；未指定时由 agent 结合需求选择。
- **找到版本再下载**：候选包含歌名、歌手、专辑、格式等信息，下载引用本机搜索快照。
- **单曲与批量下载**：逐项返回实际文件路径、格式和成功或失败状态。
- **从歌单开始**：将歌单解析为候选，按用户要求继续选择和下载。
- **给 agent 清晰的结果**：JSON 输出，与终端进度信息分离；已观测到的解析方式随结果返回。

```mermaid
flowchart LR
    A[你提出需求] --> B[Agent 选择平台]
    B --> C[搜索或解析歌单]
    C --> D[选择歌曲版本]
    D --> E[下载到本地]
```

## 快速开始

准备好 **Git 与 uv**，选择你的 agent 安装目录执行。脚本会创建 Python 3.13 环境并安装固定版本依赖。当前实测环境为 macOS arm64，安装脚本使用 POSIX shell。

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

安装后在新会话中说“使用 music-download”，即可开始。完整的 agent 调用规则见 [SKILL.md](SKILL.md)。

<details>
<summary>自定义路径、已有安装与依赖环境</summary>

自定义了 `CODEX_HOME` 时，将 Codex 安装路径替换为对应的 `skills` 目录。目标目录已存在时，先检查已有安装，保留本地修改。

Claude Code 和 Codex 两边分别执行 `setup.sh`。迁移目录后重新创建环境，不能直接复制已有 `.venv`。需要选择包索引时，使用 uv 的 `UV_DEFAULT_INDEX` 环境变量显式设置。

</details>

## 支持平台

**酷我 · 酷狗 · 网易云 · QQ音乐 · 咪咕 · 千千 · 汽水 · 5sing**

**Apple Music · Deezer · Jamendo · Joox · Qobuz · SoundCloud · StreetVoice · Spotify · TIDAL**

共 **17 个平台适配器**。各平台的 CLI ID、别名、账号配置及歌单说明，见 [平台与配置](references/platforms.md)。

部分平台需要账号或额外配置，部分解析路径使用第三方服务。实际可用性受平台接口、地区、账号与网络条件影响；适配范围与当次测试结果分别记录。

## 实测记录

**2026-10-27，本机实测：**

- **11 个平台**完成真实搜索和下载，生成的 11 个音频文件均能打开音轨并解码首帧。
- **14 首歌曲**从一个 StreetVoice 真实歌单中成功解析为候选。
- **4 项离线集成测试**通过，覆盖平台映射、专用对象快照、本地 HTTP 下载与批量部分失败、未知候选错误。

跑通搜索与下载的平台包括：5sing、Jamendo、酷我、酷狗、咪咕、网易云、QQ音乐、千千、StreetVoice、汽水、Joox。

Apple Music、Deezer、Qobuz、SoundCloud、Spotify、TIDAL 在当次测试中遇到网络、接口、超时或账号条件限制。详细参数、格式与限制见 [完整测试记录](references/test-results.md)。以上是带日期的实测结果，不构成持续可用性保证。

在仓库根目录运行测试：

```sh
.venv/bin/python -m unittest discover -s tests -v
```

## 命令行用法

也可以直接调用脚本。以下命令均在仓库根目录执行。

**列出平台，搜索候选：**

```sh
./scripts/music sources
./scripts/music search --query "晴天 周杰伦" --sources netease,qq --limit 3
```

**下载选中的候选：** 将 `<search_id>` 替换为搜索返回的 ID，`qq:1` 替换为实际候选 ID。

```sh
./scripts/music download --search-id "<search_id>" --items qq:1 --output "$PWD/已下载音乐"
```

**解析歌单：** 此命令返回候选，后续按需求调用下载。

```sh
./scripts/music playlist \
  --sources streetvoice \
  --url 'https://www.streetvoice.cn/svmusic_cn/playlists/880153/' \
  --timeout 300
```

脚本要求显式传入搜索平台。自然语言请求未指定平台时，由 agent 决定参数；脚本不内置固定的平台优先顺序或自动替代源。

stdout 为 JSON。退出码 `1` 可能表示部分成功，仍需读取各项结果。每个平台的默认运行期限为 120 秒，可通过 `--timeout` 调整。

<details>
<summary>本地账号配置与搜索状态</summary>

- 可选配置文件：`~/.config/music-download/config.json`。
- 默认状态目录：`~/.local/share/music-download`。
- 自定义路径：在子命令前使用 `--config <文件>`、`--state-dir <目录>`。

账号凭据由用户在本地配置。状态包含原生歌曲对象快照和私有后端日志，可能带有临时授权信息，不应分享状态目录或加载他人提供的 pickle、状态库。详细字段见 [平台与配置](references/platforms.md)。

</details>

## 宣传图

<details>
<summary>展开查看竖版宣传海报</summary>

<p align="center">
  <a href="assets/promo-poster.png"><img src="assets/promo-poster.png" alt="music-download 宣传海报：搜歌、选曲、下载，交给你的 Agent。" width="420"></a>
</p>

</details>

[README 封面原图](assets/readme-cover.png) · [宣传海报原图](assets/promo-poster.png) · [图片生成说明与提示词](assets/image-prompts.md)

## 项目来源与许可

核心平台能力来自 [musicdl](https://github.com/CharlesPikachu/musicdl)。早期需求参考了 [MrsEWE44/musicDownload](https://github.com/MrsEWE44/musicDownload) 桌面项目的功能范围。

本仓库不附带歌曲文件、共享账号或第三方解析服务的凭据。依赖项目有各自的许可证；musicdl 2.14.2 随包提供 PolyForm Noncommercial License 1.0.0，使用时请阅读其许可证。
