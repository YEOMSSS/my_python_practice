# deck_tracker.py

import tkinter as tk
from game_logic import create_deck
from utils import get_card_color

def show_deck_status(root, deck):
    if not deck:
        return

    top = tk.Toplevel(root)
    top.title("카드 트래커")
    top.configure(bg="darkgreen")

    # 중앙 위치 & 넓은 창 설정
    width, height = 1100, 400
    top.geometry(f"{width}x{height}+{root.winfo_x() + 100}+{root.winfo_y() + 100}")

    full_deck = create_deck()
    used_cards = set(full_deck) - set(deck)

    suits = ['♠', '♥', '♦', '♣']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    table_frame = tk.Frame(top, bg="darkgreen")
    table_frame.pack(expand=True, pady=20)

    for j, rank in enumerate(ranks):
        label = tk.Label(table_frame, text=rank, font=("Arial", 12, "bold"),
                         bg="darkgreen", fg="white", width=4, pady=5)
        label.grid(row=0, column=j + 1)

    for i, suit in enumerate(suits):
        suit_label = tk.Label(table_frame, text=suit, font=("Arial", 14, "bold"),
                              bg="darkgreen", fg="white", width=2)
        suit_label.grid(row=i + 1, column=0, padx=5)

        for j, rank in enumerate(ranks):
            card = rank + suit
            is_used = card in used_cards
            color = "gray" if is_used else get_card_color(card)
            label = tk.Label(table_frame, text=card, font=("Courier", 20, "bold"),
                             width=4, height=2, relief="ridge", bd=2,
                             bg="white", fg=color)
            label.grid(row=i + 1, column=j + 1, padx=2, pady=2)
