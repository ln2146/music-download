---
name: music-download
description: 搜索和下载音乐、解析歌单，覆盖酷我、酷狗、网易云、QQ、咪咕、汽水及 Apple Music、Spotify 等 17 个平台。用户指定平台时遵循指定范围，未指定时由 agent 选择平台。适用于查找歌曲文件、批量下载和歌单下载；纯音乐讨论或推荐无需调用。
---

# 音乐搜索与下载

本 skill 自带脚本直接调用 musicdl，无需 musicDownload 项目或桌面界面。下文 `<skill>` 指本 SKILL.md 所在目录，执行时替换为实际绝对路径。

## 安装

首次安装或迁移目录后执行：

```sh
sh <skill>/scripts/setup.sh
<skill>/scripts/music sources
```

需要 uv；setup 创建独立 Python 3.13 环境并安装 requirements.txt，无图形界面依赖。已安装时直接运行 scripts/music。迁移目录不能复用旧 .venv，重新运行安装。可用 UV_DEFAULT_INDEX 显式选择包索引，不自动切换镜像。

## 平台选择

- 用户指定平台时仅在指定范围操作，不因失败自行切换范围外的平台。
- 用户未指定时，根据歌曲、语言、地区、已有账号配置和本次结果自主选择一个或多个平台，无需每次询问。没有固定顺序或脚本内置的平台回退链，告知本次选择。
- 歌单根据链接归属选择平台。见 [references/platforms.md](references/platforms.md)。
- sources 列出全部 17 个平台 ID、别名和配置情况。configured 只表示存在配置，不表示登录有效或已测试成功。
- 需要参考已有实测记录时读 [references/test-results.md](references/test-results.md)；它是带日期的本机快照，不是固定的平台优先顺序或永久可用性保证。
- 无账号时可能通过第三方解析。遵循当前 musicdl 路径，不能声称仅调用官方接口或使用了用户会员身份。

## 搜索和下载

```sh
<skill>/scripts/music search --query "歌名 歌手" --sources netease,qq --limit 3
<skill>/scripts/music download --search-id <search_id> --items qq:1 --output <绝对保存目录>
```

stdout 是 JSON。操作失败会返回非零退出码及结构化结果；即使退出码 1 也读取 JSON，partial 中仍可能有可用结果或已下载文件。results 按平台返回状态、候选、诊断计数和私有日志路径。候选包含 item_id、歌名、歌手、专辑、格式、时长、大小、平台和已观测到的解析方法。resolver 为 null 表示未知，不猜测。

仅搜索请求不要下载。用户明确要求下载且匹配清楚时继续执行；演唱者、现场版或翻唱版明显有歧义时让用户选择。按真实元数据选曲，不引入固定评分或正则规则。用户未指定目录时可使用当前任务目录下“已下载音乐”，并告知路径。仅报告实际格式，不承诺无损，不擅自替换用户明确指定的音质。

search_id 和 item_id 引用本机快照，下载复用原始对象。链接失效时报告失败；需要重搜时说明并重新选择。脚本不自动换平台或重搜。

批量使用逗号分隔候选：--items qq:1,netease:2。逐项报告成功与失败。downloaded 只计底层返回且实际存在的文件。回复中提供可点击的绝对文件路径，注明平台、实际格式，以及已知的第三方解析方式。

## 歌单

```sh
<skill>/scripts/music playlist --url '<歌单URL>' --sources netease --timeout 300
```

该命令只解析为候选。用户要求整个歌单下载时把返回候选交给 download；只要求查看时展示列表。支持程度由 musicdl 决定，NotImplementedError 或网络错误需要明确说明，不编造内容。

## 配置与运行

默认读取 ~/.config/music-download/config.json（可不存在），也可在子命令前传 --config <文件>。结构见 [references/platforms.md](references/platforms.md)。账号配置在 skill 外部，不将 Cookie、Token 放入聊天、分享包或普通命令行参数。

状态默认位于 ~/.local/share/music-download，可用 MUSIC_DOWNLOAD_STATE_DIR 或子命令前的 --state-dir 指定。状态包含原始对象 pickle 快照和私有日志，可能含临时授权信息；仅加载本安装生成的快照，不导入别人提供的 pickle 或状态库。面向模型的 JSON 不输出音频授权 URL、Cookie、原始响应；读取日志排错时不要把完整日志贴入聊天。打包不包含状态和 .venv。

--timeout 是每个平台进程的运行期限，默认 120 秒；--jobs 是并行平台数，默认 3；--limit 是每平台搜索目标数量，默认 5。搜索会解析音频地址，数量不代表请求次数。超时会终止对应工作进程并返回 timeout，不选择替代平台。长歌单可显式提高 timeout。

no_downloadable_results 表示底层未返回可下载对象，不等于曲库没有这首歌。上游部分解析异常被吞掉，不能据空结果推断原因；已观测到的错误计数和私有日志路径会附带返回。worker_failed、error 和 timeout 都是明确失败，不能报告完成。
