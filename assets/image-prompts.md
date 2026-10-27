# 视觉素材与生成提示词

制作日期：2026-10-27。使用内置 image_gen 工具生成，未使用 API/CLI 回退。图片用于项目介绍，是品牌插画，不是软件界面截图。

- `readme-cover.png`：横向 README 封面。
- `promo-poster.png`：适合单独分享的竖版宣传海报。

两张图采用一致的黑胶唱片、音频波形与下载符号，配色为石墨黑、暖白与荧光绿。文案中的“17 个平台适配”表示适配范围，不代表所有平台在任何条件下都可下载。实际可用性见项目测试记录。

## 当前封面：面向 Agent 的介绍

使用内置 image_gen 编辑上一版封面：将工具名称与技术说明替换为“让 Agent 直接搜索与下载音乐”，把“17 个平台适配”移至底部图标区域。保留完整黑胶、音频波形、下载符号及全部平台图标与名称。平台图标沿用 AI 重绘版。

参考图：`readme-cover.png`（完整黑胶与平台图标版）。

```text
Use case: text-localization / precise marketing image edit.
Input image is the EDIT TARGET, the current music-download README cover. Make a surgical typography and layout refinement, preserving the 2:1 horizontal format and almost all visual identity and artwork.
Preserve the exact large title "music-download", the headline "一句指令，让音乐落地。", warm ivory background, realistic black vinyl record with acid-lime label, glowing waveform and download arrow. Preserve the completely visible unobstructed record outer rim, its position and photographic quality. Preserve ALL 17 existing platform icons and their exact names, in the same two-row order. Do not redraw or redesign the icons unnecessarily.

REQUESTED CHANGES:
1. Remove both left-hand small lines "Claude Code / Codex" and "17 个平台适配 · JSON CLI" completely.
2. In their place, use a single clear restrained supporting sentence, verbatim: "让 Agent 直接搜索与下载音乐". Make it smaller than the headline, near-black, comfortably spaced, aligned with the large title. Do not include names of specific agents or technical words such as JSON or CLI anywhere in the image.
3. Move the phrase "17 个平台适配" to the bottom platform directory, as a compact but legible left-aligned section heading immediately below the thin divider and above the two icon rows. Add enough vertical space to fit it cleanly; slightly increase canvas height if necessary, maintaining a horizontal banner. The heading must not touch any icon or the vinyl; retain generous breathing room.
4. Keep all existing platform labels precisely:
row 1: 酷我, 酷狗, 网易云, QQ音乐, 咪咕, 千千, 汽水, 5sing, Apple Music
row 2: Deezer, Jamendo, Joox, Qobuz, SoundCloud, StreetVoice, Spotify, TIDAL
Every name appears exactly once. The bottom section is separate from the hero, with no overlap. Keep recognizable colorful small icons and near-black text, on plain ivory without cards. No changes to platform count.

Final artwork only. No red annotation box, no screenshot borders, no browser UI, no watermark, no new promotional claims. Target a cleaner, more universal Agent-facing README cover.
```

## 历史封面：完整黑胶与平台图标

使用内置 image_gen 编辑平台名单版封面。将黑胶与平台目录分区，完整显示唱片外缘，底部两行展示全部 17 个平台的图标与名称。平台图标为 AI 重绘，并非从官方矢量源文件直接导入。

参考图：`readme-cover.png`（平台名单版）。宣传海报沿用上一版。

```text
Use case: compositing / ads-marketing.
Edit target: the supplied music-download banner. Recompose it into a polished horizontal GitHub README cover, about 2:1 aspect ratio, high resolution. Preserve the warm ivory, rich black and acid-lime identity, photographic vinyl groove detail, confident black typography, and the concept of music waveform flowing into a download arrow.

PRIMARY FIX: The vinyl must be completely visible as a circular object, with its entire outer rim inside the image and generous clear space around it. No text, footer, translucent sheet, platform list, labels or divider can cover any part of the record. Give the top hero its own roughly 70% height, and the platform directory its own roughly 30% height BELOW the record, separated by a thin quiet rule and spacious margin. The record, its soft studio shadow and waveform must end above this footer.

TOP HERO: Left half is typography only, right half is a single black vinyl record with a lime center, glossy grooves, and a delicate luminous lime waveform ending in a download arrow to the right. Keep the whole record and arrow comfortably within the right half, and away from every letter. Use a full, near-front-on circular record, not a giant cropped disc. On left render exactly:
"music-download" as the bold primary wordmark on one line.
"一句指令，让音乐落地。" as the secondary Chinese line.
"Claude Code / Codex"
"17 个平台适配 · JSON CLI"
Large but restrained typography. Plenty of breathing room.

PLATFORM FOOTER: Replace the current dense text-only platform lists with a clean evenly spaced directory of small recognizable platform brand/app icons PLUS their short names. Two horizontal rows, 9 items in first row and 8 items in second row, second row visually balanced. Each item is a recognizable small brand symbol above or beside its exact name, on the plain ivory surface. Use original brand colors only as restrained small accents in the symbols, keep labels near-black. No rounded cards, no panels, no sticker clutter, no pill backgrounds. Icons must help recognition; keep names because obscure platform icons alone are ambiguous. Every platform appears exactly once. Exact order:
row 1: 酷我, 酷狗, 网易云, QQ音乐, 咪咕, 千千, 汽水, 5sing, Apple Music
row 2: Deezer, Jamendo, Joox, Qobuz, SoundCloud, StreetVoice, Spotify, TIDAL
Use familiar recognizable platform marks (e.g. red Netease music spiral, QQ Music multicolor note, Apple Music note, Spotify three arcs, SoundCloud cloud waveform, TIDAL diamond cluster). Keep all 17 names legible, including Apple Music and SoundCloud, and don't replace any name with just a symbol.

Final artwork only, edge to edge. No webpage screenshot frame, no browser UI, no watermark. No extra slogans, no claim that every track can be downloaded. Highest priority: completely unobstructed vinyl, disciplined separation of hero and platform footer, accurate exact text and complete 17-item directory.
```

## 平台名单版修订

本次使用内置 image_gen 编辑两张原图，在封面和宣传海报上直接加入全部 17 个平台名称。以下为提交的完整修订提示词，参考图分别为仓库中的原版封面和海报。

### 封面

参考图：`readme-cover.png`（首版）。

```text
Use case: text-localization / precise marketing image edit. Edit the provided existing music-download artwork. Preserve the original visual identity: graphite-black vinyl record, luminous acid-lime center and audio waveform, warm ivory background, refined editorial typography. Preserve the exact project name "music-download", original Chinese headline, "Claude Code / Codex", and the wording "17 个平台适配". The single requested change is to clearly show the FULL list of all 17 platform names in the artwork. The names are plain typography, not logos, and must each appear exactly once, with exact spelling and Chinese characters. List (three intentional rows):
酷我 · 酷狗 · 网易云 · QQ音乐 · 咪咕 · 千千 · 汽水 · 5sing
Apple Music · Deezer · Jamendo · Joox · Qobuz
SoundCloud · StreetVoice · Spotify · TIDAL
Do not omit, duplicate, replace, misspell or invent any platform. Do not say all platforms are always available or add membership/free/lossless guarantees. Typeset the list with strong contrast, generous enough line spacing, and large readable text, especially at phone size. Do not cover the list with the record, waveform or any other object. Slightly adjust scale and spacing to fit the new information while preserving the premium original composition. No fake screenshots or QR codes. Target: existing wide README cover. Keep it landscape. Preserve the left large title "music-download" and tagline "一句指令，让音乐落地。" and the sculptural vinyl on the right. Add an integrated warm-ivory footer region across the lower portion of the banner for the three platform rows. It is acceptable to give the banner slightly more height and move the disc upward so ALL names remain legible. Make the platform list a real intentional part of the graphic, not a sticker, and do not use microprint. Group it directly with "17 个平台适配". Keep the black/ivory/lime color palette and high-end audio aesthetic.
```

### 宣传海报

参考图：`promo-poster.png`（首版）。

```text
Use case: text-localization / precise marketing image edit. Edit the provided existing music-download artwork. Preserve the original visual identity: graphite-black vinyl record, luminous acid-lime center and audio waveform, warm ivory background, refined editorial typography. Preserve the exact project name "music-download", original Chinese headline, "Claude Code / Codex", and the wording "17 个平台适配". The single requested change is to clearly show the FULL list of all 17 platform names in the artwork. The names are plain typography, not logos, and must each appear exactly once, with exact spelling and Chinese characters. List (three intentional rows):
酷我 · 酷狗 · 网易云 · QQ音乐 · 咪咕 · 千千 · 汽水 · 5sing
Apple Music · Deezer · Jamendo · Joox · Qobuz
SoundCloud · StreetVoice · Spotify · TIDAL
Do not omit, duplicate, replace, misspell or invent any platform. Do not say all platforms are always available or add membership/free/lossless guarantees. Typeset the list with strong contrast, generous enough line spacing, and large readable text, especially at phone size. Do not cover the list with the record, waveform or any other object. Slightly adjust scale and spacing to fit the new information while preserving the premium original composition. No fake screenshots or QR codes. Target: existing vertical promotional poster. Preserve the top title "music-download", headline "搜歌、选曲、下载。", supporting line "交给你的 Agent。", and exact footer URL "github.com/ln2146/music-download". Rebalance the lower ivory area to add the three platform rows under "17 个平台适配" and above "Claude Code / Codex" and the GitHub URL. Reduce the central disc and waveform modestly or increase the ivory footer area to give the names real space. Keep a portrait poster composition with large readable type, clear margins and clean separation between platform rows. Do not compress the 17 names into a tiny line.
```

## 首版共用提示词

以下共用文本分别与后面的对应图片提示词拼接后提交：

```text
Use case: ads-marketing. Create an exceptionally polished original brand visual for the real open GitHub project music-download, a standalone agent skill for music search and download using musicdl, compatible with Claude Code and Codex. Art direction: editorial Swiss typography meets premium audio equipment. Near-black graphite #10120F, warm off-white #F3F1E7, vivid acid lime #C6FF4A; no purple or blue gradient. Physical tactile brushed-metal vinyl record / audio waveform as the central conceptual object, subtle studio lighting, crisp deliberate whitespace and strong visual hierarchy. Original design, no imitation corporate logos, no fake product screenshot, no QR codes, no false promises such as unlimited free downloads or all platforms always available. All text must be precisely spelled and clearly readable. This is a visual identity illustration, not a screenshot.
```

## README 封面

```text
Asset type: GitHub README cover banner, very wide horizontal 2.6:1 composition, high resolution. Dominant title on the left exactly "music-download" with excellent typography and no line break inside the name. Directly beneath it, Chinese tagline exactly "一句指令，让音乐落地。" Below in small legible lettering "Claude Code / Codex" and "17 个平台适配 · JSON CLI". Right half features a stunning oversized sculptural charcoal vinyl disc with a lime circular center and a delicate luminous waveform drawn as a single continuous route toward a minimal download arrow, on warm cream negative space. The image should feel like a contemporary record sleeve designed by an elite independent design studio. Calm, useful, technical and musical. Keep generous margins for GitHub mobile viewing. Use only the exact specified text, no other labels or extra small print.
```

## 竖版宣传海报

```text
Asset type: shareable vertical promotional poster, portrait 3:4 composition, high resolution, Chinese audience. Large brand title exactly "music-download" across the upper portion, black background top, warm ivory lower area with purposeful asymmetric typographic grid. Main Chinese headline exactly "搜歌、选曲、下载。" on its own prominent line, supporting line exactly "交给你的 Agent。" Central artwork: an oversized elegant black vinyl disc with an acid-lime center, luminous lime audio waveform emerging from the disc and resolving into a subtle outlined download icon, beautifully lit metallic details, sophisticated depth. A single compact row near the bottom reads exactly "17 个平台适配". Below it exactly "Claude Code / Codex". Footer clearly reads exactly "github.com/ln2146/music-download". The name and URL must be correct. Keep all text large enough to read on a phone, no dense cards, no mock chat bubbles, no extra feature claims, no platform brand logos. This must look like a polished music technology release poster, not generic AI art.
```
