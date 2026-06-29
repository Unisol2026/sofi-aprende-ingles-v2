from pathlib import Path
import math
import re

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "Imagens" / "expressions"
SIZE = 512


EXPRESSIONS = {
    "hello": ["Hello!", "What's your name?", "I'm Sofia."],
    "unit1": [
        "Stand up.",
        "Sit down.",
        "Open your book.",
        "Close your book.",
        "Pick up your pencil.",
        "Put your bag on your desk.",
    ],
    "unit2": [
        "This is my brother.",
        "Open the door.",
        "Say hello to your mum.",
        "What's that?",
        "It's a sandwich.",
    ],
    "unit3": [
        "I'm happy.",
        "You're happy.",
        "I'm angry.",
        "I'm sad.",
        "I'm scared.",
        "Close your eyes.",
        "Open your eyes.",
        "Give your friend a hug.",
    ],
    "unit4": [
        "I've got a ball.",
        "Throw the ball.",
        "Catch the ball.",
        "Bounce the ball.",
        "Put the ball in your bag.",
        "I haven't got a kite.",
    ],
    "unit5": [
        "The doll is in the cabinet.",
        "The doll is on the cabinet.",
        "The doll is under the cabinet.",
        "Where's the cat?",
        "Look on the couch.",
        "Look under the table.",
        "It's in the cabinet.",
        "Tidy up!",
        "Put the kite in the cabinet.",
    ],
    "unit6": [
        "My favorite color is orange.",
        "I like your colors.",
        "Sniff like a rabbit.",
        "Eat like a rabbit.",
        "Hop, rabbit, hop!",
        "Run, dog, run!",
    ],
    "unit7": [
        "I like carrots.",
        "I don't like carrots.",
        "What's that smell?",
        "You're hungry.",
        "Go into the kitchen.",
        "Take one.",
        "Eat the chip.",
        "Yummy!",
    ],
    "unit8": [
        "I'm riding a bike.",
        "You're riding a bike.",
        "Oh what fun!",
        "Thank you.",
        "We're having fun!",
    ],
    "unit9": [
        "Let's have biscuits.",
        "Let's have crisps.",
        "Let's have salad.",
        "Let's have sweets.",
        "Nice work!",
        "Walk home.",
        "Open the door.",
        "Surprise!",
        "Put on your party hat.",
        "Dance with your friends.",
    ],
}


def slug(text: str) -> str:
    value = text.lower().replace("'", "")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "expression"


def new_canvas():
    img = Image.new("RGB", (SIZE, SIZE), "#fffaf2")
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((20, 20, 492, 492), radius=36, fill="#fffdf8", outline="#f2c7d7", width=8)
    draw.ellipse((34, 34, 142, 112), fill="#f4e7ff")
    draw.ellipse((376, 44, 472, 126), fill="#dff5ff")
    draw.ellipse((44, 396, 160, 474), fill="#e6f6da")
    return img, draw


def paste_asset(img, rel_path, box, alpha=255):
    path = ROOT / rel_path
    if not path.exists():
        return False
    asset = Image.open(path).convert("RGBA")
    max_w = box[2] - box[0]
    max_h = box[3] - box[1]
    asset.thumbnail((max_w, max_h), Image.LANCZOS)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    x = box[0] + (max_w - asset.width) // 2
    y = box[1] + (max_h - asset.height) // 2
    if alpha != 255:
        a = asset.getchannel("A").point(lambda p: p * alpha // 255)
        asset.putalpha(a)
    layer.alpha_composite(asset, (x, y))
    img.paste(Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"))
    return True


def draw_floor(draw):
    draw.rounded_rectangle((70, 374, 442, 430), radius=28, fill="#f5ead9", outline="#e2d0b8", width=3)


def draw_arrow(draw, start, end, color="#e85d89", width=8):
    draw.line((start, end), fill=color, width=width)
    ang = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 24
    p1 = (end[0] - size * math.cos(ang - 0.55), end[1] - size * math.sin(ang - 0.55))
    p2 = (end[0] - size * math.cos(ang + 0.55), end[1] - size * math.sin(ang + 0.55))
    draw.polygon([end, p1, p2], fill=color)


def draw_kid(draw, x, y, shirt="#7bc8ff", pose="stand", face="happy", scale=1.0):
    s = scale
    head = [x - 34 * s, y - 122 * s, x + 34 * s, y - 54 * s]
    draw.ellipse(head, fill="#ffd7b5", outline="#8a5a44", width=max(2, int(3 * s)))
    draw.arc((x - 28 * s, y - 130 * s, x + 28 * s, y - 76 * s), 190, 350, fill="#7b4a32", width=max(4, int(7 * s)))
    eye_y = y - 92 * s
    if face == "sad":
        draw.arc((x - 17 * s, y - 80 * s, x + 17 * s, y - 50 * s), 200, 340, fill="#5d4037", width=max(2, int(3 * s)))
    elif face == "angry":
        draw.line((x - 22 * s, eye_y - 6 * s, x - 8 * s, eye_y), fill="#5d4037", width=max(2, int(3 * s)))
        draw.line((x + 8 * s, eye_y, x + 22 * s, eye_y - 6 * s), fill="#5d4037", width=max(2, int(3 * s)))
        draw.arc((x - 16 * s, y - 72 * s, x + 16 * s, y - 52 * s), 20, 160, fill="#5d4037", width=max(2, int(3 * s)))
    elif face == "scared":
        draw.ellipse((x - 8 * s, y - 76 * s, x + 8 * s, y - 58 * s), outline="#5d4037", width=max(2, int(3 * s)))
    else:
        draw.arc((x - 18 * s, y - 84 * s, x + 18 * s, y - 56 * s), 20, 160, fill="#5d4037", width=max(2, int(3 * s)))
    draw.ellipse((x - 18 * s, eye_y - 4 * s, x - 10 * s, eye_y + 4 * s), fill="#3a2b25")
    draw.ellipse((x + 10 * s, eye_y - 4 * s, x + 18 * s, eye_y + 4 * s), fill="#3a2b25")

    if pose == "sit":
        draw.rounded_rectangle((x - 34 * s, y - 54 * s, x + 34 * s, y + 20 * s), radius=int(15 * s), fill=shirt, outline="#4f7ca8", width=max(2, int(3 * s)))
        draw.line((x - 22 * s, y + 20 * s, x - 58 * s, y + 48 * s), fill="#424242", width=max(5, int(8 * s)))
        draw.line((x + 22 * s, y + 20 * s, x + 58 * s, y + 48 * s), fill="#424242", width=max(5, int(8 * s)))
        draw.line((x - 36 * s, y - 30 * s, x - 70 * s, y - 2 * s), fill="#ffd7b5", width=max(5, int(8 * s)))
        draw.line((x + 36 * s, y - 30 * s, x + 70 * s, y - 2 * s), fill="#ffd7b5", width=max(5, int(8 * s)))
    else:
        draw.rounded_rectangle((x - 34 * s, y - 54 * s, x + 34 * s, y + 58 * s), radius=int(16 * s), fill=shirt, outline="#4f7ca8", width=max(2, int(3 * s)))
        draw.line((x - 18 * s, y + 58 * s, x - 34 * s, y + 104 * s), fill="#424242", width=max(5, int(8 * s)))
        draw.line((x + 18 * s, y + 58 * s, x + 34 * s, y + 104 * s), fill="#424242", width=max(5, int(8 * s)))
        if pose == "wave":
            draw.line((x - 36 * s, y - 28 * s, x - 72 * s, y - 76 * s), fill="#ffd7b5", width=max(5, int(8 * s)))
            draw.line((x + 36 * s, y - 28 * s, x + 72 * s, y - 8 * s), fill="#ffd7b5", width=max(5, int(8 * s)))
        elif pose == "point":
            draw.line((x + 36 * s, y - 28 * s, x + 88 * s, y - 48 * s), fill="#ffd7b5", width=max(5, int(8 * s)))
            draw.line((x - 36 * s, y - 28 * s, x - 68 * s, y - 4 * s), fill="#ffd7b5", width=max(5, int(8 * s)))
        elif pose == "run":
            draw.line((x - 36 * s, y - 28 * s, x - 70 * s, y + 8 * s), fill="#ffd7b5", width=max(5, int(8 * s)))
            draw.line((x + 36 * s, y - 28 * s, x + 80 * s, y - 64 * s), fill="#ffd7b5", width=max(5, int(8 * s)))
        else:
            draw.line((x - 36 * s, y - 28 * s, x - 68 * s, y - 2 * s), fill="#ffd7b5", width=max(5, int(8 * s)))
            draw.line((x + 36 * s, y - 28 * s, x + 68 * s, y - 2 * s), fill="#ffd7b5", width=max(5, int(8 * s)))


def draw_book(draw, x, y, open_book=True):
    if open_book:
        draw.polygon([(x, y), (x - 86, y - 24), (x - 86, y + 58), (x, y + 82)], fill="#fff7d6", outline="#7aa6d8")
        draw.polygon([(x, y), (x + 86, y - 24), (x + 86, y + 58), (x, y + 82)], fill="#fff7d6", outline="#7aa6d8")
        draw.line((x, y, x, y + 82), fill="#7aa6d8", width=4)
    else:
        draw.rounded_rectangle((x - 80, y - 48, x + 80, y + 58), radius=14, fill="#7aa6d8", outline="#4b6f95", width=5)


def draw_bag(draw, x, y):
    draw.rounded_rectangle((x - 54, y - 28, x + 54, y + 70), radius=16, fill="#ff9dbd", outline="#b8577a", width=5)
    draw.arc((x - 32, y - 64, x + 32, y - 6), 180, 360, fill="#b8577a", width=8)
    draw.rounded_rectangle((x - 30, y + 4, x + 30, y + 34), radius=10, fill="#ffd1df", outline="#b8577a", width=3)


def draw_door(draw, x, y, open_door=False):
    draw.rectangle((x - 64, y - 150, x + 64, y + 88), fill="#f3ddbd", outline="#9a6a42", width=8)
    if open_door:
        draw.polygon([(x - 48, y - 132), (x + 74, y - 154), (x + 74, y + 66), (x - 48, y + 84)], fill="#d99a5f", outline="#8a5a35")
        draw.ellipse((x + 34, y - 22, x + 48, y - 8), fill="#f5d45e")
    else:
        draw.ellipse((x + 32, y - 26, x + 48, y - 10), fill="#f5d45e")


def draw_cabinet(draw, x, y):
    draw.rounded_rectangle((x - 86, y - 106, x + 86, y + 110), radius=18, fill="#d9a66f", outline="#8d613c", width=7)
    draw.line((x, y - 100, x, y + 104), fill="#8d613c", width=5)
    draw.ellipse((x - 22, y - 2, x - 8, y + 12), fill="#f7d66c")
    draw.ellipse((x + 8, y - 2, x + 22, y + 12), fill="#f7d66c")


def draw_table(draw, x, y):
    draw.rounded_rectangle((x - 100, y - 62, x + 100, y - 28), radius=12, fill="#b9835a", outline="#75513a", width=5)
    for lx in (x - 72, x + 72):
        draw.rounded_rectangle((lx - 10, y - 28, lx + 10, y + 96), radius=8, fill="#8f6141")


def draw_food(draw, x, y, kind):
    if kind == "sandwich":
        draw.polygon([(x - 70, y + 40), (x, y - 60), (x + 70, y + 40)], fill="#f2c978", outline="#a56c38")
        draw.polygon([(x - 58, y + 28), (x, y - 42), (x + 58, y + 28)], fill="#f7efd0", outline="#a56c38")
        draw.rectangle((x - 42, y + 0, x + 42, y + 14), fill="#79b866")
    elif kind == "salad":
        draw.ellipse((x - 82, y - 26, x + 82, y + 52), fill="#cfeef8", outline="#6ca3ad", width=5)
        for dx, dy, col in [(-36, 0, "#6bbf59"), (0, -12, "#8ed66f"), (34, 6, "#ff8a7a"), (18, 24, "#f7d66c")]:
            draw.ellipse((x + dx - 24, y + dy - 18, x + dx + 24, y + dy + 18), fill=col)
    elif kind == "sweets":
        for dx, col in [(-48, "#ff77a8"), (0, "#77c6ff"), (48, "#ffd66c")]:
            draw.ellipse((x + dx - 24, y - 22, x + dx + 24, y + 26), fill=col, outline="#8c6680", width=4)
            draw.polygon([(x + dx - 24, y), (x + dx - 46, y - 18), (x + dx - 44, y + 18)], fill=col)
            draw.polygon([(x + dx + 24, y), (x + dx + 46, y - 18), (x + dx + 44, y + 18)], fill=col)
    elif kind == "biscuits":
        for dx in (-36, 22):
            draw.ellipse((x + dx - 34, y - 34, x + dx + 34, y + 34), fill="#c98e50", outline="#8a5a32", width=4)
            for px, py in [(-12, -8), (8, 12), (16, -12)]:
                draw.ellipse((x + dx + px - 5, y + py - 5, x + dx + px + 5, y + py + 5), fill="#6a3e23")
    elif kind == "crisps":
        for i in range(7):
            dx = -60 + i * 20
            draw.ellipse((x + dx - 15, y - 20 + (i % 2) * 8, x + dx + 15, y + 20 + (i % 2) * 8), fill="#f3cf55", outline="#c49a28", width=3)
    else:
        draw.ellipse((x - 62, y - 30, x + 62, y + 40), fill="#f3cf55", outline="#b68d2d", width=4)


def draw_small_pet(draw, x, y, kind="cat"):
    if kind == "dog":
        fill = "#c7834c"
        ear = "#8a5734"
    else:
        fill = "#f0b36e"
        ear = "#d98f52"
    draw.ellipse((x - 54, y - 44, x + 54, y + 42), fill=fill, outline="#6d4b3a", width=4)
    draw.polygon([(x - 38, y - 32), (x - 18, y - 82), (x + 0, y - 28)], fill=ear, outline="#6d4b3a")
    draw.polygon([(x + 38, y - 32), (x + 18, y - 82), (x + 0, y - 28)], fill=ear, outline="#6d4b3a")
    draw.ellipse((x - 20, y - 10, x - 8, y + 2), fill="#3a2b25")
    draw.ellipse((x + 8, y - 10, x + 20, y + 2), fill="#3a2b25")
    draw.ellipse((x - 7, y + 10, x + 7, y + 24), fill="#3a2b25")


def draw_expression(text, unit):
    img, draw = new_canvas()
    draw_floor(draw)
    t = text.lower()

    if "cabinet" in t or "cupboard" in t:
        draw_cabinet(draw, 298, 264)
        if "doll" in t:
            if "under" in t:
                draw.ellipse((228, 348, 276, 396), fill="#ffd7b5", outline="#7a5b48", width=3)
                draw.rounded_rectangle((238, 388, 308, 442), radius=16, fill="#ff9bd1", outline="#9b5f86", width=3)
            elif "on" in t:
                draw.ellipse((260, 98, 310, 148), fill="#ffd7b5", outline="#7a5b48", width=3)
                draw.rounded_rectangle((252, 144, 318, 208), radius=16, fill="#ff9bd1", outline="#9b5f86", width=3)
            else:
                draw.ellipse((278, 232, 326, 280), fill="#ffd7b5", outline="#7a5b48", width=3)
                draw.rounded_rectangle((268, 278, 338, 338), radius=16, fill="#ff9bd1", outline="#9b5f86", width=3)
        elif "kite" in t:
            paste_asset(img, "Imagens/unit4/kite.png", (58, 156, 220, 330))
            draw_arrow(draw, (176, 270), (258, 282))
        else:
            draw_kid(draw, 132, 344, pose="point", scale=0.75)
    elif "couch" in t or "sofa" in t:
        paste_asset(img, "Imagens/words/couch.png", (170, 160, 440, 386))
        if "cat" in t:
            draw_small_pet(draw, 220, 376, "cat")
        else:
            draw_kid(draw, 116, 340, pose="point", scale=0.72)
    elif "table" in t:
        draw_table(draw, 286, 276)
        if "under" in t:
            draw_small_pet(draw, 286, 376, "cat")
        draw_kid(draw, 116, 344, pose="point", scale=0.7)
    elif "door" in t:
        draw_door(draw, 310, 268, open_door="open" in t)
        draw_kid(draw, 150, 352, pose="point" if "open" in t else "wave", scale=0.76)
    elif "book" in t:
        draw_kid(draw, 180, 348, pose="sit", scale=0.78)
        draw_book(draw, 312, 292, open_book="open" in t)
    elif "pencil" in t:
        draw_kid(draw, 178, 344, pose="point", scale=0.78)
        paste_asset(img, "Imagens/unit1/pencil.png", (280, 196, 434, 338))
        draw_arrow(draw, (200, 300), (314, 268))
    elif "bag" in t:
        draw_table(draw, 310, 286)
        draw_bag(draw, 160, 306)
        draw_arrow(draw, (180, 312), (302, 240))
    elif "stand up" in t:
        draw_kid(draw, 258, 334, pose="stand", scale=0.95)
        draw_arrow(draw, (258, 374), (258, 164))
    elif "sit down" in t:
        draw_kid(draw, 258, 330, pose="sit", scale=0.95)
        draw_arrow(draw, (258, 154), (258, 288))
    elif "brother" in t:
        draw_kid(draw, 190, 354, shirt="#7bc8ff", scale=0.78)
        draw_kid(draw, 315, 354, shirt="#9be17d", scale=0.78)
    elif "mum" in t:
        draw_kid(draw, 178, 356, pose="wave", scale=0.72)
        draw_kid(draw, 324, 334, shirt="#f2a0ca", pose="wave", scale=0.92)
    elif "sandwich" in t:
        draw_food(draw, 292, 270, "sandwich")
        draw_kid(draw, 138, 354, pose="point", scale=0.76)
    elif "happy" in t:
        draw_kid(draw, 256, 348, face="happy", pose="wave", scale=0.95)
    elif "angry" in t:
        draw_kid(draw, 256, 348, face="angry", scale=0.95, shirt="#ff9b8a")
    elif "sad" in t:
        draw_kid(draw, 256, 348, face="sad", scale=0.95, shirt="#8ac4ff")
    elif "scared" in t:
        draw_kid(draw, 256, 348, face="scared", scale=0.95, shirt="#c6a4ff")
        draw.polygon([(380, 185), (408, 245), (350, 245)], fill="#d2c2ff", outline="#8b75c7", width=4)
    elif "eyes" in t:
        draw_kid(draw, 256, 348, scale=0.95)
        if "close" in t:
            draw.line((228, 248, 242, 248), fill="#2d2d2d", width=5)
            draw.line((270, 248, 284, 248), fill="#2d2d2d", width=5)
        else:
            draw.ellipse((220, 238, 248, 266), fill="#ffffff", outline="#2d2d2d", width=3)
            draw.ellipse((264, 238, 292, 266), fill="#ffffff", outline="#2d2d2d", width=3)
    elif "hug" in t:
        draw_kid(draw, 222, 354, shirt="#7bc8ff", scale=0.8)
        draw_kid(draw, 292, 354, shirt="#ffb3c9", scale=0.8)
        draw.arc((190, 244, 324, 370), 200, 340, fill="#e85d89", width=8)
    elif "ball" in t:
        paste_asset(img, "Imagens/unit4/ball.png", (274, 142, 430, 296))
        draw_kid(draw, 142, 352, pose="point", scale=0.78)
        if "throw" in t:
            draw_arrow(draw, (184, 258), (330, 196))
        elif "catch" in t:
            draw_arrow(draw, (362, 198), (190, 260))
        elif "bounce" in t:
            draw_arrow(draw, (356, 192), (356, 328))
    elif "kite" in t:
        paste_asset(img, "Imagens/unit4/kite.png", (250, 90, 438, 278), alpha=130 if "haven" in t else 255)
        draw_kid(draw, 150, 356, pose="point", scale=0.78)
        if "haven" in t:
            draw.line((250, 112, 428, 276), fill="#e85d89", width=10)
    elif "rabbit" in t:
        paste_asset(img, "Imagens/unit6/rabbit.png", (250, 150, 428, 324))
        draw_kid(draw, 126, 354, pose="point", scale=0.72)
        if "hop" in t:
            draw_arrow(draw, (310, 326), (376, 248))
        elif "sniff" in t:
            for r in (16, 30, 44):
                draw.arc((222 - r, 218 - r, 222 + r, 218 + r), 300, 60, fill="#88b7dc", width=4)
        elif "eat" in t:
            paste_asset(img, "Imagens/unit7/carrots.png", (144, 254, 246, 356))
    elif "dog" in t:
        paste_asset(img, "Imagens/unit6/dog.png", (256, 180, 432, 336))
        draw_kid(draw, 126, 354, pose="run", scale=0.75)
        draw_arrow(draw, (300, 350), (410, 332))
    elif "color" in t or "colours" in t or "colors" in t:
        draw_kid(draw, 142, 354, pose="point", scale=0.75)
        for i, col in enumerate(["#ff8a38", "#59b9ff", "#7bd66d", "#d28bff"]):
            draw.ellipse((252 + i * 38, 210 + (i % 2) * 30, 302 + i * 38, 260 + (i % 2) * 30), fill=col, outline="#7c6f68", width=3)
    elif "carrots" in t:
        paste_asset(img, "Imagens/unit7/carrots.png", (258, 170, 428, 328), alpha=125 if "don't" in t else 255)
        draw_kid(draw, 132, 354, pose="point", face="sad" if "don't" in t else "happy", scale=0.78)
        if "don't" in t:
            draw.line((264, 178, 422, 324), fill="#e85d89", width=10)
    elif "smell" in t:
        draw_food(draw, 312, 302, "crisps")
        draw_kid(draw, 132, 354, pose="point", scale=0.75)
        for x in (286, 322, 358):
            draw.arc((x - 16, 190, x + 16, 260), 95, 270, fill="#9dc7c7", width=5)
    elif "hungry" in t:
        draw_kid(draw, 154, 354, face="sad", scale=0.75)
        draw_food(draw, 324, 282, "sandwich")
    elif "kitchen" in t:
        draw.rounded_rectangle((245, 145, 430, 342), radius=22, fill="#dbeefa", outline="#7ca5bf", width=6)
        draw_food(draw, 338, 282, "salad")
        draw_kid(draw, 130, 356, pose="point", scale=0.72)
        draw_arrow(draw, (188, 304), (264, 270))
    elif "take one" in t or "eat the chip" in t or "yummy" in t:
        draw_kid(draw, 160, 354, pose="point", face="happy", scale=0.76)
        draw_food(draw, 326, 282, "crisps")
        if "eat" in t:
            draw_arrow(draw, (326, 282), (194, 258))
    elif "bike" in t:
        paste_asset(img, "Imagens/unit8/bike.png", (218, 208, 426, 370))
        draw_kid(draw, 230, 296, pose="sit", scale=0.65)
        if "you" in t:
            draw_kid(draw, 110, 354, pose="point", scale=0.65)
    elif "fun" in t:
        paste_asset(img, "Imagens/unit8/bus.png", (258, 186, 438, 326))
        draw_kid(draw, 120, 354, pose="wave", scale=0.68)
        draw_kid(draw, 190, 354, pose="wave", shirt="#ffb3c9", scale=0.68)
    elif "thank" in t:
        draw_kid(draw, 180, 354, pose="wave", scale=0.75)
        draw_kid(draw, 322, 354, pose="wave", shirt="#ffb3c9", scale=0.75)
        draw.ellipse((238, 170, 276, 208), fill="#ff77a8")
    elif "biscuits" in t:
        draw_food(draw, 318, 274, "biscuits")
        draw_kid(draw, 138, 354, pose="point", scale=0.76)
    elif "crisps" in t:
        draw_food(draw, 318, 274, "crisps")
        draw_kid(draw, 138, 354, pose="point", scale=0.76)
    elif "salad" in t:
        draw_food(draw, 318, 274, "salad")
        draw_kid(draw, 138, 354, pose="point", scale=0.76)
    elif "sweets" in t:
        draw_food(draw, 318, 274, "sweets")
        draw_kid(draw, 138, 354, pose="point", scale=0.76)
    elif "nice work" in t:
        draw_kid(draw, 256, 350, pose="wave", face="happy", scale=0.9)
        draw.ellipse((182, 120, 330, 212), fill="#fff3a6", outline="#e0b645", width=5)
        draw.polygon([(256, 118), (278, 170), (334, 174), (290, 208), (306, 262), (256, 232), (206, 262), (222, 208), (178, 174), (234, 170)], fill="#ffd74d", outline="#cc9b1f")
    elif "walk home" in t:
        draw_kid(draw, 132, 354, pose="run", scale=0.72)
        draw.polygon([(300, 184), (420, 292), (180, 292)], fill="#ffb66e", outline="#9a5b35", width=5)
        draw.rectangle((214, 292, 386, 406), fill="#ffe1b8", outline="#9a5b35", width=5)
        draw_arrow(draw, (176, 324), (254, 294))
    elif "surprise" in t:
        draw_door(draw, 310, 268, open_door=True)
        draw_kid(draw, 154, 354, face="scared", scale=0.75)
        for x, y, col in [(360, 154, "#ff77a8"), (392, 208, "#77c6ff"), (342, 250, "#ffd66c")]:
            draw.ellipse((x - 16, y - 16, x + 16, y + 16), fill=col)
    elif "party hat" in t:
        draw_kid(draw, 246, 354, pose="wave", scale=0.86)
        paste_asset(img, "Imagens/unit9/hat.png", (212, 82, 296, 172))
        draw_arrow(draw, (250, 156), (250, 222))
    elif "dance" in t:
        draw_kid(draw, 190, 354, pose="wave", scale=0.72)
        draw_kid(draw, 314, 354, pose="wave", shirt="#ffb3c9", scale=0.72)
        draw.arc((154, 210, 354, 370), 205, 335, fill="#e85d89", width=8)
    else:
        draw_kid(draw, 182, 354, pose="wave", scale=0.78)
        draw_kid(draw, 318, 354, pose="wave", shirt="#ffb3c9", scale=0.78)

    return img


def main():
    for unit, expressions in EXPRESSIONS.items():
        out_dir = OUT_ROOT / unit
        out_dir.mkdir(parents=True, exist_ok=True)
        for text in expressions:
            img = draw_expression(text, unit)
            img.save(out_dir / f"{slug(text)}.png", optimize=True)


if __name__ == "__main__":
    main()
