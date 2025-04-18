
import tkinter as tk
import subprocess
import os
import sys

def start_game(event=None):
    root.destroy()
    game_script = os.path.join(os.path.dirname(__file__), "main_final_restored_ui.py")
    subprocess.Popen([sys.executable, game_script])

root = tk.Tk()
root.title("남두육성")
root.attributes("-fullscreen", True)

# 타이틀 라벨
title_label = tk.Label(root, text="남두육성", font=("Helvetica", 48, "bold"))
title_label.place(relx=0.5, rely=0.4, anchor="center")

# 안내 문구
click_label = tk.Label(root, text="Click anywhere to start", font=("Arial", 14))
click_label.place(relx=0.5, rely=0.52, anchor="center")

# 마우스 클릭으로 시작
root.bind("<Button-1>", start_game)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

root.mainloop()
