# 独立安装测试记录

测试日期：2026-10-27（Asia/Taipei）。环境：macOS arm64、Python 3.13.13、musicdl 2.14.2。

skill 已单独安装到用户技能目录，创建独立 .venv，从 /tmp 执行搜索、歌单和下载。运行代码没有原 musicDownload 项目的路径或导入；依赖包来自独立技能环境。技能安装环境含 52 个包，不含 Qt。

## 真实平台测试

使用关键词“晴天”，每平台目标数量 1；此测试验证下载链路，候选包括不同演唱者、不同歌曲和版本，不能把它们都解释为周杰伦原版。没有提供用户账号。

首轮全部 17 平台：每平台 60 秒，平台并发 6，client.max_retries=1，requests.timeout=[8,12]。其中 9 个平台返回候选并实际完成下载。

QQ、Joox 随后仅配置 client.max_retries=1，采用上游原生请求参数，90 秒期限，完成搜索和下载。部分上游解析函数自己传入 timeout，因此第一轮覆盖请求超时会使这些分支失效；已在 platforms.md 记录，不静默修改用户的配置。

完成真实搜索与下载的 11 个平台：

- 5sing：MP3。
- Jamendo：FLAC。
- 酷我：FLAC。
- 酷狗：MP3，本次记录到第三方解析方法 _parsewith90svipapi。
- 咪咕：MP3。
- 网易云：MP3。
- QQ音乐：FLAC。
- 千千：FLAC。
- StreetVoice：HLS 下载为 MP3。
- 汽水：M4A/AAC。
- Joox：MP3。

11 个实际文件合计 367,530,250 字节；用 PyAV 打开全部音轨并成功解码首个音频帧。此检查确认文件可读和音频可解码，不证明音源母带品质，也不代表对整首内容做了人工听审。

本次未跑通的 6 个平台：

- Apple Music：请求 amp-api.music.apple.com 时 SSL EOF。
- Deezer：接口读取超时。
- Qobuz：SSL 连接错误。
- SoundCloud：接口返回 HTTP 401。
- Spotify：60 秒进程期限内未完成。
- TIDAL：缺少用户 SessionStorage 账号配置，上游构造函数明确抛出 AssertionError。

以上是本机当次结果，不代表这些平台永久不支持。账号专用下载未获得用户凭据，未测试。Apple/TIDAL 原生音频对象的本地快照保存与恢复已在离线测试中覆盖。

## 歌单

- StreetVoice：https://www.streetvoice.cn/svmusic_cn/playlists/880153/ ，成功解析 14 首候选，未自动下载。
- 网易云示例歌单：https://music.163.com/#/playlist?id=7583298906 ，45 秒期限内未完成，返回 timeout。

## 离线集成测试

运行 `.venv/bin/python -m unittest discover -s tests -v`，4 项通过：

1. 17 平台对应的上游实现存在，中文别名正确，列平台命令不创建歌曲状态。
2. Apple DownloadItem、TIDAL StreamUrl、二进制内容经私有快照恢复后保留原生类型。
3. 使用本地 HTTP 服务和生成的 WAV 测试音频执行真实下载；一个成功、一个 HTTP 404 时返回 partial，成功文件的音频采样与输入一致。该测试明确使用人工生成的测试素材，不冒充平台歌曲。
4. 不存在的候选返回明确 LookupError，不生成成功结果。

SKILL.md 规范检查通过；独立环境的 52 个依赖通过 uv pip check。
