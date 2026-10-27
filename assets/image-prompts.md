# 视觉素材与生成提示词

制作日期：2026-10-27。使用内置 image_gen 工具生成，未使用 API/CLI 回退。图片用于项目介绍，是品牌插画，不是软件界面截图。

- `readme-cover.png`：横向 README 封面。
- `promo-poster.png`：适合单独分享的竖版宣传海报。

两张图采用一致的黑胶唱片、音频波形与下载符号，配色为石墨黑、暖白与荧光绿。文案中的“17 个平台适配”表示适配范围，不代表所有平台在任何条件下都可下载。实际可用性见项目测试记录。

## 共用提示词

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
