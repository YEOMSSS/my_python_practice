import tkinter as tk

# 🕒 전역 속도 설정
_deal_speed = 50  # 밑줄로 내부 변수임을 표시

# 🔄 getter 함수: 최신 속도 값을 외부에 제공
def get_deal_speed():
    return _deal_speed

# 슬라이더 이벤트로 속도 업데이트
def update_speed(val):
    global _deal_speed
    _deal_speed = int(val)

# ⚙️ 속도 설정 UI
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
    scale.set(_deal_speed)
    scale.pack(pady=5)
