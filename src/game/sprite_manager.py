from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Mood → (body_color, eye_color, bg_color)
MOOD_PALETTE = {
    "happy":   ("#F4A261", "#2D6A4F", "#FFF9F0"),
    "grumpy":  ("#6A4C93", "#E63946", "#F0EEF6"),
    "playful": ("#43AA8B", "#F4A261", "#F0FBF7"),
    "anxious": ("#E76F51", "#023E8A", "#FFF5F0"),
    "sleepy":  ("#577590", "#ADB5BD", "#F0F4F8"),
}

# Level → (border_color, border_width, badge_emoji)
LEVEL_STYLE = {
    "rookie":    ("#CCCCCC", 4,  ""),
    "learner":   ("#90E0EF", 6,  "⭐"),
    "skilled":   ("#52B788", 8,  "⭐⭐"),
    "expert":    ("#F4A261", 10, "⭐⭐⭐"),
    "legendary": ("#E63946", 12, "👑"),
}

def _draw_cat(draw, mood, cx, cy, size):
    """Draw a cat face centered at (cx, cy)."""
    r = size // 2

    # ── Ears ─────────────────────────────────────────────────
    ear_color = MOOD_PALETTE[mood][0]
    inner_ear  = "#FFB5A7"
    # Left ear
    draw.polygon([(cx - r + 10, cy - r + 20),
                  (cx - r + 35, cy - r - 10),
                  (cx - r + 60, cy - r + 20)], fill=ear_color)
    draw.polygon([(cx - r + 20, cy - r + 18),
                  (cx - r + 35, cy - r + 2),
                  (cx - r + 50, cy - r + 18)], fill=inner_ear)
    # Right ear
    draw.polygon([(cx + r - 60, cy - r + 20),
                  (cx + r - 35, cy - r - 10),
                  (cx + r - 10, cy - r + 20)], fill=ear_color)
    draw.polygon([(cx + r - 50, cy - r + 18),
                  (cx + r - 35, cy - r + 2),
                  (cx + r - 20, cy - r + 18)], fill=inner_ear)

    # ── Head ─────────────────────────────────────────────────
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ear_color)

    # ── Eyes ─────────────────────────────────────────────────
    eye_color = MOOD_PALETTE[mood][1]
    lx, rx = cx - r // 3, cx + r // 3
    ey = cy - r // 6

    if mood == "happy":
        # Curved upward (happy arcs)
        draw.arc([lx - 14, ey - 8, lx + 14, ey + 8], 200, 340, fill=eye_color, width=4)
        draw.arc([rx - 14, ey - 8, rx + 14, ey + 8], 200, 340, fill=eye_color, width=4)
    elif mood == "grumpy":
        # Angled inward (furrowed)
        draw.line([lx - 14, ey - 6, lx + 14, ey + 6], fill=eye_color, width=4)
        draw.line([rx - 14, ey + 6, rx + 14, ey - 6], fill=eye_color, width=4)
        draw.ellipse([lx - 8, ey, lx + 8, ey + 16], fill=eye_color)
        draw.ellipse([rx - 8, ey, rx + 8, ey + 16], fill=eye_color)
    elif mood == "playful":
        # Stars / sparkle eyes
        draw.ellipse([lx - 10, ey - 10, lx + 10, ey + 10], fill=eye_color)
        draw.ellipse([rx - 10, ey - 10, rx + 10, ey + 10], fill=eye_color)
        draw.ellipse([lx - 4,  ey - 4,  lx + 4,  ey + 4],  fill="white")
        draw.ellipse([rx - 4,  ey - 4,  rx + 4,  ey + 4],  fill="white")
    elif mood == "anxious":
        # Wide open circles
        draw.ellipse([lx - 12, ey - 12, lx + 12, ey + 12], fill=eye_color)
        draw.ellipse([rx - 12, ey - 12, rx + 12, ey + 12], fill=eye_color)
        draw.ellipse([lx - 5,  ey - 5,  lx + 5,  ey + 5],  fill="white")
        draw.ellipse([rx - 5,  ey - 5,  rx + 5,  ey + 5],  fill="white")
    elif mood == "sleepy":
        # Half-closed (flat bottom ellipse)
        draw.ellipse([lx - 12, ey - 5, lx + 12, ey + 10], fill=eye_color)
        draw.ellipse([rx - 12, ey - 5, rx + 12, ey + 10], fill=eye_color)
        draw.rectangle([lx - 14, ey - 6, lx + 14, ey + 2], fill=MOOD_PALETTE[mood][0])
        draw.rectangle([rx - 14, ey - 6, rx + 14, ey + 2], fill=MOOD_PALETTE[mood][0])

    # ── Nose ─────────────────────────────────────────────────
    ny = cy + r // 8
    draw.polygon([(cx, ny + 8), (cx - 7, ny), (cx + 7, ny)], fill="#E63946")

    # ── Mouth ────────────────────────────────────────────────
    my = ny + 10
    if mood in ("happy", "playful"):
        draw.arc([cx - 16, my - 6, cx, my + 6],     0, 180, fill="#5C4033", width=3)
        draw.arc([cx,      my - 6, cx + 16, my + 6], 0, 180, fill="#5C4033", width=3)
    elif mood == "grumpy":
        draw.arc([cx - 16, my, cx, my + 12],     180, 360, fill="#5C4033", width=3)
        draw.arc([cx,      my, cx + 16, my + 12], 180, 360, fill="#5C4033", width=3)
    else:
        draw.line([cx - 12, my + 4, cx + 12, my + 4], fill="#5C4033", width=3)

    # ── Whiskers ─────────────────────────────────────────────
    w_color = "#5C4033"
    wy = ny + 2
    for offset in [-12, 0, 12]:
        draw.line([cx - 50, wy + offset, cx - 14, wy], fill=w_color, width=1)
        draw.line([cx + 14, wy, cx + 50, wy + offset], fill=w_color, width=1)


def get_cat_image(mood: str, level: str, size: int = 220) -> Image.Image:
    bg    = MOOD_PALETTE.get(mood, MOOD_PALETTE["happy"])[2]
    border_color, border_width, _ = LEVEL_STYLE.get(level, LEVEL_STYLE["rookie"])

    img  = Image.new("RGB", (size, size), color=bg)
    draw = ImageDraw.Draw(img)

    # Border (level indicator)
    draw.rectangle([0, 0, size - 1, size - 1],
                   outline=border_color, width=border_width)

    # Cat centered in canvas
    _draw_cat(draw, mood, size // 2, size // 2, size // 2 - 20)

    return img


def get_mood_caption(mood: str) -> str:
    captions = {
        "happy":   "😸 Your cat is happy and content!",
        "grumpy":  "😾 Your cat is feeling grumpy...",
        "playful": "😺 Your cat wants to play!",
        "anxious": "🙀 Your cat seems anxious.",
        "sleepy":  "😴 Your cat is getting sleepy.",
    }
    return captions.get(mood, "🐱 Observing your cat...")