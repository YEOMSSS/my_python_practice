import tkinter as tk
import ui_style
from utils import get_card_color
from ui_layout import create_card_container, create_card_label

log_records = []  # 로그는 문자열로 저장
log_window = None

def refresh_if_open():
    if log_window and log_window.winfo_exists():
        update_log_ui()

# 📜 로그를 기록합니다.
def log_event(label, hand):
    log_records.append((label, list(hand)))
    if log_window and log_window.winfo_exists():
        update_log_ui()

# 📋 로그 창을 표시합니다.
def open_log_window(root):
    global log_window
    if log_window and log_window.winfo_exists():
        log_window.lift()
        return

    style = ui_style.current_theme
    log_window = tk.Toplevel(root)
    log_window.title("플레이 로그")
    log_window.configure(bg=style["TABLE_BG"])
    log_window.geometry(f"420x420+{root.winfo_x() + 100}+{root.winfo_y() + 150}")

    update_log_ui()

# 🔄 로그 UI를 갱신합니다.
def update_log_ui():
    style = ui_style.current_theme

    for widget in log_window.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(log_window, bg=style["TABLE_BG"])
    scrollbar = tk.Scrollbar(log_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    frame = tk.Frame(canvas, bg=style["TABLE_BG"])
    canvas.create_window((0, 0), window=frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)

    for label, hand in log_records:
        title = tk.Label(frame, text=label, font=("Arial", 11, "bold"),
                         fg=style["TEXT_COLOR"], bg=style["TABLE_BG"])
        title.pack(anchor="w", padx=10, pady=(10, 2))

        hand_frame = tk.Frame(frame, bg=style["TABLE_BG"])
        hand_frame.pack(anchor="w", padx=10, pady=(0, 10))

        for card in hand:
            container = tk.Frame(hand_frame, width=65, height=65, bg=style["TABLE_BG"])
            container.propagate(False)
            container.pack(side="left", padx=3)
            label = tk.Label(container, text=card, font=style["DECK_FONT"],
                             bg=style["CARD_BG"], fg=get_card_color(card),
                             relief="ridge", bd=2)
            label.pack(fill="both", expand=True)
        
    log_window.after(100, lambda: canvas.yview_moveto(1.0))

