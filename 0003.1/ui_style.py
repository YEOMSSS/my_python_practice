# ========================
# 🎨 테마 정의 (딕셔너리)
# ========================

# 🌑 다크 테마 스타일 정의
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

# ☀️ 라이트 테마 스타일 정의
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

# 🌓 현재 적용 중인 테마를 나타냅니다. 기본은 다크 테마입니다.
current_theme = dark_theme

# 🔄 현재 테마를 다크/라이트로 전환합니다.
def toggle_theme():
    global current_theme
    current_theme = light_theme if current_theme == dark_theme else dark_theme
