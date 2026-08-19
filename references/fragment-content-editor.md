# Fragment Content Editorial Layer

Use this layer when the user provides several photos, screenshots, objects, tickets, pets, notes, or scattered thoughts and wants them turned into a coherent fashion poster, lookbook, contact sheet, or social publishing package. The goal is to find one editorial idea and give the material a second meaning; do not merely label every image.

## Editorial principles

1. Inventory the material before writing copy or styling it.
2. Find one moment worth amplifying, then state the surface fact and the underlying proposition separately.
3. Keep one core idea. Drop weak, redundant, private, or visually noisy assets.
4. Use fashion language—silhouette, material, gesture, light, type, archive, runway, attitude—rather than generic social-media decoration.
5. Humor, absurdity, or displacement is optional. Use it only when the user asks for a playful or fragmented tone, and keep it subordinate to the visual proposition.
6. Protect people, original photographs, private text, addresses, tickets, screens, logos, and other identifying details.

## Material inventory

For each asset, note:

```text
asset | type | subject | visible text | time/scene | mood or visual fact
visual strength | privacy risk | usable crop | keep / drop / optional
```

Do not infer biography, profession, nationality, relationship, or hidden psychology from appearance. Describe only what can be seen or what the user supplied.

## Route templates

Choose one route. Keep the fashion poster system as the default when the user gives one image and asks for a single poster.

- **F1 人像主角版 / portrait editorial**: one person is the absolute protagonist. Use a strong crop, one dynamic title, sparse metadata, and a clear fashion attitude. Adapt the portrait-centered route when the user focuses on “我” or one model.
- **F2 素材拼贴版 / material collage**: several images, objects, screenshots, pets, tickets, or details become an archive, index, report, manual, or research board. Use unequal scale, numbered labels, and one reading path; do not force every asset into the grid.
- **F3 原图压字版 / image with overprint**: preserve one emotionally strong original image and change its interpretation with one title, a small deck, and restrained metadata. Do not redraw the person when the user asks to keep the original.
- **F4 成套 lookbook 版 / contact sheet**: place two to six related poster panels in one image. Keep a shared series identity, but vary pose, crop, layout, palette accent, and title rhythm across panels. This is the preferred route when the user asks for “一组成套海报放在一张图上”.

Quick decision:

```text
one person as the focus → F1
several fragments or objects as the focus → F2
one image's feeling as the focus → F3
multiple finished poster panels in one image → F4
```

For F4, define the panel count, panel order, shared masthead or collection code, and each panel's independent composition before generating. The sheet must read as a designed series, not four copies squeezed into a collage.

## Content-first title method

First write one sentence in this form:

```text
surface fact: what is visibly present
underlying proposition: what new editorial meaning the design adds
```

Generate 8–15 short title candidates internally from the visible signature, underlying proposition, and publishing intent. Select one strongest title and one short deck. The title should add a second layer of meaning, not repeat “a woman in a white shirt”, “daily life”, or a list of the assets.

Possible publishing intents include self-expression, life fragments, fashion observation, archive/index, pet personification, work survival, mood record, light commemoration, campaign, lookbook, or invitation. Use a serious report, archive label, material naming, Chinese-English mismatch, or quiet observation only when it fits the chosen intent.

Avoid hollow phrases such as `记录美好生活`, `今天也要开心`, `生活需要仪式感`, `氛围感拉满`, and `治愈一切不开心`. Exact user-provided text always overrides generated copy.

## Fragment output package

When the request is a social or multi-asset package, return:

1. **内容核心**：一句话主题，包含 surface fact 与 underlying proposition。
2. **推荐模板**：F1/F2/F3/F4 及选择理由。
3. **主标题**：最终标题；不要默认输出全部候选。
4. **辅助文字**：3–8 条短 deck、标签、编号或元信息。
5. **图片使用**：hero、保留、删除、顺序、裁切与原图保护要求。
6. **朋友圈正文（如需要）**：自然、具体、15–60 字，不复述图片清单。
7. **视觉简报**：画幅、版式、主体、字体、色彩、光影、材质和手机缩略图阅读方式。
8. **发布前检查**：隐私、版权/品牌、文字、焦点、主题、原图保护和移动端可读性。

For a pure fashion poster, keep the normal output contract and use only the relevant parts of this package. Do not add social copy unless requested or clearly implied by the publishing context.

## Iteration commands

Interpret short follow-ups as controlled edits to the same brief:

- “更冷一点” → lower warmth and emotional language; preserve the subject and change light/palette only.
- “减少文字” → keep one title and one metadata line; preserve the composition.
- “换成拼贴” → route to F2 and re-inventory usable assets.
- “保留原图，不要重画人物” → route to F3 and protect identity, crop, and visible details.
- “更适合朋友圈首图” → use 3:4, stronger thumbnail hierarchy, fewer micro-details, and one immediate title.
- “更潮流 / 更 fashion” → keep one clear proposition but increase silhouette, type rhythm, material contrast, and graphic confidence rather than adding random stickers.
