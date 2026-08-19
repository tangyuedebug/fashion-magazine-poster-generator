from pathlib import Path
from PIL import Image, ImageStat
import argparse
import csv
import colorsys
import hashlib
import math


EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tif", ".tiff"}


def color_name(rgb):
    r, g, b = [x / 255 for x in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if v < 0.18:
        return "black / charcoal"
    if s < 0.10 and v > 0.88:
        return "white / ivory"
    if s < 0.12:
        return "cool gray"
    if s < 0.25:
        return "muted neutral"
    deg = h * 360
    if deg < 15 or deg >= 345:
        return "red / burgundy"
    if deg < 42:
        return "orange / terracotta"
    if deg < 70:
        return "yellow / ochre"
    if deg < 160:
        return "green / olive"
    if deg < 205:
        return "cyan / teal"
    if deg < 255:
        return "blue / cobalt"
    if deg < 300:
        return "violet / purple"
    return "pink / magenta"


def color_name_zh(rgb):
    name = color_name(rgb)
    return {
        "black / charcoal": "黑色/炭黑",
        "white / ivory": "白色/象牙白",
        "cool gray": "冷灰",
        "muted neutral": "低饱和中性色",
        "red / burgundy": "红色/酒红",
        "orange / terracotta": "橙色/陶土",
        "yellow / ochre": "黄色/赭黄",
        "green / olive": "绿色/橄榄",
        "cyan / teal": "青色/蓝绿",
        "blue / cobalt": "蓝色/钴蓝",
        "violet / purple": "紫色/紫罗兰",
        "pink / magenta": "粉色/品红",
    }.get(name, name)


def _grid_pixels(im, side=48):
    small = im.convert("RGB").resize((side, side))
    px = small.load()
    return small, px


def _mean_hsv(im):
    total_s = 0.0
    total_v = 0.0
    count = 0
    for r, g, b in im.getdata():
        _, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        total_s += s
        total_v += v
        count += 1
    return total_s / max(count, 1), total_v / max(count, 1)


def _quadrant_analysis(im):
    small, px = _grid_pixels(im, 48)
    quads = []
    for qy in range(2):
        for qx in range(2):
            values = []
            edges = []
            for y in range(qy * 24, qy * 24 + 24):
                for x in range(qx * 24, qx * 24 + 24):
                    r, g, b = px[x, y]
                    values.append((0.2126 * r + 0.7152 * g + 0.0722 * b) / 255)
                    if x < 47:
                        r2, g2, b2 = px[x + 1, y]
                        edges.append((abs(r - r2) + abs(g - g2) + abs(b - b2)) / 765)
                    if y < 47:
                        r2, g2, b2 = px[x, y + 1]
                        edges.append((abs(r - r2) + abs(g - g2) + abs(b - b2)) / 765)
            quads.append({"mean": sum(values) / max(len(values), 1), "edge": sum(edges) / max(len(edges), 1)})
    brightest = max(range(4), key=lambda i: quads[i]["mean"])
    darkest = min(range(4), key=lambda i: quads[i]["mean"])
    busiest = max(range(4), key=lambda i: quads[i]["edge"])
    horizontal_balance = abs((quads[0]["mean"] + quads[2]["mean"]) - (quads[1]["mean"] + quads[3]["mean"]))
    vertical_balance = abs((quads[0]["mean"] + quads[1]["mean"]) - (quads[2]["mean"] + quads[3]["mean"]))
    pos = {0: "upper-left", 1: "upper-right", 2: "lower-left", 3: "lower-right"}
    return {
        "brightest": pos[brightest],
        "darkest": pos[darkest],
        "busiest": pos[busiest],
        "horizontal_balance": horizontal_balance,
        "vertical_balance": vertical_balance,
        "quadrants": quads,
    }


def _dominant_colors(im, n=4):
    q = im.convert("RGB").resize((96, 96)).quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    palette = q.getpalette()
    counts = q.getcolors() or []
    colors = []
    for count, idx in sorted(counts, reverse=True):
        rgb = tuple(palette[idx * 3:idx * 3 + 3])
        colors.append((count, rgb))
    return colors[:n]


def image_stats(path):
    try:
        with Image.open(path) as im:
            im = im.convert("RGB")
            w, h = im.size
            small = im.copy()
            small.thumbnail((160, 160))
            stat = ImageStat.Stat(small)
            mean = tuple(int(x) for x in stat.mean)
            extrema = stat.extrema
            spread = sum((hi - lo) for lo, hi in extrema) / 3
            sat_mean, value_mean = _mean_hsv(small)
            gray_delta = sum(abs(mean[i] - sum(mean) / 3) for i in range(3))
            if gray_delta < 12 and sat_mean < 0.12:
                color_mode = "monochrome black and white"
            elif sat_mean < 0.25:
                color_mode = "muted low-saturation palette"
            else:
                color_mode = "full-color editorial palette"
            if spread > 150:
                contrast = "high contrast"
            elif spread < 70:
                contrast = "soft low contrast"
            else:
                contrast = "moderate contrast"
            if w / h > 1.18:
                orientation = "landscape"
            elif h / w > 1.18:
                orientation = "portrait"
            else:
                orientation = "near-square"
            q = _quadrant_analysis(small)
            colors = _dominant_colors(small)
            edge_density = sum(qi["edge"] for qi in q["quadrants"]) / 4
            whitespace = sum(1 for qi in q["quadrants"] if qi["mean"] > 0.78 and qi["edge"] < 0.12) / 4
            if edge_density > 0.22:
                visual_density = "dense graphic or collage structure"
            elif edge_density < 0.08:
                visual_density = "quiet, sparse composition"
            else:
                visual_density = "moderately layered composition"
            return {
                "w": w, "h": h, "ratio": round(w / h, 3), "orientation": orientation,
                "color_mode": color_mode, "contrast": contrast, "palette": color_name(mean),
                "palette_zh": color_name_zh(mean), "dominant_colors": colors, "sat_mean": sat_mean,
                "value_mean": value_mean, "quadrants": q, "edge_density": edge_density,
                "whitespace": whitespace, "visual_density": visual_density, "note": "ok",
            }
    except Exception as exc:
        return {
            "w": 0, "h": 0, "ratio": 0, "orientation": "unknown orientation",
            "color_mode": "unknown color treatment", "contrast": "unknown contrast", "palette": "unknown palette",
            "palette_zh": "未知色调", "dominant_colors": [], "sat_mean": 0, "value_mean": 0,
            "quadrants": {"brightest": "unknown", "darkest": "unknown", "busiest": "unknown", "horizontal_balance": 0, "vertical_balance": 0, "quadrants": []},
            "edge_density": 0, "whitespace": 0, "visual_density": "unknown density", "note": f"unreadable: {exc}",
        }


def category_for(path):
    name = path.parts[-2] if len(path.parts) >= 2 else ""
    if name.startswith("01_"):
        return "layout"
    if name.startswith("02_"):
        return "color"
    if name.startswith("03_"):
        return "typography"
    if name.startswith("04_"):
        return "image"
    if name.startswith("05_"):
        return "function"
    return "editorial"


LAYOUT_VARIANTS = [
    ("asymmetric 12-column spread with a narrow information rail on the left", "12 栏不对称跨页，左侧窄信息轨"),
    ("split composition with a tall image panel and a quiet text field on the opposite side", "高竖图像板与对侧安静文字区的分栏构图"),
    ("centered hero with oversized cropped title crossing the image boundary", "中央主视觉与越界超大标题"),
    ("four-panel lookbook grid with one panel deliberately enlarged", "四宫格 lookbook，其中一格刻意放大"),
    ("diagonal editorial rhythm with image, caption, and rule lines stepping downward", "图片、说明、细线向下错落的对角线节奏"),
    ("full-bleed image interrupted by a small floating caption block", "满版主图被小型悬浮信息块打断"),
    ("top-and-bottom editorial bands with a strong central pause", "上下编辑带与中央停顿区"),
    ("mosaic of unequal image tiles aligned to a visible baseline", "不等尺寸图片拼贴并统一基线"),
    ("left-heavy composition with a large clean negative-space field on the right", "左重右留白构图"),
    ("vertical type spine and a low, wide image strip", "竖向文字脊柱与底部横向图片带"),
    ("overlapping cutout figures with restrained registration offsets", "人物切出叠放与克制套印错位"),
    ("editorial poster with a small inset image inside a dominant paper field", "大面积纸张底场中的小型嵌入图"),
]
COLOR_VARIANTS = [
    ("a single saturated accent against warm ivory and near-black", "暖象牙白与近黑中嵌入单一高饱和强调色"),
    ("a cool blue monochrome ramp with one pale coral interruption", "冷蓝单色阶与一点浅珊瑚色"),
    ("earthy terracotta, tobacco, and faded cream with tactile warmth", "陶土、烟草棕、褪色奶油色的温暖组合"),
    ("deep burgundy, charcoal, and muted blush for controlled drama", "深酒红、炭黑、低饱和粉的戏剧组合"),
    ("olive green, chalk white, and ochre yellow with a utilitarian mood", "橄榄绿、粉笔白、赭黄色的实用主义组合"),
    ("electric cobalt, paper white, and a small acid-lime accent", "电光钴蓝、纸白与少量酸橙色"),
    ("dusty lilac, soft gray, and silver with a cool romantic tone", "灰紫、柔灰、银色的冷调浪漫"),
    ("sun-faded orange, pink, and cream with a late-afternoon glow", "褪日橙、粉色、奶油色的午后感"),
    ("near-black and bone white with a restrained metallic champagne detail", "近黑、骨白与克制香槟金细节"),
    ("teal, rust, and parchment in a compact complementary palette", "蓝绿、铁锈红、羊皮纸色的互补组合"),
]
POSE_VARIANTS = [
    ("walking past the camera while the shoulders stay squared", "从镜头前走过，肩线保持挺直"),
    ("seated sideways with one hand resting lightly on the knee", "侧坐，一只手轻放在膝上"),
    ("turning the torso away while the face returns toward the lens", "身体转开，脸部回到镜头方向"),
    ("leaning against a wall with one ankle crossed over the other", "靠墙站立，一只脚踝交叠"),
    ("lifting the collar or sleeve to make the fabric structure visible", "抬起衣领或袖口，展示面料结构"),
    ("arms extended slightly outward so the silhouette creates a clean graphic shape", "双臂微微向外伸展，形成清晰图形轮廓"),
    ("looking down while adjusting a cuff, belt, or small accessory", "低头整理袖口、腰带或小配饰"),
    ("standing almost still, weight shifted into one hip, with a long vertical line", "近乎静止站立，重心落在一侧髋部，形成长竖线"),
    ("reclining with the garment spread around the body like a sculptural field", "身体后倚，服装像雕塑场一样展开"),
    ("two models arranged at different depths, one facing forward and one in profile", "两位模特前后错位，一人正面、一人侧面"),
    ("close crop of hands, neck, and garment detail instead of a full figure", "只裁切手部、颈部与服装细节，不出现完整人物"),
    ("a garment or accessory suspended mid-motion, suggesting a held breath", "服装或配饰悬停在运动瞬间，像屏住呼吸"),
]
EXPRESSION_VARIANTS = [
    ("quiet direct gaze with composed self-possession", "安静直视，克制而自持"),
    ("a distant side glance, thoughtful rather than smiling", "疏离侧目，若有所思而不微笑"),
    ("lowered eyes and a softened mouth, inward and restrained", "眼神下压、嘴角放松，内收且克制"),
    ("slightly raised brow with a hint of dry wit", "轻微挑眉，带一点冷幽默"),
    ("calm alertness, as if listening to something outside the frame", "平静而警觉，像在聆听画外声音"),
    ("minimal half-smile with an editorial, unforced confidence", "极轻的半笑，自然而有编辑感的自信"),
    ("serene neutrality, allowing the clothing and silhouette to carry the emotion", "平静中性，让服装和轮廓承担情绪"),
    ("intense eye contact softened by a gentle head tilt", "强烈眼神接触，但头部轻微倾斜以柔化"),
    ("dreamy, absorbed expression with no theatrical exaggeration", "梦游般专注，不做戏剧化夸张"),
    ("profile expression with a small tension around the jaw", "侧脸神态，下颌保留一点紧张感"),
]
LIGHT_VARIANTS = [
    ("hard window light from the upper left, casting a clean rectangular shadow", "左上方硬质窗光，投下清晰矩形阴影"),
    ("soft frontal daylight with a cool rim light on the far shoulder", "柔和正面日光，远侧肩部带冷色轮廓光"),
    ("a narrow top spotlight that isolates the figure from a dark ground", "窄束顶光把人物从深色底场中分离"),
    ("warm low side light grazing across the fabric while the face stays quiet", "暖色低位侧光擦过面料，脸部保持安静"),
    ("overcast diffused light with barely visible shadows and a matte atmosphere", "阴天漫射光，阴影极浅，哑光氛围"),
    ("red and blue stage reflections split across the silhouette", "红蓝舞台反射光在轮廓上分裂"),
    ("backlight through translucent fabric, producing a pale halo and soft flare", "光线穿过半透明面料，产生浅色光晕与柔和眩光"),
    ("single side key light with deep falloff and controlled negative fill", "单侧主光、深渐暗与受控负补光"),
    ("flash-like frontal light with crisp edges and a slightly flattened fashion image", "闪光灯式正面光，边缘清晰、画面略平面化"),
    ("late-afternoon amber light with long architectural shadows", "傍晚琥珀光与长条建筑阴影"),
]
FONT_VARIANTS = [
    ("high-contrast modern serif masthead with a narrow grotesk for metadata", "高对比现代衬线刊头搭配窄体无衬线元信息"),
    ("condensed sans-serif title stacked vertically with generous tracking", "窄体无衬线标题竖向堆叠并拉开字距"),
    ("giant serif initials cropped by the frame, supported by tiny monospaced labels", "超大衬线首字母被画框裁切，配小号等宽标签"),
    ("soft italic serif for the feature title and restrained uppercase sans-serif notes", "柔和斜体衬线专题标题搭配克制大写无衬线注释"),
    ("bold geometric sans-serif blocks with one delicate hairline caption", "粗几何无衬线字块搭配一条纤细说明线"),
    ("vertical masthead along the outer edge with small aligned folio numbers", "外侧边缘竖排刊头与对齐的页码"),
    ("oversized title behind the model, partially obscured but still legible", "超大标题置于模特之后，局部遮挡但保持可读"),
    ("lowercase editorial wordmark with widely spaced small caps", "小写编辑刊名与宽字距小型大写"),
    ("split headline across two columns, with one word crossing the image seam", "标题拆分到两栏，其中一个词跨越图像接缝"),
    ("minimal type system using one family, contrasting only weight and scale", "单一字体家族，仅用字重和字号做对比"),
]
FUNCTION_VARIANTS = [
    ("a quiet luxury magazine cover", "安静奢华杂志封面"),
    ("a runway announcement with date, venue, and collection code", "含日期、场地和系列编号的秀场公告"),
    ("a seasonal lookbook opening page", "季节 lookbook 开篇页"),
    ("a color-direction board for a fashion collection", "时装系列色彩方向板"),
    ("an editorial portrait feature opener", "编辑部人物专题开篇"),
    ("a campaign poster for a limited capsule collection", "限量胶囊系列 campaign 海报"),
    ("a fashion week invitation with compact information hierarchy", "信息紧凑的时装周邀请函"),
    ("a brand manifesto poster with one short statement", "只有一句短宣言的品牌海报"),
    ("a retail window or launch communication poster", "零售橱窗或新品发布传播海报"),
    ("an archive-style fashion index with numbered looks", "带编号造型的档案式时装索引"),
]


def pick(options, key, salt=0):
    digest = hashlib.sha1(f"{key}|{salt}".encode("utf-8")).hexdigest()
    return options[int(digest[:8], 16) % len(options)]


def _quadrant_zh(q):
    return {"upper-left": "左上", "upper-right": "右上", "lower-left": "左下", "lower-right": "右下"}.get(q, q)


def _category_base(category, variant):
    if category == "layout":
        return f"a fashion magazine editorial layout focused on {variant[0]}"
    if category == "color":
        return f"a fashion color-direction composition organized as {variant[0]}"
    if category == "typography":
        return f"a typography-led fashion poster using {variant[0]}"
    if category == "image":
        return "a high-fashion editorial image with a single controlled hero subject"
    if category == "function":
        return f"{variant[0]} for a contemporary fashion label"
    return "a contemporary fashion editorial graphic"


def dynamic_editorial_text(key, category, stats, pose, expression, palette, light, function, seq):
    """Create short copy from visible style cues; never use one fixed title."""
    expr = expression[0].lower()
    if "direct gaze" in expr or "eye contact" in expr:
        title_pool = [("STEADY PRESENCE", "稳定存在"), ("OPEN SIGNAL", "开放信号"), ("THE HELD GAZE", "凝视之间")]
    elif "side glance" in expr or "profile" in expr:
        title_pool = [("DISTANT FORM", "远方形态"), ("SIDE NOTE", "侧面注释"), ("OFF FRAME", "画外之处")]
    elif "lowered eyes" in expr or "dreamy" in expr:
        title_pool = [("INNER LIGHT", "内在微光"), ("SOFT FOCUS", "柔焦时刻"), ("QUIET CURRENT", "静默流动")]
    else:
        title_pool = [("CALM FORCE", "平静力量"), ("VISIBLE TENSION", "可见张力"), ("STILL SIGNAL", "静止信号")]

    palette_text = f"{stats.get('palette', '')} {palette[0]}".lower()
    if any(word in palette_text for word in ("black", "charcoal", "graphite", "dark")):
        material_en, material_zh = "DARK GRAIN", "暗面肌理"
    elif any(word in palette_text for word in ("burgundy", "rust", "terracotta", "red", "orange")):
        material_en, material_zh = "WARM TRACE", "暖色痕迹"
    elif any(word in palette_text for word in ("gray", "silver", "blue", "cool")):
        material_en, material_zh = "COLD CONTOUR", "冷感轮廓"
    else:
        material_en, material_zh = "TACTILE FIELD", "触感场域"

    pose_text = pose[0].lower()
    if "turning the torso" in pose_text or "turning" in pose_text:
        gesture_en, gesture_zh = "TURNED LINE", "回身线条"
    elif "collar" in pose_text or "cuff" in pose_text or "sleeve" in pose_text:
        gesture_en, gesture_zh = "HAND / FABRIC", "手与面料"
    elif "seated" in pose_text or "reclining" in pose_text:
        gesture_en, gesture_zh = "HELD POSTURE", "停驻姿态"
    else:
        gesture_en, gesture_zh = "QUIET GESTURE", "安静动作"

    title_en, title_zh = pick(title_pool, f"{key}|dynamic-title", 31)
    deck_en = f"{material_en} / {gesture_en}"
    deck_zh = f"{material_zh} · {gesture_zh}"
    code = int(hashlib.sha1(f"{key}|dynamic-code".encode("utf-8")).hexdigest()[:6], 16) % 900 + 100
    metadata = [f"PORTRAIT {code}", category.upper(), function[1]]
    signature_en = f"{expression[0]}; {pose[0]}; {palette[0]}; {light[0]}"
    signature_zh = f"{expression[1]}；{pose[1]}；{palette[1]}；{light[1]}"
    return {
        "editorial_title_en": title_en,
        "editorial_title_zh": title_zh,
        "editorial_deck_en": deck_en,
        "editorial_deck_zh": deck_zh,
        "editorial_metadata": metadata,
        "signature_en": signature_en,
        "signature_zh": signature_zh,
    }


def rich_templates(category, path, stats, seq):
    key = str(path)
    layout = pick(LAYOUT_VARIANTS, key, 1)
    palette = pick(COLOR_VARIANTS, key, 2)
    pose = pick(POSE_VARIANTS, key, 3)
    expression = pick(EXPRESSION_VARIANTS, key, 4)
    light = pick(LIGHT_VARIANTS, key, 5)
    font = pick(FONT_VARIANTS, key, 6)
    function = pick(FUNCTION_VARIANTS, key, 7)
    text = dynamic_editorial_text(key, category, stats, pose, expression, palette, light, function, seq)
    visual_mass = stats["quadrants"]["busiest"]
    bright = stats["quadrants"]["brightest"]
    dark = stats["quadrants"]["darkest"]
    ratio = stats["ratio"] or 1.0
    ratio_text = f"{ratio:.2f}:1 aspect ratio"
    dom = ", ".join(color_name(c) for _, c in stats["dominant_colors"][:3]) or stats["palette"]
    layout_note_en = (
        f"the brightest visual field is concentrated in the {bright} quadrant, "
        f"the darkest field in {dark}, and the busiest detail in {visual_mass}"
    )
    layout_note_zh = (
        f"最亮区域在{_quadrant_zh(bright)}、最暗区域在{_quadrant_zh(dark)}，细节最密集在{_quadrant_zh(visual_mass)}"
    )
    category_variant = pick({
        "layout": LAYOUT_VARIANTS,
        "color": COLOR_VARIANTS,
        "typography": FONT_VARIANTS,
        "image": POSE_VARIANTS,
        "function": FUNCTION_VARIANTS,
    }.get(category, LAYOUT_VARIANTS), key, 8)
    base = _category_base(category, category_variant)
    subject = (
        "a young adult fashion model or a carefully cropped garment detail, "
        f"{pose[0]}, with {expression[0]}; "
        "if the reference is non-figurative, translate this into fabric movement or object direction"
    )
    common = (
        f"{stats['orientation']} composition, {layout[0]}, {layout_note_en}, "
        f"{stats['visual_density']}, {stats['color_mode']}, {stats['contrast']}, "
        f"dominant sampled colors {dom}, {palette[0]}, {font[0]}, {light[0]}, "
        f"{function[0]}, {ratio_text}, subtle matte paper and fine film grain, "
        f"dynamic editorial title {text['editorial_title_en']}, short deck {text['editorial_deck_en']}, metadata {text['editorial_metadata'][0]}, "
        "clear subject separation, precise alignment, no watermark, no brand logo, no illegible long paragraphs"
    )
    master = f"{base}; {subject}; {common}."
    zh = (
        f"{category_variant[1]}；{layout[1]}；{stats['orientation']}，画面视觉重心在{_quadrant_zh(visual_mass)}，"
        f"{layout_note_zh}，{stats['visual_density']}；"
        f"主视觉为年轻成人时装模特或裁切的服装细节，{pose[1]}，神态为{expression[1]}；"
        f"{font[1]}；{light[1]}；参考图提取的主色倾向为{stats['palette_zh']}，并加入{palette[1]}；"
        f"功能为{function[1]}；根据人物可见特征动态生成标题“{text['editorial_title_zh']}”、副标题“{text['editorial_deck_zh']}”和编号“{text['editorial_metadata'][0]}”；"
        f"{stats['orientation']}、比例约 {ratio:.2f}:1；哑光纸张、细颗粒胶片、精确对齐，避免固定模板文字"
    )
    sd = (
        f"({base}:1.2), ({layout[0]}:1.25), ({subject}:1.1), {palette[0]}, {font[0]}, {light[0]}, "
        f"{stats['color_mode']}, {stats['contrast']}, sampled palette {dom}, {ratio_text}, "
        f"editorial fashion photography, premium print design, clear hierarchy, clean edges, dynamic title {text['editorial_title_en']}, high detail"
    )
    mj = f"{base}, {subject}, {common}, high-detail editorial fashion photography --ar {ratio:.2f} --style raw --no watermark, logo, messy text"
    image2_en = (
        f"Create {base}. The reference-specific structure is {layout[0]}; keep the brightest field in the {bright} quadrant, "
        f"the darkest field in the {dark} quadrant, and the densest visual detail in the {visual_mass} quadrant. "
        f"Show {subject}. Use {palette[0]}; the sampled reference palette leans toward {dom}. "
        f"Use {font[0]} and {light[0]}. The communication function is {function[0]}. "
        f"Generate fresh copy from the visible subject signature: title {text['editorial_title_en']}, deck {text['editorial_deck_en']}, metadata {text['editorial_metadata'][0]}. "
        f"Keep the {stats['orientation']} {ratio_text}, with an intentional negative-space field, matte paper texture, subtle film grain, "
        "one clear focal point, and short correctly spelled text only. Do not copy the reference literally; redesign the relationships as an original fashion editorial. Avoid long paragraphs, random letters, watermarks, logos, distorted anatomy, duplicated figures, and clutter."
    )
    image2_zh = (
        f"根据参考图重新设计一张{function[1]}。采用{layout[1]}，保留参考图中{_quadrant_zh(bright)}偏亮、{_quadrant_zh(dark)}偏暗、{_quadrant_zh(visual_mass)}细节最密集的视觉关系，但不要直接复制。"
        f"主视觉为年轻成人时装模特或服装细节，{pose[1]}，神态{expression[1]}。采用{palette[1]}，字体为{font[1]}，光影为{light[1]}。"
        f"画面为{stats['orientation']}、比例约 {ratio:.2f}:1，保留明确留白，哑光纸张与细颗粒胶片质感；根据人物的{expression[1]}、{pose[1]}、{palette[1]}动态生成标题“{text['editorial_title_zh']}”、副标题“{text['editorial_deck_zh']}”和编号“{text['editorial_metadata'][0]}”，不要套用固定标题；避免长段乱码、水印、品牌标志、畸形手部、重复人物和杂乱装饰。"
    )
    flux = f"{master} Magazine-quality art direction, realistic print texture, controlled composition, crisp details."
    niji = f"Fashion editorial poster, {base}, {layout[0]}, {palette[0]}, expressive pose, graphic print design, clean hierarchy --ar {ratio:.2f} --niji 6"
    neg = "low resolution, blurry face, muddy colors, distorted anatomy, extra limbs, duplicated people, awkward hands, unreadable long paragraphs, random letters, warped typography, cluttered layout, watermark, brand logo, plastic skin, inconsistent shadows, compression artifacts"
    return {
        "visual_summary_zh": zh, "variation_code": f"R{seq:04d}-{hashlib.sha1(key.encode()).hexdigest()[:6]}",
        "layout_feature": layout[1], "palette_feature": palette[1], "font_feature": font[1],
        "pose_feature": pose[1], "expression_feature": expression[1], "lighting_feature": light[1],
        "function_feature": function[1], "reference_basis": layout_note_en + f"; sampled colors: {dom}",
        **text,
        "master_prompt_en": master, "stable_diffusion_prompt": sd, "midjourney_prompt": mj,
        "image2_prompt_en": image2_en, "image2_prompt_zh": image2_zh, "flux_prompt": flux,
        "nijijourney_prompt": niji, "negative_prompt": neg,
    }


def main(input_root, output_dir=None):
    root = Path(input_root).resolve()
    output_dir = Path(output_dir or root).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    out_csv = output_dir / "image_reverse_prompts_rich.csv"
    out_image2_csv = output_dir / "image2_only_reverse_prompts_rich.csv"
    out_md = output_dir / "image_reverse_prompts_rich.md"
    out_universal = output_dir / "universal_fashion_editorial_prompt_rich.md"
    files = sorted([p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in EXTS], key=lambda p: str(p).lower())
    fields = [
        "id", "source_file", "category", "width", "height", "aspect_ratio", "orientation", "color_mode", "contrast", "dominant_palette", "dominant_colors", "visual_density", "brightest_quadrant", "darkest_quadrant", "busiest_quadrant", "readability_note",
        "variation_code", "reference_basis", "layout_feature", "palette_feature", "font_feature", "pose_feature", "expression_feature", "lighting_feature", "function_feature", "editorial_title_en", "editorial_title_zh", "editorial_deck_en", "editorial_deck_zh", "editorial_metadata", "signature_en", "signature_zh",
        "visual_summary_zh", "master_prompt_en", "stable_diffusion_prompt", "midjourney_prompt", "image2_prompt_en", "image2_prompt_zh", "flux_prompt", "nijijourney_prompt", "negative_prompt"
    ]
    rows = []
    counts = {}
    for idx, path in enumerate(files, 1):
        rel = path.relative_to(root).as_posix()
        cat = category_for(path)
        stats = image_stats(path)
        rich = rich_templates(cat, path, stats, idx)
        dom = ", ".join(f"{c[0]}:{c[1]}" for c in stats["dominant_colors"])
        rows.append({
            "id": f"IMG-{idx:04d}", "source_file": rel, "category": cat, "width": stats["w"], "height": stats["h"], "aspect_ratio": stats["ratio"],
            "orientation": stats["orientation"], "color_mode": stats["color_mode"], "contrast": stats["contrast"], "dominant_palette": stats["palette"], "dominant_colors": dom,
            "visual_density": stats["visual_density"], "brightest_quadrant": stats["quadrants"]["brightest"], "darkest_quadrant": stats["quadrants"]["darkest"], "busiest_quadrant": stats["quadrants"]["busiest"], "readability_note": stats["note"],
            **rich,
        })
        counts[cat] = counts.get(cat, 0) + 1

    with out_csv.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    image2_fields = ["id", "source_file", "category", "visual_summary_zh", "image2_prompt_en", "image2_prompt_zh"]
    with out_image2_csv.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=image2_fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "id": row["id"],
                "source_file": row["source_file"],
                "category": row["category"],
                "visual_summary_zh": row["visual_summary_zh"],
                "image2_prompt_en": row["image2_prompt_en"],
                "image2_prompt_zh": row["image2_prompt_zh"],
            })

    with out_md.open("w", encoding="utf-8") as f:
        f.write("# 全部图片反推提示词\n\n")
        f.write(f"已生成 **{len(rows)}** 个图片条目。每条记录都根据图片采样得到的画幅、明暗象限、色彩分布、视觉密度和构图重心生成，并加入差异化的版式、字体、动作、神态、光影、色调与功能组合。\n\n")
        f.write("## 分类统计\n\n")
        for k in ["layout", "color", "typography", "image", "function", "editorial"]:
            if k in counts:
                f.write(f"- {k}: {counts[k]} 张\n")
        f.write("\n## 使用说明\n\n")
        f.write("这些是根据图片可见的版式、构图、色彩、字体关系、摄影类型和技术特征反推的**可复现视觉提示词**，不是原始作者的隐藏 prompt。动作与神态是结合参考图类型生成的可执行设计描述；当参考图没有人物时，会自动转换为服装/物体的运动方向。真实品牌名、完整杂志正文和水印没有被当作生成指令，以避免生成乱码或不必要的品牌复刻。\n\n")
        f.write("## 推荐工作流\n\n")
        f.write("1. Image 2 优先使用 `image2_only_reverse_prompts_rich.csv` 的 `image2_prompt_zh` 或 `image2_prompt_en`。\n2. 每次生成至少替换 6 个变量：风格族、版式、色彩、字体关系、人物动作/神态、光影、功能和图像策略。\n3. 无准确文案时，使用 CSV 中根据人物可见特征生成的 `editorial_title_zh`、`editorial_deck_zh` 和 `editorial_metadata`，不要套用固定标题。\n4. 若需要准确刊名、日期、页码和说明，请在生成后使用排版软件重新输入，不要依赖模型生成长段正文。\n5. 想保持参考图结构时，只固定 `reference_basis`；其余字段轮换，避免批量结果同质化。\n")

    out_universal.write_text("""# 基于参考图的高审美通用提示词系统

从逐图 CSV 中选一条作为结构基准，再替换主题或人物，不要把所有参考图平均混成一张泛化海报。

## 通用母提示词

```text
请以参考图片为视觉研究依据，提取构图重心、明暗分区、色彩层级、字体关系和印刷质感，但重新设计成原创的当代时尚杂志视觉，不直接复制人物、品牌、标题或具体图像。

功能：{function_feature}。画幅：{orientation}，比例约 {ratio}。版式：{layout_feature}；让主视觉占画面约 55%–75%，在 {left/right/top/bottom} 保留 20%–40% 功能性留白。
主视觉：{人物/局部人物/服装细节/色卡与材质}；服装为 {廓形、面料、层次和配饰}。动作：{pose_feature}。神态：{expression_feature}。视线朝向 {镜头/留白区/画外/侧前方}。若没有人物，将动作转译为衣料飘动、悬停配饰、折叠结构或物体方向。
字体：{font_feature}；最多两种字体家族。根据人物可见特征动态生成标题“{editorial_title_zh}”、副标题“{editorial_deck_zh}”和元信息“{editorial_metadata}”，不要使用固定模板标题。色彩：参考图采样主色为 {reference palette}；本次改用 {palette_feature}，保持背景色、文字色、主视觉色、单一强调色四层。
光影：{lighting_feature}；光线方向统一，阴影服务主体轮廓。材质：哑光纸张、细腻纸纤维、轻微胶片颗粒、克制套印或半透明色块。
每次生成必须与上一张明显不同：改变风格族并至少改变另外五项变量；标题、副标题和编号也必须根据当前人物的可见风格特征重新生成，不能重复上一张。保留一个主焦点。避免乱码长文、品牌标志、水印、塑料皮肤、畸形手指、重复人物、僵硬站姿、廉价 3D、过度拼贴和拥挤排版。
```

## 差异化轮换

每次记录并轮换：风格族、版式、色彩、字体关系、主体位置、动作、神态、光影、功能、图像策略和动态文字。连续两张必须改变风格族并至少改变另外五项。准确正文、日期和长文案在生成后用排版软件输入。
""", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate evidence-based fashion editorial prompts from reference images.")
    parser.add_argument("--root", required=True, help="Reference image folder")
    parser.add_argument("--output-dir", default=None, help="Output folder; defaults to --root")
    args = parser.parse_args()
    main(args.root, args.output_dir)
