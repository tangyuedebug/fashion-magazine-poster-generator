# Dynamic Editorial Text System

Generate poster copy from the visible style signature of the supplied image. Do not start from a fixed magazine-title list.

For fragment or social requests, also derive the text from the underlying editorial proposition. First state the surface fact and the second meaning added by the design; the title must shift the reading rather than enumerate the images.

## Extract the signature

Choose three to five observable features:

- age presence: youthful, mature, weathered, ageless, or deliberately ambiguous;
- face and gaze: direct, distant, lowered, alert, serene, severe, curious;
- gesture and posture: upright, leaning, turning, adjusting, holding, walking, seated;
- wardrobe and material: tailoring, linen, velvet, nylon, knit, denim, leather, metallic, transparent;
- environment and light: rust wall, paper field, concrete, curtain, daylight, flash, rim light, shadow;
- visual temperature: warm, cool, muted, high-contrast, soft, raw, polished.

Do not infer biography, profession, nationality, private history, or hidden emotion from appearance.

## Convert features into language

Use this chain:

```text
visible feature → material or action → editorial tension → short title
```

Examples of the method, not fixed copy:

- weathered face + wool texture → time as material → `AGE / GRAIN`;
- direct gaze + rigid tailoring → calm resistance → `STEADY CUT`;
- lowered gaze + translucent fabric → presence / disappearance → `SOFT EVIDENCE`;
- turned torso + hard light → body / structure → `ANGLE OF FORM`;
- linen + diffused light → quiet tactility → `OPEN WEAVE`.

## Text set

Create three levels:

1. **Main title:** 1–4 words; name the visible proposition, material, action, or tension.
2. **Short deck:** 2–7 words; describe the garment, gaze, light, texture, or editorial subject.
3. **Metadata:** 1–3 labels; use a generated collection code, season, portrait code, or issue number only when it serves the layout.

Chinese can lead, English can lead, or they can be split across roles. Keep the language consistent with the style family: restrained language for minimal work, hard nouns for technical work, poetic fragments for romantic work, archival labels for documentary work.

## Rotation rules

- Never reuse the latest title, deck, slogan, or issue number unless the user explicitly requests a series identity.
- Do not use `FORM / MEMORY`, `NOCTURNE`, `FUTURE SKIN`, `ISSUE 08`, or `NEW FORM` as defaults; they are only prior examples.
- Avoid generic words such as `FASHION`, `STYLE`, `LUXURY`, and `BEAUTY` as the main title unless the user specifically asks for a commercial campaign.
- If the visible signature is ambiguous, use a material or compositional noun rather than inventing a personality claim.
- Keep generated text short enough for image-model rendering; place exact long copy later in a layout tool.

## Fragment title gate

- Generate 8–15 candidates internally, then select one strongest title and one short deck.
- Use the selected title as a content decision, not as a random decoration.
- Avoid hollow phrases such as `记录美好生活`, `今天也要开心`, `生活需要仪式感`, `氛围感拉满`, and `治愈一切不开心`.
- If the user provides exact text, preserve it even when it conflicts with the generated title system.
