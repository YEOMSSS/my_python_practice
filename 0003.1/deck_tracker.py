import tkinter as tk
from game_logic import create_deck
import utils
import ui_style  # ✅ 테마 딕셔너리

# 📦 현재 덱의 상태를 팝업 창으로 시각화하여 보여줍니다.
# 사용된 카드, 플레이어 손패, 남은 카드를 색상으로 구분해 표시합니다.
def show_deck_status(root, deck, player_hand=[]):
    style = ui_style.current_theme
    if not deck:
        return

    top = tk.Toplevel(root)
    top.title("현재 덱 현황")
    top.configure(bg=style["TABLE_BG"])

    width, height = 900, 300
    top.geometry(f"{width}x{height}+{root.winfo_x() + 100}+{root.winfo_y() + 100}")

    full_deck = create_deck()
    used_cards = set(full_deck) - set(deck)
    player_hand_set = set(player_hand)

    suits = ['♠', '♦', '♥', '♣']
    ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']

    table_frame = tk.Frame(top, bg=style["TABLE_BG"])
    table_frame.pack(expand=True, pady=20)

    for i, suit in enumerate(suits):
        for j, rank in enumerate(ranks):
            card = rank + suit
            if card in player_hand_set:
                bg_color = "yellow"
                fg_color = utils.get_card_color(card)
            elif card in used_cards:
                bg_color = style["CARD_BG"]
                fg_color = "gray"
            else:
                bg_color = style["CARD_BG"]
                fg_color = utils.get_card_color(card)

            # 카드 셀 (정사각형 고정)
            cell = tk.Frame(table_frame, width=60, height=60, bg=style["TABLE_BG"])
            cell.propagate(False)
            cell.grid(row=i, column=j, padx=2, pady=2)

            label = tk.Label(cell, text=card, font=style["DECK_FONT"],
                             bg=bg_color, fg=fg_color,
                             relief="ridge", bd=2)
            label.pack(fill="both", expand=True)
