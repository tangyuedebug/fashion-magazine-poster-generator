# Prompt Rotation Reference

Use one reference image as the structural anchor, then rotate the remaining variables. Do not average all references into one generic prompt.

## Evidence vs. design direction

- Evidence: aspect ratio, orientation, dominant colors, contrast, brightest/darkest quadrant, visual density, detail-heavy quadrant, whitespace tendency.
- Design direction: exact font family, model action, expression, lighting recipe, communication function, and replacement palette. Phrase these as executable choices, not claims about hidden author intent.

## Rotation matrix

Keep a generation log with: `reference`, `reference_mode`, `style_family`, `layout`, `palette`, `font`, `subject_position`, `pose`, `expression`, `lighting`, `function`, `image_strategy`, and `recent_exclusions`.

Change the style family plus at least five other columns between successive outputs. Never reuse the latest dominant palette and layout when the user asks for another style.

- Style family: street-editorial graphic, quiet luxury, retro French editorial, Y2K digital, Y2K cyber-kawaii idol scrapbook, gothic romantic, Japanese minimal, art-school collage, futuristic technical, sports couture, surreal color-block, documentary runway, typography-first.

- Layout: asymmetrical grid, split page, centered hero, four-panel lookbook, diagonal rhythm, full-bleed crop, top/bottom bands, unequal mosaic, left-heavy negative space, vertical type spine, overlapping cutouts, inset image.
- Palette: cool gray monochrome, ivory neutral, burgundy charcoal, terracotta tobacco, cobalt acid-lime, olive ochre, lilac silver, faded orange pink, bone black champagne, teal rust parchment.
- Font relation: high-contrast serif plus narrow grotesk, stacked condensed sans, cropped serif initials, italic serif plus uppercase sans, geometric blocks plus hairline caption, vertical masthead, title behind subject, lowercase wordmark, split headline, one-family weight contrast.
- Pose: walking past camera, side-seated, torso turned with face returned, wall lean, collar adjustment, arms extended, cuff adjustment, one-hip stance, reclining sculptural silhouette, two-depth blocking, close crop of hands/neck, suspended garment.
- Expression: composed direct gaze, distant side glance, lowered eyes, raised brow, calm alertness, minimal half-smile, serene neutrality, softened intense eye contact, dreamy absorption, profile jaw tension.
- Lighting: hard window rectangle, soft daylight rim, top spotlight, warm low side light, overcast diffusion, red/blue stage reflection, translucent backlight halo, single side key with negative fill, frontal flash, late-afternoon amber shadows.
- Function: cover, runway announcement, seasonal lookbook, color board, editorial portrait opener, capsule campaign, invitation, manifesto, retail launch, archive index.

## Image 2 text policy

Ask for only short, clear text: masthead, title, date, issue number, location, collection code, or a few labels. Replace exact copy in a layout tool after generation. Never use long body text as a quality test for the image model.
