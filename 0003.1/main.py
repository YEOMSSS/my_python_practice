# main.py (버튼 정리 + 체크버튼 적용 + 색상강조 버그 수정)

import tkinter as tk
import random
from functools import partial
from game_logic import (
    create_deck, deal_hand, sort_hand,
    evaluate_hand, compare_hands, bot_replace
)
from utils import get_card_color, color_mode
from deck_tracker import show_deck_status
from speed_control import open_speed_control, deal_speed

selected_cards = []
player_hand, bot_hand, deck = [], [], []
card_labels = []
bot_card_labels = []
game_in_progress = False  # 게임 상태 플래그 추가

root = tk.Tk()
root.title("파이썬 포커")
root.geometry("800x700")
root.configure(bg="darkgreen")

main_frame = tk.Frame(root, bg="darkgreen")
main_frame.pack(expand=True, anchor="center")

message_label = tk.Label(main_frame, text="게임을 시작하세요.", font=("Arial", 14), bg="darkgreen", fg="white")
message_label.pack(pady=10)

# 🃏 남은 카드 보기 버튼
deck_button = tk.Button(
    main_frame,
    text="🃏 남은 카드 수 보기",
    font=("Arial", 16, "bold"),
    fg="white",
    bg="darkred",
    padx=10, pady=5,
    relief="raised", bd=2,
    command=lambda: show_deck_status(root, deck, player_hand),
    state="disabled"
)
deck_button.pack(pady=5)

card_frame = tk.Frame(main_frame, bg="darkgreen")
card_frame.pack(pady=10, fill="x")

bot_frame = tk.Frame(main_frame, bg="darkgreen")
bot_frame.pack(pady=10, fill="x")

# 🎛️ 도구 버튼 (위쪽 줄)
tool_button_frame = tk.Frame(main_frame, bg="darkgreen")
tool_button_frame.pack(pady=(0, 5))

speed_button = tk.Button(tool_button_frame, text="⚙️ 속도 조절",
                         command=lambda: open_speed_control(root),
                         bg="dim gray", fg="white",
                         font=("Arial", 11, "bold"))
speed_button.pack(side="left", padx=5)

# 🎨 색상 강조 체크버튼
color_mode_var = tk.BooleanVar(value=color_mode)

def toggle_color_mode():
    import utils
    utils.color_mode = color_mode_var.get()
    update_cards()
    if game_in_progress:
        show_bot_back()
    message_label.config(text="🎨 색상 강조 ON" if utils.color_mode else "🎨 색상 강조 OFF")

color_check = tk.Checkbutton(tool_button_frame, text="🎨 색상 강조",
                             variable=color_mode_var,
                             command=toggle_color_mode,
                             font=("Arial", 11), bg="darkgreen",
                             fg="white", activebackground="darkgreen",
                             selectcolor="darkgreen")
color_check.pack(side="left", padx=5)

# ▶️ 게임 진행 버튼 (아래쪽 줄)
action_button_frame = tk.Frame(main_frame, bg="darkgreen")
action_button_frame.pack(pady=(5, 10))

start_button = tk.Button(action_button_frame, text="게임 시작", command=lambda: start_game(),
                         bg="forest green", fg="white", font=("Arial", 12, "bold"))
start_button.pack(side="left", padx=5)

replace_button = tk.Button(action_button_frame, text="카드 바꾸기", command=lambda: replace_cards(), state="disabled",
                           bg="forest green", fg="white", font=("Arial", 12, "bold"))
replace_button.pack(side="left", padx=5)

result_button = tk.Button(action_button_frame, text="결과 확인", command=lambda: show_result(), state="disabled",
                          bg="forest green", fg="white", font=("Arial", 12, "bold"))
result_button.pack(side="left", padx=5)

# 🎯 카드 선택 / 딜링 관련 함수들
def select_card(card_label, card_index, event):
    if card_index in selected_cards:
        selected_cards.remove(card_index)
        card_label.config(highlightthickness=0)
    else:
        selected_cards.append(card_index)
        card_label.config(highlightthickness=2, highlightbackground="red")

def update_cards():
    for widget in card_frame.winfo_children():
        widget.destroy()
    card_labels.clear()
    deal_player_cards()

def deal_player_cards(index=0):
    if index < len(player_hand):
        card = player_hand[index]
        card_label = tk.Label(
            card_frame, text=card,
            font=("Courier", 28, "bold"),
            width=4, height=3,
            relief="ridge", bd=3,
            bg="white", fg=get_card_color(card)
        )
        card_label.pack(side="left", padx=5)
        card_label.bind("<Button-1>", partial(select_card, card_label, index))
        card_labels.append(card_label)
        root.after(deal_speed, deal_player_cards, index + 1)

def show_bot_back():
    for widget in bot_frame.winfo_children():
        widget.destroy()
    for _ in range(5):
        tk.Label(
            bot_frame, text='🁠',
            font=("Courier", 28, "bold"),
            width=4, height=3,
            relief="ridge", bd=3,
            bg="white", fg="gray"
        ).pack(side="left", padx=5)

def show_bot_hand(index=0):
    if index == 0:
        for widget in bot_frame.winfo_children():
            widget.destroy()
        bot_card_labels.clear()
    if index < len(bot_hand):
        card = bot_hand[index]
        label = tk.Label(
            bot_frame, text=card,
            font=("Courier", 28, "bold"),
            width=4, height=3,
            relief="ridge", bd=3,
            bg="white", fg=get_card_color(card)
        )
        label.pack(side="left", padx=5)
        bot_card_labels.append(label)
        root.after(deal_speed, show_bot_hand, index + 1)

# 상태 업데이트

def update_deck_count():
    deck_button.config(text=f"🃏 남은 카드 수 보기 ({len(deck)}장)")
    deck_button.config(state="normal" if deck else "disabled")

# 게임 시작 흐름
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
    show_bot_back()
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
    show_bot_back()
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
    show_bot_hand()
    update_deck_count()

def format_hand_summary(name, values):
    rank_map = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    readable = [rank_map[v] for v in values]
    if name == "Full House":
        return f"{name} ({readable[0]})"
    elif name in ["One Pair", "Three of a Kind", "Four of a Kind"]:
        return f"{name} ({readable[0]})"
    elif name == "Two Pair":
        return f"{name} ({readable[0]} & {readable[1]})"
    elif name in ["High Card", "Flush", "Straight", "Straight Flush", "Royal Flush"]:
        return f"{name} ({readable[0]})"
    else:
        return name

root.mainloop()
