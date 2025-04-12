# speed_control.py

import tkinter as tk

deal_speed = 50  # 전역 변수로 정의

def update_speed(val):
    global deal_speed
    deal_speed = int(val)
    
# ✅ 업데이트된 open_speed_control - 인자 1개만 받는다!

def open_speed_control(root):
    top = tk.Toplevel(root)
    top.title("속도 설정")
    top.configure(bg="darkgreen")
    top.geometry("350x120+{}+{}".format(root.winfo_x() + 150, root.winfo_y() + 150))

    label = tk.Label(top, text="카드 애니메이션 속도 (ms)",
                     font=("Arial", 11, "bold"), bg="darkgreen", fg="white")
    label.pack(pady=(10, 0))

    scale = tk.Scale(top, from_=50, to=200, resolution=10,
                     orient="horizontal", command=update_speed,
                     bg="darkgreen", fg="white",
                     troughcolor="gray", highlightthickness=0,
                     length=250)
    scale.set(deal_speed)
    scale.pack(pady=5)
