import tkinter as tk
from game_logic import create_deck
import utils
import ui_style  # ✅ 테마 딕셔너리

status_window = None  # 전역 참조
_cached_deck = []
_cached_hand = []

# 🔄 테마 변경 시 열려 있는 덱 창 갱신
def refresh_if_open():
    if status_window and status_window.winfo_exists():
        update_deck_ui()

# 📦 현재 덱의 상태를 팝업 창으로 시각화하여 보여줍니다.
# 사용된 카드, 플레이어 손패, 남은 카드를 색상으로 구분해 표시합니다.
def show_deck_status(root, deck, player_hand=[]):
    global status_window, _cached_deck, _cached_hand
    if not deck:
        return

    if status_window and status_window.winfo_exists():
        status_window.lift()
        return

    style = ui_style.current_theme
    status_window = tk.Toplevel(root)
    status_window.title("현재 덱 현황")
    status_window.geometry(f"900x300+{root.winfo_x() + 100}+{root.winfo_y() + 100}")

    _cached_deck = deck[:]
    _cached_hand = player_hand[:]

    update_deck_ui(deck, player_hand)

# ♻️ 테마 변경 또는 상태 업데이트용 렌더링 함수
def update_deck_ui(deck=None, player_hand=None, *, refresh_cache=False):
    global _cached_deck, _cached_hand
    style = ui_style.current_theme

    if not status_window or not status_window.winfo_exists():
        return

    status_window.configure(bg=style["TABLE_BG"])

    for widget in status_window.winfo_children():
        widget.destroy()

    if refresh_cache:
        if deck is not None:
            _cached_deck[:] = deck
        if player_hand is not None:
            _cached_hand[:] = player_hand

    deck = deck or _cached_deck
    player_hand = player_hand or _cached_hand

    full_deck = create_deck()
    used_cards = set(full_deck) - set(deck)
    player_hand_set = set(player_hand)

    suits = ['♠', '♦', '♥', '♣']
    ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']

    table_frame = tk.Frame(status_window, bg=style["TABLE_BG"])
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
