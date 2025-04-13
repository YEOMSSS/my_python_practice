import tkinter as tk
import random
from functools import partial

import ui_style
style = ui_style.current_theme

from game_logic import (
    create_deck, deal_hand, sort_hand,
    evaluate_hand, compare_hands, bot_replace
)
from utils import get_card_color, color_mode
from deck_tracker import show_deck_status
from speed_control import open_speed_control, deal_speed
from ui_layout import render_player_hand, render_bot_back, render_bot_hand

from ui_style import toggle_theme

selected_cards = []
player_hand, bot_hand, deck = [], [], []
card_labels = []
bot_card_labels = []
game_in_progress = False

root = tk.Tk()
root.title("파이썬 포커")
root.geometry("800x700")
root.configure(bg=style["TABLE_BG"])

main_frame = tk.Frame(root, bg=style["TABLE_BG"])
main_frame.pack(expand=True, anchor="center", pady=20)
message_label = tk.Label(main_frame, text="게임을 시작하세요.",
                         font=("Arial", 16, "bold"),
                         bg=style["TABLE_BG"], fg=style["TEXT_COLOR"])
message_label.pack(pady=10)

deck_button = tk.Button(
    main_frame,
    text="🃏 남은 카드 수 보기",
    font=("Arial", 14, "bold"),
    fg="white", bg="darkred",
    padx=10, pady=5, relief="raised", bd=2,
    command=lambda: show_deck_status(root, deck, player_hand),
    state="disabled"
)
deck_button.pack(pady=5)

card_frame = tk.Frame(main_frame, bg=style["TABLE_BG"])
card_frame.pack(pady=15, fill="x")

bot_frame = tk.Frame(main_frame, bg=style["TABLE_BG"])
bot_frame.pack(pady=15, fill="x")

color_mode_var = tk.BooleanVar(value=color_mode)
bot_visible_var = tk.BooleanVar(value=False)

tool_button_frame = tk.Frame(main_frame, bg=style["TABLE_BG"])
tool_button_frame.pack(pady=(5, 10))

def toggle_color_mode():
    import utils
    utils.color_mode = color_mode_var.get()
    update_cards()
    if game_in_progress and result_button["state"] == "normal":
        if bot_visible_var.get():
            render_bot_hand(bot_frame, bot_hand, deal_speed, bot_card_labels, root)
        else:
            render_bot_back(bot_frame)
    message_label.config(text="🎨 색상 강조 ON" if utils.color_mode else "🎨 색상 강조 OFF")

def toggle_bot_visibility():
    if game_in_progress and result_button["state"] == "normal":
        if bot_visible_var.get():
            render_bot_hand(bot_frame, bot_hand, deal_speed, bot_card_labels, root)
        else:
            render_bot_back(bot_frame)

tk.Button(tool_button_frame, text="⚙️ 속도 조절",
          command=lambda: open_speed_control(root),
          bg="dim gray", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=5)

tk.Checkbutton(tool_button_frame, text="🎨 색상 강조",
               variable=color_mode_var, command=toggle_color_mode,
               font=("Arial", 11), bg=style["TABLE_BG"], fg="white",
               activebackground=style["TABLE_BG"], selectcolor=style["TABLE_BG"]
).pack(side="left", padx=5)

tk.Checkbutton(tool_button_frame, text="🤖 봇 핸드 보기",
               variable=bot_visible_var, command=toggle_bot_visibility,
               font=("Arial", 11), bg=style["TABLE_BG"], fg="white",
               activebackground=style["TABLE_BG"], selectcolor=style["TABLE_BG"]
).pack(side="left", padx=5)

def apply_theme_refresh():
    global style
    ui_style.toggle_theme()
    style = ui_style.current_theme  # 새 테마 적용

    # 🌀 스타일 재적용
    root.configure(bg=style["TABLE_BG"])
    main_frame.configure(bg=style["TABLE_BG"])
    card_frame.configure(bg=style["TABLE_BG"])
    bot_frame.configure(bg=style["TABLE_BG"])
    tool_button_frame.configure(bg=style["TABLE_BG"])
    action_button_frame.configure(bg=style["TABLE_BG"])
    message_label.configure(bg=style["TABLE_BG"], fg=style["TEXT_COLOR"])

    # 버튼 재생성
    update_cards()
    if game_in_progress and result_button["state"] == "normal":
        if bot_visible_var.get():
            render_bot_hand(bot_frame, bot_hand, deal_speed, bot_card_labels, root)
        else:
            render_bot_back(bot_frame)

    message_label.config(text="🌗 테마 변경됨!")

# 토글 버튼 추가 (tool_button_frame에)
tk.Button(tool_button_frame, text="🌗 테마 전환",
          command=apply_theme_refresh,
          bg="dim gray", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=5)


action_button_frame = tk.Frame(main_frame, bg=style["TABLE_BG"])
action_button_frame.pack(pady=(5, 10))

def themed_button(text, command, state="normal"):
    return tk.Button(action_button_frame, text=text, command=command, state=state,
                     bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))

start_button = themed_button("게임 시작", lambda: start_game())
start_button.pack(side="left", padx=5)

replace_button = themed_button("카드 바꾸기", lambda: replace_cards(), state="disabled")
replace_button.pack(side="left", padx=5)

result_button = themed_button("결과 확인", lambda: show_result(), state="disabled")
result_button.pack(side="left", padx=5)

def select_card(card_label, card_index, event):
    if card_index in selected_cards:
        selected_cards.remove(card_index)
        card_label.config(highlightthickness=0)
    else:
        selected_cards.append(card_index)
        card_label.config(highlightthickness=2,
                          highlightbackground=style["HIGHLIGHT_COLOR"])

def update_cards():
    for widget in card_frame.winfo_children():
        widget.destroy()
    card_labels.clear()
    render_player_hand(card_frame, player_hand, deal_speed, select_card, card_labels, root)

def update_deck_count():
    deck_button.config(text=f"🃏 남은 카드 수 보기 ({len(deck)}장)")
    deck_button.config(state="normal" if deck else "disabled")

# 게임 흐름
def start_game():
    global game_in_progress
    game_in_progress = True
    start_button.config(state="disabled")
    global deck, player_hand, bot_hand
    selected_cards.clear()
    deck = create_deck()
    random.shuffle(deck)
    player_hand = sort_hand(deal_hand(deck))
    bot_hand = sort_hand(deal_hand(deck))
    update_cards()
    if bot_visible_var.get():
        render_bot_hand(bot_frame, bot_hand, deal_speed, bot_card_labels, root)
    else:
        render_bot_back(bot_frame)
    message_label.config(text="카드를 선택하고 바꿔주세요.")
    replace_button.config(state="normal")
    result_button.config(state="normal")
    update_deck_count()

def replace_cards():
    global player_hand, bot_hand
    if len(deck) < len(selected_cards):
        message_label.config(text="데크에 카드가 부족합니다!")
        return
    for idx in selected_cards[:]:
        if deck:
            player_hand[idx] = deck.pop()
    selected_cards.clear()
    player_hand[:] = sort_hand(player_hand)
    bot_hand[:] = sort_hand(bot_replace(bot_hand, deck))
    update_cards()
    if bot_visible_var.get():
        render_bot_hand(bot_frame, bot_hand, deal_speed, bot_card_labels, root)
    else:
        render_bot_back(bot_frame)
    message_label.config(
        text="⚠️ 데크 소진! 이제 결과를 확인하세요." if not deck else f"교체 완료. 남은 카드 수: {len(deck)}장"
    )
    if not deck:
        replace_button.config(state="disabled")
    update_deck_count()

def show_result():
    global game_in_progress
    game_in_progress = False
    start_button.config(state="normal")
    global bot_hand
    pe, be = evaluate_hand(player_hand), evaluate_hand(bot_hand)
    result = compare_hands(pe, be)
    player_summary = format_hand_summary(pe[0], pe[2])
    bot_summary = format_hand_summary(be[0], be[2])
    result_text = f"Player: {player_summary}\nBot: {bot_summary}\n"
    result_text += "🎉 Player 승리!" if result == "player" else "🤖 Bot 승리!" if result == "bot" else "무승부!"
    message_label.config(text=result_text)
    replace_button.config(state="disabled")
    result_button.config(state="disabled")
    render_bot_hand(bot_frame, bot_hand, deal_speed, bot_card_labels, root)
    update_deck_count()

def format_hand_summary(name, values):
    rank_map = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    readable = [rank_map[v] for v in values]
    if name == "Two Pair":
        return f"{name} ({readable[0]} & {readable[1]})"
    elif name in ["High Card", "One Pair", "Three of a Kind", "Four of a Kind",
                  "Full House", "Flush", "Straight", "Straight Flush", "Royal Flush"]:
        return f"{name} ({readable[0]})"
    else:
        return name

root.mainloop()
