# utils.py

color_mode = False  # 기본값: 빨강/검정

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
