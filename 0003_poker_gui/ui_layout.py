import tkinter as tk
from utils import get_card_color
from ui_style import current_theme as style
from speed_control import open_speed_control, get_deal_speed

# 🎴 카드 표시용 프레임(컨테이너)을 생성합니다.
# 카드 한 장을 담을 수 있는 일정 크기의 프레임입니다.
def create_card_container(parent):
    container = tk.Frame(parent,
                         width=style["CARD_WIDTH"],
                         height=style["CARD_HEIGHT"],
                         bg=style["TABLE_BG"])  # ✅ 배경 통일
    container.pack_propagate(False)
    container.pack(side="left", padx=5)
    return container

# 🃏 실제 카드(텍스트/색상)를 표시하는 Label을 생성합니다.
# 선택 가능 여부에 따라 클릭 이벤트도 바인딩할 수 있습니다.
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

# 👤 플레이어 핸드를 애니메이션처럼 순차적으로 화면에 표시합니다.
# 카드 하나씩 딜레이 주며 보여줌
def render_player_hand(frame, hand, select_callback, card_labels, root):
    def deal(index=0):
        if index < len(hand):
            card = hand[index]
            container = create_card_container(frame)
            label = create_card_label(container, card, get_card_color(card),
                                      selectable=True,
                                      select_callback=select_callback, index=index)
            card_labels.append(label)
            root.after(get_deal_speed(), lambda: deal(index + 1))  # ✅ 여기!
    deal()

# 🤖 봇 핸드를 뒷면 카드(🁠)로 비공개 상태로 렌더링합니다.
def render_bot_back(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    for _ in range(5):
        container = create_card_container(frame)
        create_card_label(container, "🁠", fg="gray")

# 🤖 봇 핸드를 실제 카드 내용으로 공개하여 렌더링합니다.
# 순차적으로 딜레이 주며 보여줌
def render_bot_hand(frame, hand, bot_card_labels, root):
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
            root.after(get_deal_speed(), lambda: deal(index + 1))  # ✅ 여기!
    deal()
