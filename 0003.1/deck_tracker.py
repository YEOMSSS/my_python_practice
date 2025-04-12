# deck_tracker.py (업데이트됨)

import tkinter as tk
from game_logic import create_deck
import utils

def show_deck_status(root, deck, player_hand=[]):
    if not deck:
        return

    top = tk.Toplevel(root)
    top.title("현재 덱 현황")
    top.configure(bg="darkgreen")

    width, height = 1100, 400
    top.geometry(f"{width}x{height}+{root.winfo_x() + 100}+{root.winfo_y() + 100}")

    full_deck = create_deck()
    used_cards = set(full_deck) - set(deck)
    player_hand_set = set(player_hand)

    suits = ['♠', '♦', '♥', '♣']
    ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']

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
            if card in player_hand_set:
                bg_color = "yellow"
                fg_color = utils.get_card_color(card)
            elif card in used_cards:
                bg_color = "white"
                fg_color = "gray"
            else:
                bg_color = "white"
                fg_color = utils.get_card_color(card)

            label = tk.Label(table_frame, text=card, font=("Courier", 20, "bold"),
                             width=4, height=2, relief="ridge", bd=2,
                             bg=bg_color, fg=fg_color)
            label.grid(row=i + 1, column=j + 1, padx=2, pady=2)
