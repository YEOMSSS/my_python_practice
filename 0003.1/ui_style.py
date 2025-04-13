# ui_style.py

# ========================
# 🎨 테마 정의 (딕셔너리)
# ========================

dark_theme = {
    "TABLE_BG": "#1A1A1A",
    "TEXT_COLOR": "white",
    "CARD_FONT": ("Garamond", 22, "bold"),
    "DECK_FONT": ("Garamond", 16, "bold"),
    "CARD_BG": "ivory",
    "CARD_FG_DEFAULT": "black",
    "CARD_WIDTH": 100,
    "CARD_HEIGHT": 150,
    "CARD_RELIEF": "groove",
    "HIGHLIGHT_COLOR": "gold"
}

light_theme = {
    "TABLE_BG": "#F0F0F0",
    "TEXT_COLOR": "#222222",
    "CARD_FONT": ("Garamond", 22, "bold"),
    "DECK_FONT": ("Garamond", 16, "bold"),
    "CARD_BG": "white",
    "CARD_FG_DEFAULT": "black",
    "CARD_WIDTH": 100,
    "CARD_HEIGHT": 150,
    "CARD_RELIEF": "solid",
    "HIGHLIGHT_COLOR": "#0077CC"
}

# ========================
# ⛓️ 현재 테마 선택
# ========================
current_theme = dark_theme

def toggle_theme():
    global current_theme
    current_theme = light_theme if current_theme == dark_theme else dark_theme
