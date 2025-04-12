# utils.py

def get_card_color(card):
    return "red" if card[-1] in ["♥", "♦"] else "black"

def format_card(card):
    rank, suit = card[:-1], card[-1]
    return ("10" if rank == "T" else rank) + suit
