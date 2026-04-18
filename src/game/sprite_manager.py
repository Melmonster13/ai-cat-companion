from PIL import Image, ImageDraw
from pathlib import Path

MOOD_COLORS = {
    "happy":   "#F9C74F",
    "grumpy":  "#6A4C93",
    "playful": "#43AA8B",
    "anxious": "#F8961E",
    "sleepy":  "#577590",
}

LEVEL_BORDER = {
    "rookie":    "#CCCCCC",
    "learner":   "#90E0EF",
    "skilled":   "#52B788",
    "expert":    "#F4A261",
    "legendary": "#E63946",
}

def get_cat_image(mood: str, level: str, size=(200, 200)) -> Image.Image:
    """
    Returns a PIL Image for the cat.
    Week 6: replace body of this function with real sprite loading.
    """
    sprites_path = Path("src/game/assets/sprites") / f"cat_{mood}_{level}.png"
    if sprites_path.exists():
        return Image.open(sprites_path).resize(size)

    # Fallback: colored placeholder
    img = Image.new("RGB", size, color=MOOD_COLORS.get(mood, "#AAAAAA"))
    draw = ImageDraw.Draw(img)
    border_color = LEVEL_BORDER.get(level, "#CCCCCC")
    draw.rectangle([0, 0, size[0]-1, size[1]-1], outline=border_color, width=8)
    draw.text((size[0]//2 - 30, size[1]//2 - 10), mood.upper(),
              fill="white")
    return img