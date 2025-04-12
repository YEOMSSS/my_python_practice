# main.py

import tkinter as tk
import random
from functools import partial
from game_logic import (
    create_deck, deal_hand, sort_hand,
    evaluate_hand, compare_hands, bot_replace
)
from utils import get_card_color
from deck_tracker import show_deck_status

selected_cards = []
player_hand, bot_hand, deck = [], [], []
card_labels = []
bot_card_labels = []
deal_speed = 50

# 🟩 UI 설정
root = tk.Tk()
root.title("파이썬 포커")
root.geometry("800x650")
root.configure(bg="darkgreen")

main_frame = tk.Frame(root, bg="darkgreen")
main_frame.pack(expand=True)

message_label = tk.Label(main_frame, text="게임을 시작하세요.", font=("Arial", 14), bg="darkgreen", fg="white")
message_label.pack(pady=10)

# 🃏 덱 상태 보기 버튼
deck_button = tk.Button(
    main_frame,
    text="🃏 남은 카드 수 보기",
    font=("Arial", 16, "bold"),
    fg="white",
    bg="darkred",
    padx=10, pady=5,
    relief="raised", bd=2,
    command=lambda: show_deck_status(root, deck),
    state="disabled"
)
deck_button.pack(pady=5)

card_frame = tk.Frame(main_frame, bg="darkgreen", height=180)
card_frame.pack(pady=10)

bot_frame = tk.Frame(main_frame, bg="darkgreen", height=180)
bot_frame.pack(pady=10)

# 🎚️ 속도 조절
def update_speed(val):
    global deal_speed
    deal_speed = int(val)

speed_scale = tk.Scale(main_frame, from_=50, to=200, resolution=10,
                       orient="horizontal", label="카드 애니메이션 속도 (ms)",
                       command=update_speed, bg="darkgreen", fg="white",
                       troughcolor="gray", highlightthickness=0)
speed_scale.set(deal_speed)
speed_scale.pack(pady=5)

# 🎨 카드 선택 / 딜링
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
            bot_frame, text='🂠',
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

# 🔄 상태 업데이트
def update_deck_count():
    deck_button.config(text=f"🃏 남은 카드 수 보기 ({len(deck)}장)")
    deck_button.config(state="normal" if deck else "disabled")

# ▶️ 게임 시작 / 진행
def start_game():
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
    global player_hand
    if len(deck) < len(selected_cards):
        message_label.config(text="덱에 카드가 부족합니다!")
        return
    for idx in selected_cards[:]:
        if deck:
            player_hand[idx] = deck.pop()
    selected_cards.clear()
    player_hand[:] = sort_hand(player_hand)
    update_cards()
    show_bot_back()
    message_label.config(
        text="⚠️ 덱 소진! 이제 결과를 확인하세요." if not deck else f"교체 완료. 남은 카드 수: {len(deck)}장"
    )
    if not deck:
        replace_button.config(state="disabled")
    update_deck_count()

def show_result():
    start_button.config(state="normal")
    global bot_hand
    if deck:
        bot_hand = sort_hand(bot_replace(bot_hand, deck))
    pe, be = evaluate_hand(player_hand), evaluate_hand(bot_hand)
    result = compare_hands(pe, be)
    result_text = f"Player: {pe[0]}\nBot: {be[0]}\n"
    result_text += "🎉 Player 승리!" if result == "player" else "🤖 Bot 승리!" if result == "bot" else "무승부!"
    message_label.config(text=result_text)
    replace_button.config(state="disabled")
    result_button.config(state="disabled")
    show_bot_hand()
    update_deck_count()

# 🧩 버튼
start_button = tk.Button(main_frame, text="게임 시작", command=start_game,
                         bg="forest green", fg="white", font=("Arial", 12, "bold"))
start_button.pack(pady=5)

replace_button = tk.Button(main_frame, text="카드 바꾸기", command=replace_cards, state="disabled",
                           bg="forest green", fg="white", font=("Arial", 12, "bold"))
replace_button.pack(pady=5)

result_button = tk.Button(main_frame, text="결과 확인", command=show_result, state="disabled",
                          bg="forest green", fg="white", font=("Arial", 12, "bold"))
result_button.pack(pady=5)

root.mainloop()
