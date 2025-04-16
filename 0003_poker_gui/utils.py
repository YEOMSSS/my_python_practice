# utils.py

# 🔧 색상 강조 모드 설정 (True면 강조 색상, False면 기본 빨강/검정)
color_mode = False  # 기본값: 빨강/검정

# 🎨 카드의 무늬(♠, ♥ 등)에 따라 글자 색상을 반환합니다.
# color_mode 설정에 따라 강조 색상 또는 전통적 빨강/검정 색상 사용
def get_card_color(card):
    suit = card[-1]
    if color_mode:
        if suit == "♦":
            return "orange"
        elif suit == "♣":
            return "blue"
        elif suit == "♥":
            return "red"
        else:
            return "black"
    else:
        return "red" if suit in ["♥", "♦"] else "black"

def format_card(card):
    rank, suit = card[:-1], card[-1]
    return ("10" if rank == "T" else rank) + suit
