# 即梦 Prompt Recipes

## One-shot recipe

```text
使用上传的参考图作为[visual-study/style-reference/composition-reference]，先提取人物可见的年龄质感、面部纹理、视线、姿态、服装廓形、面料、配饰、背景材质和光线特征，再把这些特征转化为一个原创编辑命题。创作一张原创[功能]，画幅[比例]。采用[风格族]和[主构成模型]：主体位于[位置]，人物穿着[服装与材质]，正在[具体动作]，视线[方向]，神态[可见状态]。背景为[场景/纸张/图形]，文字区位于[位置]，使用[字体关系]。根据人物的可见风格特征动态生成一组全新的短文字：主标题1—4个词，副标题2—7个词，1—3个期号/栏目/材质标签；不要套用固定标题。色彩层级为[底色]、[文字色]、[主体色]和[强调色]；光线来自[方向]，阴影[特征]，加入[材质/印刷质感]。画面有一个明确焦点、清晰阅读路径和有功能的留白。避免复制参考图、品牌标志、水印、长段落、乱码、塑料皮肤、僵硬姿势、畸形手部和杂乱装饰。
```

## Exact-text rules

- Keep visible text to a masthead, title, issue/date, and one short label.
- When no exact copy is supplied, derive the title, deck, and metadata from the image's visible subject signature; do not reuse a template title.
- Put exact text in quotation marks and ask for verbatim rendering.
- For long Chinese copy, generate the image without it and replace the copy later in a layout tool.
- Do not add fake brand names, real magazine titles, awards, or logos.

## Style-variation recipe

State the latest output's family, palette, layout, pose, expression, lighting, and material internally. Choose a new family and explicitly exclude the latest dominant palette and layout. Change at least five more fields before writing the prompt.

## Negative prompt

```text
避免复制原图版式、品牌Logo、真实杂志名称、水印、长段落文字、乱码、错误中文、字体过多、主体平均分散、无意义装饰、塑料皮肤、过度磨皮、僵硬站姿、畸形手部、多余手指、重复人物、服装结构错误、光线冲突、色彩浑浊、廉价3D和普通证件照构图。
```
