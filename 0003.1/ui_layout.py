import tkinter as tk
from utils import get_card_color
from ui_style import current_theme as style

def create_card_container(parent):
    container = tk.Frame(parent,
                         width=style["CARD_WIDTH"],
                         height=style["CARD_HEIGHT"],
                         bg=style["TABLE_BG"])  # ✅ 배경 통일
    container.pack_propagate(False)
    container.pack(side="left", padx=5)
    return container

def create_card_label(container, text, fg,
                      selectable=False, select_callback=None, index=None):
    label = tk.Label(container, text=text,
                     font=style["CARD_FONT"],
                     width=4, height=3,
                     relief=style["CARD_RELIEF"], bd=3,
                     bg=style["CARD_BG"], fg=fg,
                     highlightthickness=0,
                     highlightbackground="white")  # 선택 시 색상은 main에서 제어
    label.pack(fill="both", expand=True)

    if selectable and select_callback and index is not None:
        from functools import partial
        label.bind("<Button-1>", partial(select_callback, label, index))

    return label

def render_player_hand(frame, hand, deal_speed, select_callback, card_labels, root):
    def deal(index=0):
        if index < len(hand):
            card = hand[index]
            container = create_card_container(frame)
            label = create_card_label(container, card, get_card_color(card),
                                      selectable=True,
                                      select_callback=select_callback, index=index)
            card_labels.append(label)
            root.after(deal_speed, deal, index + 1)
    deal()

def render_bot_back(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    for _ in range(5):
        container = create_card_container(frame)
        create_card_label(container, "🁠", fg="gray")

def render_bot_hand(frame, hand, deal_speed, bot_card_labels, root):
    def deal(index=0):
        if index == 0:
            bot_card_labels.clear()
            for widget in frame.winfo_children():
                widget.destroy()
        if index < len(hand):
            card = hand[index]
            container = create_card_container(frame)
            label = create_card_label(container, card, get_card_color(card))
            bot_card_labels.append(label)
            root.after(deal_speed, deal, index + 1)
    deal()
