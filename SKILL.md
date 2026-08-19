---
name: fashion-magazine-poster-generator
description: "Create original high-aesthetic fashion magazine covers, editorial posters, lookbooks, campaign pages, color boards, typography posters, invitations, runway announcements, and fragment-editorial social packages from a supplied reference image, a set of visual materials, or a brief. Analyze visible composition, whitespace, palette, typography, image strategy, model pose, expression, lighting, tone, material, content theme, asset hierarchy, and communication function. Use supplied references to recommend a fitting single style or a justified combination of styles; if no compatible recommendation exists, say so instead of forcing a blend. For image generation, first present style or combination recommendations and wait for the user's selection before generating; then produce a finished raster poster or copy-ready 即梦/Jimeng prompt. Includes a dedicated Y2K cyber-kawaii idol scrapbook / fan-zine collage family for maximalist idol posters. Use when the user asks to create, transform, vary, reverse-engineer, batch-generate, or editorially organize fashion posters, magazine covers, lookbook visuals, multi-image contact sheets, reference-photo prompts, or scattered social-content fragments."
---

# Fashion Magazine Poster Generator

Turn a supplied reference image or creative brief into an independently compelling fashion-editorial poster. Treat a reference as evidence and creative stimulus, never as a layer to copy. Preserve useful relationships—visual mass, negative space, palette hierarchy, type rhythm, image strategy, gesture, and light behavior—while inventing an original subject, wardrobe, text system, and communication purpose.

Use the image-generation capability for finished raster output. Do not display the internal generation prompt by default. If the user explicitly asks for a prompt, provide the compiled prompt after the image or instead of generating.

## Execution Contract

- For every request that may lead to image generation, use a mandatory two-stage interaction: **Stage A — style selection**, then **Stage B — generation**. Never call the image-generation capability during Stage A.
- In Stage A, inspect the reference or brief, then present a complete, numbered set of distinct style candidates before asking the user to choose. Include enough candidates to make the choice meaningful, normally 8–12 styles. For each candidate show: style name, core visual proposition, layout, palette, typography, image strategy, lighting, material, and the main difference from the other candidates.
- If the user names a desired style or supplies multiple reference images, run the Reference-Based Recommendation Gate before the general candidate menu. Recommend a single style or a primary-plus-secondary combination only when visible evidence supports it. If no compatible recommendation exists, state “没有合适的单风格或组合推荐” and explain the conflict briefly; do not invent a blend just to provide an answer.
- Tailor the candidate set to the supplied reference and requested function. Do not dump an unrelated generic list: explain in one short phrase why each candidate fits the reference.
- End Stage A with a direct selection request such as “请选择编号（可选 1 个，也可选 2 个让我融合）”. If the user has not selected a style, pause and do not generate an image or a final image-generation prompt.
- If the user explicitly says “直接生成”“随机选” or gives a style number/name, treat that as the selection and proceed to Stage B. If two styles are selected, define one as primary and one as a restrained secondary influence; do not merge all styles equally.
- In Stage B, restate the chosen style card briefly, compile the prompt, generate the image, and run Post-generation QA. If the user asks to change style, return to Stage A with a new candidate set instead of silently regenerating.
- If the user uploads one image and asks to make a poster, cover, or fashion visual, do not ask for a title unless exact copy is essential; ask for the style choice first.
- If the user asks for “another style,” inspect the latest output in the conversation, name the new style family internally, and change at least six visual dimensions before generating.
- If the user asks for a prompt, return one copy-ready prompt for the requested image model; do not substitute a long design lecture for the prompt.
- Treat “fashionable” as a concrete art direction: define silhouette, material, pose, type behavior, palette roles, lighting, and print or screen texture.
- If the user does not provide exact copy, generate fresh editorial text from visible subject features; never reuse example titles, fixed issue numbers, or a stock slogan as the default.

## Start Router

Resolve these four choices before designing:

1. **Output intent:** analysis only, creative direction, copy-ready prompt, one finished image, or a batch/series.
2. **Reference mode:** `visual-study` for abstract evidence only; `style-reference` for mood and material; `composition-reference` for layout logic; `likeness-preserve` when the user explicitly requests a permitted likeness; `edit-target` when changing the supplied image itself.
3. **Communication function and format:** cover, editorial opener, campaign, lookbook, invitation, or archive; default to 4:5 portrait unless the user specifies another ratio.
4. **Text mode:** short generated text, exact short text, or typography layer for later replacement.

If an image is attached and the user asks to make a poster, complete the style-selection gate after these choices and before image generation. Do not ask for information that can be reasonably inferred from the reference. If the user asks only for analysis or a prompt, do not generate an image; for a prompt request, still offer style candidates first when the prompt depends on a visual direction.

## Interactive Style Selection Gate

Use this gate whenever the user wants an image, poster, cover, visual variation, or a prompt whose visual direction has not already been fixed.

### Stage A — candidate menu

1. Inspect the reference and identify its visible anchors: subject or object, crop, gesture, dominant palette, light direction, texture, and communication function.
2. Select 8–12 style families from the library below, prioritizing clearly different visual systems rather than near-duplicates. Include at least one restrained option, one image-led option, one typography-led option, one collage or material option, and one experimental option when appropriate.
3. Build a numbered candidate card for every style. Use this compact format:

```text
编号｜风格名
命题：一句话说明这张海报要表达的视觉关系
版式：主体位置、留白、阅读路径
色彩：背景色、文字色、主视觉色、强调色
字体：字族关系、尺度、方向、图文关系
图像：主体处理、裁切、重复、叠层或摄影策略
光影/材质：光线方向、色温、颗粒、纸张或屏幕质感
适配原因：为什么适合当前参考图
与其他方案的主要差异：一句话
```

4. Make the options mutually legible: change the style family plus at least five dimensions across candidates, including layout, palette, typography, image strategy, lighting, material, and function. Do not present twelve names with nearly identical prompts.
5. Do not compile or reveal the final generation prompt at this stage. The cards are art-direction choices, not hidden chain-of-thought.

## Reference-Based Recommendation Gate

Use this gate when the user asks for a named style, supplies one or more style references, or asks whether several references can be combined.

1. Analyze each reference separately. Record only visible evidence: composition geometry, subject treatment, palette hierarchy, typography behavior, image strategy, lighting, material, density, and communication function.
2. Assign each reference a role: `style`, `layout`, `palette`, `typography`, `image strategy`, `lighting`, or `material`. Do not treat every reference as a full-style instruction.
3. Compare the requested style with the reference evidence. Recommend:
   - **Single-style recommendation** when one style explains the reference most coherently.
   - **Combination recommendation** when two references contribute non-conflicting roles; name one primary style and one secondary influence.
   - **No recommendation** when the references conflict in focal hierarchy, density, palette temperature, identity, or communication function and cannot be reconciled without making a generic collage.
4. Present the recommendation with: `推荐类型`, `主风格`, `辅助风格（如有）`, `各参考图承担的角色`, `保留的视觉证据`, `需要舍弃的冲突`, and `为什么适配`.
5. Do not force a combination. It is valid and preferred to say “没有合适的单风格或组合推荐” when the evidence does not support a coherent poster.
6. After the user confirms the recommendation, return to Stage B and compile the prompt. Until confirmation, do not generate an image or final generation prompt.

### Stage B — selected direction

After the user chooses, lock the chosen style family and its variation card. Then compile the final prompt in the prescribed order, include short dynamic text, generate the raster image, inspect it, and return the image with concise creative notes. Preserve the reference anchors but make the poster an original reinterpretation.

### Default candidate library

Use these as a starting library, then adapt them to the reference instead of repeating fixed recipes:

- Street editorial graphic
- Quiet luxury / restrained paper cover
- Retro French editorial
- Y2K digital youth
- Y2K cyber-kawaii idol scrapbook / fan-zine collage
- Gothic romantic
- Japanese minimal / quiet negative space
- Art-school collage / cut-paper research board
- Futuristic technical interface
- Sports couture / kinetic campaign
- Surreal color-block
- Documentary runway / flash archive
- Experimental typography-first

When the user asks for “所有风格”, list the complete relevant set, including any additional directions from `references/style-families.md`; do not reduce the menu to only three favorites.

### Dedicated family: Y2K Cyber-Kawaii Idol Scrapbook

Treat this as a standalone style family, not as an automatic blend of Y2K digital and art-school collage. Use it when the reference suggests idol fan-zine energy, maximalist scrapbook density, cute-deco symbols, many mini portraits, or a 2000s digital diary.

- **Signature:** one central glam portrait surrounded by many smaller portrait crops, styling records, stickers, star/heart/bow motifs, pixel icons, handwritten labels, and playful interface fragments.
- **Layout:** maximalist full-bleed scrapbook; central hero controls the hierarchy, peripheral fragments form a dense orbit, irregular frames and overlapping layers replace a regular grid, with little or no empty field.
- **Palette:** silver or white base, hot pink, cyan, lilac, candy blue, and one acid-lime or chrome accent; keep one dominant ink color so the density remains controlled.
- **Typography:** ornate bubble or curly display title, chrome or outlined lettering, mixed with tiny sans-serif labels, fan-zine captions, dates, member/style tags, and compact code-like marks.
- **Image strategy:** hero portrait plus contact-sheet mini portraits, cropped eyes/hair/garments, sticker-like cutouts, tiny outfit archives, and repeated evidence fragments; every fragment must guide the eye or establish idol/archive function.
- **Lighting and material:** direct flash, glossy facial highlights, cyan-pink reflected light, scanned magazine texture, sticker gloss, low-resolution digital artifacts, photocopy grain, and thin chrome or plastic overlays.
- **Function:** idol fan-zine cover, comeback moodboard, member profile archive, collectible poster, pop campaign, or playful visual diary.
- **Hard avoids:** uncontrolled sticker clutter, equal visual weight everywhere, unreadable long text, random logos, copied branding, chaotic neon, distorted faces, duplicated limbs, and generic “cute” decoration without a hierarchy.

## Fragment Editorial Router

Add a content-first route when the request contains several images, screenshots, objects, tickets, pets, notes, scattered thoughts, or a social publishing intention. Read `references/fragment-content-editor.md` and inventory the material before choosing the visual treatment.

- One reference image plus a single fashion poster request → use the normal fashion poster route.
- Several assets or a request to turn fragments into publishable content → choose one route: `F1` portrait editorial, `F2` material collage, `F3` original-image overprint, or `F4` multi-panel lookbook contact sheet.
- “一组成套的海报放在一张图上” / “成套海报” → use `F4`; define two to six independent panels inside one sheet, one shared series identity, and visibly varied panel compositions.
- “保留原图”“不要重画人物” → use `F3` and preserve the supplied image's identity, crop, and important visual facts.

Keep one editorial proposition across the package, but do not force every asset into the final composition. Default fashion posters remain 4:5; social fragment packages default to 3:4 unless the user specifies another ratio.

## Compact Project Brief

Maintain one internal brief for every output:

```text
function | format | reference_mode | style_family | primary_composition
subject/image_strategy | wardrobe/material | pose | expression/gaze
typography/text_mode | palette hierarchy | light/tone | material texture
recent exclusions | exact text, if any
```

Use the brief to prevent drift between the analysis, prompt, generated image, and final art-direction notes. For repeated or batch work, use `references/project-brief.json` as the field contract.

## Return

Return, in this order:

1. the generated raster image;
2. a concise Chinese explanation of the creative proposition;
3. concise art-direction notes covering reference anchors, composition, typography, color, image, pose, lighting, and variation choices.

State briefly that the reference image was used as a visual study by the image-generation service. Do not expose hidden chain-of-thought or internal analysis.

## Decision Priority

Resolve conflicts in this order:

1. Establish one specific editorial proposition and make it visible.
2. Match the poster's communication function to its information density.
3. Preserve the reference's semantic and structural nucleus without copying its identity.
4. Create one dominant focal point and a deliberate eye path.
5. Make layout, whitespace, image, typography, color, pose, light, and texture serve the proposition.
6. Build controlled variety so every new output is visibly different from recent outputs.
7. Keep text short enough for reliable generation and accurate enough for a usable poster.
8. Finish with a premium, tactile, art-directed editorial voice rather than generic commercial decoration.

Do not treat the task as a filter, style transfer, literal redraw, brand replica, or generic “luxury fashion” collage.

## Consent and Source Handling

- Treat an uploaded image plus a transformation or generation request as consent to use image generation; do not ask again.
- Use the reference for visual analysis only. Do not browse, share, or upload it elsewhere.
- Do not reproduce logos, exact brand marks, celebrity identity, exact magazine titles, watermarks, full article copy, or distinctive artwork.
- If the reference contains a person, design a new adult fashion subject unless the user explicitly requests likeness and has the right to use it.
- If the reference contains no person, translate pose and expression into garment movement, object direction, spatial tension, or material behavior.

## Build the Editorial Direction Card

Inspect the reference before composing. Resolve only visible evidence and executable design decisions:

- **Communication function:** cover, editorial opener, runway announcement, seasonal lookbook, campaign, manifesto, invitation, color board, retail launch, or archive index.
- **Semantic nucleus:** the smallest subject, garment, relationship, or event that gives the reference meaning.
- **Layout geometry:** portrait, square, or landscape; hero, split page, grid, full bleed, diagonal, vertical spine, inset, overlapping cutouts, or unequal mosaic.
- **Visual-weight map:** dominant mass, quiet field, brightest quadrant, darkest quadrant, detail-heavy area, reading entry, focal encounter, and quiet exit.
- **Whitespace plan:** where functional negative space sits and its approximate share; whitespace must support title, metadata, or breathing room.
- **Palette hierarchy:** paper/background, ink/text, main image color, one accent, temperature, value, chroma, and contrast. Do not write only “premium” or “high-end.”
- **Typography roles:** masthead, title, editorial deck, metadata, issue/date/location/number. Identify type behavior, not an unverified exact font name.
- **Image strategy:** close portrait, three-quarter portrait, full-body look, runway silhouette, city fashion, garment detail, hands/neck crop, two-model blocking, color board, still life, silhouette, collage, or illustration.
- **Wardrobe and material:** silhouette, cut, construction, surface, sheen, layering, accessories, and relation to the background.
- **Model action:** physical verb, torso direction, shoulder/hip line, hand placement, gait, lean, seated relationship, or interaction with garment/accessory.
- **Visible expression:** direct gaze, side glance, lowered eyes, raised brow, calm alertness, restrained half-smile, profile jaw tension, dreamy absorption, or neutral focus. Never claim to know inner emotion.
- **Light and tone:** main light direction, hard/soft quality, shadow edge, rim or reflected light, tonal temperature, and print or film feel.
- **Discard list:** clutter, redundant objects, long copy, unsupported symbols, brand cues, and anything that competes with the focal point.

Preserve two to four reference anchors. Change the rest with purpose; do not average all references into one generic result.

## Editorial Proposition Engine

Build the direction through this chain:

```text
visible reference fact → editorial function → artistic proposition → visual tension → formal embodiment → readable poster
```

Write one internal proposition that is specific to the reference and the requested output. Examples:

- a restrained portrait is interrupted by a vertical red signal that turns a quiet cover into a declaration;
- two silhouettes share one architectural field while remaining emotionally separate;
- a garment's rigid construction becomes the organizing grid of a seasonal lookbook;
- a model moving through shadow makes the campaign feel like a threshold rather than a product shot.

Choose one primary tension, with at most one subordinate tension:

- stillness / movement;
- intimacy / distance;
- softness / structure;
- visibility / concealment;
- warmth / coldness;
- human body / architecture;
- quiet luxury / graphic interruption;
- natural texture / synthetic gloss;
- order / asymmetry;
- presence / disappearance.

Embodify the tension through scale, crop, overlap, interval, color contrast, light direction, gesture, garment structure, and text–image interaction. Do not explain the tension with long copy.

## Reference-Respectful Reinterpretation

Allow:

- changing the subject, wardrobe, age-neutral styling, crop, scale, and placement;
- reorganizing the original spatial relationship;
- enlarging a garment detail or shrinking the figure to change power and attention;
- merging, splitting, repeating, or rhythmically compressing image fragments;
- deleting realistic background detail and retaining only structural traces;
- changing the palette while preserving its hierarchy or temperature logic;
- making the model walk, lean, turn, sit, adjust a cuff, hold fabric, or look away;
- translating non-figurative references into cloth movement, suspended accessories, folds, shadows, color fields, or object direction;
- using Chinese, English, bilingual text, numbers, or compact symbols when they serve the editorial purpose.

Every invented element must do at least one job: establish hierarchy, guide the eye, clarify function, balance weight, extend a gesture, strengthen material contrast, or make the communication more memorable. Remove elements that only make the poster look busy.

## Content-first Editorial Layer

Before writing the title, separate the visible surface fact from the underlying editorial proposition. The design should add a second layer of meaning instead of merely describing the image or listing the materials. For fragment requests, first inventory people, objects, scenes, visible text, time, emotion-as-visible-tone, visual strength, privacy risk, and usable crop; then keep, drop, and order the assets.

Generate 8–15 short title candidates internally from the visible signature, proposition, and publishing intent, then select one strongest title and one short deck. Do not output the full candidate list unless asked. Avoid hollow social phrases such as `记录美好生活`, `今天也要开心`, `生活需要仪式感`, `氛围感拉满`, and `治愈一切不开心`. Exact user-provided text always wins.

If the user requests humor, absurdity, or fragment editing, use one mechanism—serious report, archive/index, error naming, material personification, Chinese-English mismatch, or quiet observation—and keep it subordinate to the fashion concept. Do not pile up memes or jokes.

## Variation Director

Before each new image, create a private variation card. Change at least six dimensions from the most recent output; never repeat the same full combination.

### Style family

Choose one primary family and avoid the most recent family: street-editorial graphic; quiet luxury; retro French editorial; Y2K digital; Y2K cyber-kawaii idol scrapbook; gothic romantic; Japanese minimal; art-school collage; futuristic technical; sports couture; surreal color-block; documentary runway; or experimental typography-first. Give the family one visible signature instead of mixing all families into generic “fashion.”

### Diversity lock

Read recent outputs in the conversation before choosing the card. Track: style family, layout, palette, typography relation, image strategy, subject position, pose, expression, lighting, function, and material. Change the style family plus at least five other fields. Explicitly exclude the previous palette and dominant layout when the user asks for a visibly different style. If there is no previous output, choose a family deliberately and report it in the variation note.

### Layout

Choose one: asymmetric 12-column spread; split page with tall image panel and quiet text field; centered hero with cropped title; four-panel lookbook with one enlarged tile; diagonal stepping rhythm; full-bleed image with floating caption; top/bottom editorial bands; unequal mosaic on a baseline; left-heavy image with right whitespace; vertical type spine with low image strip; overlapping cutout figures; inset image inside a dominant paper field.

### Palette

Choose one hierarchy: cool gray monochrome; ivory, oatmeal, and near-black; burgundy, charcoal, and blush; terracotta, tobacco, and cream; cobalt, paper white, and acid-lime; olive, chalk white, and ochre; lilac, soft gray, and silver; faded orange, pink, and cream; bone black and champagne; teal, rust, and parchment; midnight blue, violet, and silver; tomato red, warm gray, and bone white.

### Typography relation

Choose one: high-contrast serif masthead plus narrow grotesk metadata; stacked condensed sans-serif; oversized serif initials cropped by the frame; italic serif title plus uppercase sans-serif notes; geometric sans-serif blocks plus hairline caption; vertical masthead on the outer edge; title behind the subject; lowercase editorial wordmark with widely tracked small caps; split headline across two columns; one type family differentiated only by scale and weight.

### Subject and image strategy

Choose one: close three-quarter portrait; full-body runway pose; seated side profile; city walk; wall lean; garment detail with hand; two models at different depths; architectural silhouette; color swatches and fabric; still life with accessory; cropped face/neck/hand; suspended garment or accessory; original fashion illustration.

### Model action

Choose one concrete verb: walk past camera; turn the torso away while returning the face; adjust a collar; pull a sleeve; touch a pendant; lean against a wall; shift weight into one hip; sit sideways with one hand on the knee; extend both arms to reveal the silhouette; look down while fastening an accessory; hold the garment open; let the coat or scarf move in wind.

### Expression and gaze

Choose one visible state: composed direct gaze; distant side glance; lowered eyes; slightly raised brow; calm alertness; minimal half-smile; serene neutrality; softened intense eye contact; dreamy absorption; profile jaw tension; gaze toward the reserved text field; gaze beyond the frame.

### Lighting and tone

Choose one: hard upper-left window rectangle; soft north-window daylight; narrow top spotlight; warm low side light; overcast diffusion; red/blue stage reflection; translucent backlight halo; single side key with negative fill; frontal flash; late-afternoon amber shadows; cool city neon reflection; flat color-block studio light.

### Function and material

Choose one function: cover; runway announcement; seasonal lookbook; color direction board; editorial portrait opener; capsule campaign; fashion-week invitation; manifesto; retail launch; archive index.

Choose one material emphasis: matte uncoated paper; fine film grain; subtle screen-print misregistration; scanned paper fiber; vellum overlay; torn paper edge; clean glossy poster stock; restrained halftone dots; dry ink bite.

## Composition Director

Choose a composition family from the reference geometry, then adjust it through visual weight rather than habit:

- **Hero with information rail:** one dominant subject, 20–40% clear space for metadata.
- **Editorial split:** image panel on one side, quiet text field on the other; use the seam as a design event.
- **Lookbook rhythm:** four to eight image cells with unequal scale, consistent baseline, and numbered labels.
- **Type-first poster:** title carries the visual mass; the model appears as a partial crop or silhouette.
- **Diagonal movement:** image, title, and rules step through the frame along a body or garment direction.
- **Color board:** hero detail, swatches, material samples, and short labels form a coherent research page.
- **Vertical spine:** a single vertical title or metadata column counterbalances a low or wide image.
- **Archive mosaic:** unequal image tiles, numbering, and compact notes create a catalog-like reading path.

Apply figure–ground clarity, asymmetric balance, dominant–subordinate hierarchy, optical centering, scale contrast, directional breathing room, and a clear eye path. Keep one focal point. Do not split the page into equal blocks unless the reference clearly requires it.

### Primary composition rule

Choose exactly one primary composition model and at most one supporting model. Do not combine a type-first poster, full mosaic, multiple cutouts, and a color board as equal priorities. One level-one visual core must control the reading order; every other element is subordinate evidence.

## Typography Director

Use typography as an active editorial material, not a caption pasted on afterward.

- Mix Chinese, English, and numbers when that improves rhythm or function; bilingual text is allowed.
- Use one or two type families by default, but vary scale, width, weight, tracking, direction, overlap, crop, and alignment to create richness.
- Allow the title to be oversized, cropped, behind the model, over the garment, aligned to an edge, divided across columns, or rotated along a spine.
- Use only short, image-model-friendly text: masthead, title, season, date, issue number, location, collection code, section label, or a few look numbers.
- Never depend on generated long paragraphs for legibility. Recommend exact copy be placed later in a layout tool.
- If typography is the main subject, let the image support the type rather than forcing a large portrait into the frame.

### Dynamic editorial text

When exact copy is not supplied, derive the text from visible evidence rather than from a fixed title library:

1. Extract three to five visible signature features: apparent age range, facial texture, gaze, posture, gesture, garment silhouette, fabric, accessory, background material, light quality, and color temperature.
2. Convert those features into one editorial proposition, such as restraint, weathered elegance, structural tension, tactile memory, quiet defiance, or synthetic softness. Describe what is visible; do not invent biography or hidden psychology.
3. Generate a fresh text set for this image: a 1–4 word main title, a 2–7 word short deck, and 1–3 compact metadata labels.
4. Mix Chinese and English only when it improves visual rhythm. Let the visible signature decide whether the text feels restrained, severe, poetic, technical, archival, or experimental.
5. Compare against recent outputs and exclude repeated titles, repeated slogans, and repeated issue numbers. Do not use examples such as `FORM / MEMORY`, `NOCTURNE`, `FUTURE SKIN`, `ISSUE 08`, or `NEW FORM` unless the user explicitly provides them.

Full naming formulas and examples are in `references/editorial-text-system.md`; examples demonstrate the method and are not default copy.

## Generation Mode

Choose one mode before compiling the prompt:

- **One-shot poster:** generate image, short title, metadata, and graphic system together. Use for fast ideation and casual variations.
- **Layered editorial:** generate a clean image/background layer first, then a separate typography or graphic layer, then combine them with the chosen poster grid. Use when exact copy, reusable type treatment, a series, or strong text-image interaction matters.

Do not claim to have created editable layers unless separate image files were actually produced. If the image service cannot preserve exact typography, keep text short and tell the user that final copy should be replaced in a layout tool.

## Color and Light Director

Resolve color as a hierarchy, not a keyword list:

1. background or paper tone;
2. ink/text tone;
3. main wardrobe or image tone;
4. one primary accent, with at most one restrained echo.

State each color's role, area, adjacency, value contrast, and material form. Use one light direction and make shadows support silhouette, fabric, and reading order. A color or lighting effect without a compositional job is decoration and should be removed.

## Prompt Compiler

Compile the internal direction into a concise image-generation prompt in this order:

```text
function → format → layout → subject/wardrobe → physical action → expression/gaze → typography → palette → lighting → tone/texture → short-text limits → hard avoids
```

Use decisive, imageable language. Include one focal subject, intentional negative space and its location, concrete garment silhouette and material, concrete physical action and visible expression, type roles and placement, background/ink/hero/accent colors, one coherent light source, print or material texture, bilingual short text only when useful, and no-copy/anatomy safeguards.

For Image 2 or natural-language image models, write natural Chinese or English. For other models, write model-neutral language unless the user explicitly requests syntax. Do not include weights or model flags in the default prompt.

### 即梦 / copy-ready prompt mode

When the user mentions 即梦/Jimeng or asks to copy the prompt, write one natural Chinese prompt in this order: reference role → function and format → layout → subject and wardrobe → physical action → expression and gaze → typography and exact short text → palette → lighting → material and texture → hard avoids. Keep the prompt compact enough to paste into one field. Use short quoted text only; never rely on long Chinese paragraphs or invented article copy. If the user asks for an actual image rather than prompt text, use the image-generation capability and keep the prompt internal.

## Post-generation QA

Inspect the result against the direction card before returning it. Check: one focal point; clear eye path; intentional whitespace; visible difference from the latest output; realistic hands and anatomy; coherent light direction; readable short text; no copied logos or watermarks; and a concrete fashion proposition. If one important item fails, make one targeted regeneration with only that correction, then return the better result and note the changed field.

For layered work, additionally check that the background, typography, and composite preserve the same crop, safe area, scale, and visual hierarchy. Use `references/quality-control.md` for the full gate.

## Generation Workflow

1. Inspect the supplied reference image or read the brief.
2. Run the Start Router and create the Compact Project Brief.
3. Build the Editorial Direction Card and identify the visible reference anchors.
4. If the user named a style or supplied multiple references, run the Reference-Based Recommendation Gate; pause for confirmation unless the user already selected the recommendation.
5. If no recommendation gate is needed, stop at Stage A and present the complete numbered style menu; wait for the user's selection.
6. After selection or confirmation, write one editorial proposition and one primary tension.
7. Preserve two to four reference anchors and create a discard list.
8. Lock one primary composition model and one selected style family; if two styles were selected, keep one primary and one secondary influence.
9. Select a private variation card; change the style family plus at least five other dimensions from recent output.
10. Choose one-shot or layered generation mode.
11. If fragment mode is active, inventory the assets, separate surface fact from underlying proposition, choose F1/F2/F3/F4, and decide what to keep, drop, order, and crop.
12. Generate the dynamic editorial text from the visible signature and content proposition unless exact copy is supplied.
13. Design the subject, wardrobe, action, gaze, expression, palette, typography, lighting, material, and any panel-to-panel series variation.
14. Compile the final prompt in the prescribed order.
15. Generate the finished raster image using the supplied reference according to the selected reference mode and generation mode.
16. Run the Post-generation QA; for fragment mode also check theme unity, asset selection, privacy, original-image protection, and mobile thumbnail reading. If needed, make one targeted regeneration rather than changing the entire direction.
17. Return the image, concise Chinese creative idea, and art-direction notes. For a fragment/social package, use the package fields in `references/fragment-content-editor.md`. Include the generated text set in the typography note, but do not reveal the full prompt unless explicitly requested.

For a folder of references, analyze each image separately first. Keep one row per image with `reference`, `reference_mode`, `style_family`, `layout`, `palette`, `font`, `subject_position`, `pose`, `expression`, `lighting`, `function`, `image_strategy`, and `recent_exclusions`; then rotate the style family plus at least five other dimensions between successive prompts. Use the bundled `scripts/generate_reverse_prompts.py` for deterministic folder-wide prompt extraction and read `references/prompt-rotation.md` when designing a series.

## Hard Avoids

Avoid copied logos, brand marks, exact magazine titles, celebrity identity, watermarks, long gibberish text, random letters, incorrect Chinese, hollow social phrases, merely describing every asset, forcing every asset into a collage, multiple competing themes, too many type families, weak hierarchy, no negative space, plastic skin, oversmoothing, generic stock-photo poses, stiff standing, distorted anatomy, extra limbs, duplicated people, awkward hands, broken garment construction, inconsistent shadows, muddy colors, competing focal points, evenly distributed color, decorative clutter, arbitrary grids or stickers, uncontrolled collage, privacy leaks from screenshots or documents, cheap 3D, glossy mockups, neon overload, cinematic letterboxing, compression artifacts, and unreadable microtype.

## Output Format

```markdown
**生成图**

![Fashion editorial poster](absolute-image-path-or-rendered-image)

**创作想法**

[用简洁中文说明本次的编辑命题、视觉张力、主体动作、文字与图像关系，以及参考图如何被原创转译。不要描述隐藏提示词。]

**艺术指导**

- Reference anchors: [保留的两到四个可见关系]
- Function: [传播功能与信息密度]
- Composition: [版式、主体位置、留白、阅读路径]
- Image: [主体、服装、材质、场景、镜头策略]
- Pose and expression: [动作、视线、神态]
- Typography: [中文/英文/混合文字、字形角色、尺度、方向、图文交互]
- Color: [底色、墨色、主视觉色、强调色、色调]
- Light: [光线方向、阴影、色温、反射]
- Variation: [本次至少改变的六个维度]
```

If the image-generation service returns no local path, show the image normally and still include the creative idea and notes. If the user explicitly requests prompt text, add the Chinese prompt, English prompt, and negative prompt after the notes.

## Resource Index

Read only the resources needed for the current request:

- `references/decision-tree.md`: task routing, reference modes, and generation-mode choice.
- `references/style-families.md`: distinct fashion directions and their visual signatures.
- `references/prompt-rotation.md`: series variation ledger and dimension rotation.
- `references/editorial-text-system.md`: visible-feature extraction and dynamic title/deck/metadata formulas.
- `references/jimeng-prompt-recipes.md`: compact 即梦 prompts, dynamic-text rules, exact-text rules, and negative prompts.
- `references/layered-poster-workflow.md`: background, typography, grid, and composite workflow.
- `references/quality-control.md`: pre-generation and post-generation checks.
- `references/fragment-content-editor.md`: content-first inventory, F1–F4 routes, dynamic title selection, social package, and iteration commands.
- `references/project-brief.json`: repeatable field contract for single or batch work.
- `references/output-template.md`: concise Chinese result format.
