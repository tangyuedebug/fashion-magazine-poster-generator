# Fashion Poster Decision Tree

## 1. Route the request

- **分析**：describe visible evidence and reverse-engineer the reference; do not generate.
- **方案**：return editorial proposition, composition, type, color, pose, lighting, and generation plan.
- **提示词**：return one copy-ready prompt for the requested model; keep the prompt compact.
- **生成**：use the image-generation capability and return the finished raster image first.
- **批量/系列**：create one brief per reference and rotate style family plus at least five other fields.
- **碎片内容/社交发布**：when several photos, screenshots, objects, tickets, notes, or a publishing request are supplied, read `fragment-content-editor.md`, inventory the assets, and choose F1/F2/F3/F4 before writing copy.

## 2. Route the reference

- `visual-study`: abstract composition, palette, density, gesture, and light; do not preserve identity.
- `style-reference`: use material, tone, and image strategy; redesign subject and layout.
- `composition-reference`: use visual weight, whitespace, and reading path; replace image content.
- `likeness-preserve`: use only when the user explicitly requests a permitted likeness; preserve face-related invariants carefully.
- `edit-target`: modify the supplied image itself; list what must remain unchanged.

## 3. Route the generation mode

- Use **one-shot** for quick variations, mood exploration, and short text.
- Use **layered** for exact copy, reusable typography, series consistency, or strong graphic interaction.

## 4. Route the format

Default to 4:5 portrait for a magazine poster. Use 3:4 for social publishing, 9:16 for story-like covers, and another ratio only when the user specifies it.

For “a set of posters in one image,” use F4: a 2–6 panel contact sheet or lookbook board with one shared series identity and varied panel layouts. Do not reduce it to repeated portraits in equal boxes.

## 5. Route fragment templates

- one person is the focus → **F1 portrait editorial**;
- several fragments or objects are the focus → **F2 material collage**;
- one original image must remain intact → **F3 image with overprint**;
- several finished poster panels must coexist in one image → **F4 lookbook contact sheet**.

Before composing F1–F4, write one surface fact and one underlying proposition. Keep, drop, order, and crop assets according to that proposition.

## 6. Resolve missing information

Infer ordinary details from the image or brief. Ask only when the missing detail changes the deliverable materially, such as exact title text, required likeness, or final aspect ratio.
