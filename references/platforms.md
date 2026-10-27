# 平台与配置

## 平台目录

对应原界面全部 17 个选项；名称映射是接口配置，不是选择优先级。

- apple：苹果音乐 / Apple Music，链接 music.apple.com。
- deezer：Deezer，链接 deezer.com。
- 5sing：5sing，链接 5sing.kugou.com。
- jamendo：Jamendo，链接 jamendo.com。
- joox：Joox，链接 joox.com。
- kuwo：酷我音乐，链接 kuwo.cn。
- kugou：酷狗音乐，链接 kugou.com。
- migu：咪咕音乐，链接 music.migu.cn。
- netease：网易云音乐，链接 music.163.com。
- qq：QQ音乐，链接 y.qq.com / c.y.qq.com。
- qianqian：千千音乐，链接 music.91q.com。
- qobuz：Qobuz，链接 qobuz.com。
- soundcloud：SoundCloud，链接 soundcloud.com / on.soundcloud.com。
- streetvoice：StreetVoice / 街声，链接 streetvoice.com。
- soda：汽水音乐，链接 soda.douyin.com。
- spotify：Spotify，链接 open.spotify.com / spotify.link。
- tidal：TIDAL，链接 tidal.com。

sources 返回别名。存在适配器不等于当前环境的搜索、下载、歌单都成功，以真实测试为准。未知分享短链接需确定归属，不猜测平台。

## 配置

外部 JSON 的 platforms 以平台 ID 为键。client 原样传给客户端构造函数，requests 传给 request_overrides，threads 是该平台内部线程数（默认 1）。无账号的有效配置示例：

```json
{
  "platforms": {
    "streetvoice": {
      "client": {"max_retries": 1},
      "threads": 1
    }
  }
}
```

type、work_dir、logger_handle、disable_print 由封装器管理；搜索数量来自 --limit。其余参数直接交给指定版本 musicdl；无效参数明确失败。脚本不管理登录，不自动读取浏览器 Cookie。

需要限制总运行时间时优先用 --timeout。requests.timeout 可用数值或表示连接/读取超时的 JSON 数组，但上游部分第三方解析方法自身已经传了 timeout，再覆盖可能触发重复关键字错误并使该解析路径失败；只对已确认兼容的客户端使用该覆盖项。封装器不静默删除或替换显式配置。

账号字段以安装版本客户端源码为准，通过独立环境定位 musicdl 包即可，无需原项目。

- 酷我、酷狗、网易云、QQ 等默认使用上游第三方解析与平台接口链。本人 Cookie 会影响分支选择，本封装不承诺严格隔离所有第三方请求。
- TIDAL 构造阶段要求 default_search_cookies / default_download_cookies / default_parse_cookies 至少一项为 SessionStorage 字段字典，字段由对应数据类定义。缺少时上游明确报错。
- Apple Music 包括普通 URL 和账号对应的 DownloadItem 两种路径；专用路径涉及 media-user-token、设备文件、FFmpeg 等条件。无配置不等于所有搜索路径不可用，以实际接口结果为准。
- Deezer 账号路径使用 arl；Joox 使用客户端定义的嵌套认证字典；Qobuz 使用其用户认证 Token。
- 平台专用音频对象保存在私有快照中，下载恢复后继续调用对应客户端，不强制转成普通 URL。

认证由用户在本地配置，不提供共享会员凭据。源码无法证明第三方服务背后的账号或音源。

## 状态

- 退出码 0：成功，或明确返回 no_downloadable_results。
- 退出码 1：部分成功、失败、超时或配置/状态错误；先读 JSON 再看每项结果。
- 退出码 2：命令参数错误，argparse 写入 stderr。

backend.log 是原始后端日志，process.log 记录进程异常。日志可能含临时授权信息，保留在本机私有状态目录。上游包含自己的重试、第三方解析链和部分跳过 TLS 验证的路径；本封装没有新增替代源或自动回退。
