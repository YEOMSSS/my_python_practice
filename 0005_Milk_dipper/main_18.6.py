
import tkinter as tk
import random
import json
import os

# Custom Tooltip class with delay
class Tooltip:
    def __init__(self, widget, text, delay=300):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.delay = delay
        self._after_id = None
        widget.bind("<Enter>", self.schedule)
        widget.bind("<Leave>", self.cancel)

    def schedule(self, event=None):
        self._after_id = self.widget.after(self.delay, self.show)

    def cancel(self, event=None):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None
        self.hide()

    def show(self):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 50
        y = self.widget.winfo_rooty() + 30
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("Arial", 10))
        label.pack(ipadx=1)

    def hide(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

from scorer import explain_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "jamo_point_table.json"), encoding="utf-8") as f:
    point_table = json.load(f)

CHOSUNG_LIST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
JUNGSUNG_LIST = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
JONGSUNG_LIST = ['', 'ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

double_initials = {('ㄱ', 'ㄱ'): 'ㄲ', ('ㄷ', 'ㄷ'): 'ㄸ', ('ㅂ', 'ㅂ'): 'ㅃ', ('ㅅ', 'ㅅ'): 'ㅆ', ('ㅈ', 'ㅈ'): 'ㅉ'}
double_finals = {
    ('ㄱ', 'ㅅ'): 'ㄳ', ('ㄴ', 'ㅈ'): 'ㄵ', ('ㄴ', 'ㅎ'): 'ㄶ',
    ('ㄹ', 'ㄱ'): 'ㄺ', ('ㄹ', 'ㅁ'): 'ㄻ', ('ㄹ', 'ㅂ'): 'ㄼ',
    ('ㄹ', 'ㅅ'): 'ㄽ', ('ㄹ', 'ㅌ'): 'ㄾ', ('ㄹ', 'ㅍ'): 'ㄿ',
    ('ㄹ', 'ㅎ'): 'ㅀ', ('ㅂ', 'ㅅ'): 'ㅄ',
    ('ㄱ', 'ㄱ'): 'ㄲ', ('ㅅ', 'ㅅ'): 'ㅆ'
}
compound_vowel_sets = {
    frozenset(['ㅗ', 'ㅏ']): 'ㅘ', frozenset(['ㅗ', 'ㅏ', 'ㅣ']): 'ㅙ',
    frozenset(['ㅜ', 'ㅓ']): 'ㅝ', frozenset(['ㅜ', 'ㅓ', 'ㅣ']): 'ㅞ',
    frozenset(['ㅗ', 'ㅣ']): 'ㅚ', frozenset(['ㅜ', 'ㅣ']): 'ㅟ', frozenset(['ㅡ', 'ㅣ']): 'ㅢ',
    frozenset(['ㅑ', 'ㅣ']): 'ㅒ', frozenset(['ㅕ', 'ㅣ']): 'ㅖ',
    frozenset(['ㅏ', 'ㅣ']): 'ㅐ', frozenset(['ㅓ', 'ㅣ']): 'ㅔ'
}

current = {
    '초성': random.choice(['ㄱ','ㄴ','ㅁ','ㅅ','ㅇ']),
    '중성': random.choice(['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ']),
    '종성': ''
}
middle_stack = [current['중성']]
active_part = '종성'
cho_stack = [current['초성']]
jung_stack = [current['중성']]
jong_stack = []
visual_labels = []



def combine_syllable():
    cho = CHOSUNG_LIST.index(current['초성'])
    jung = JUNGSUNG_LIST.index(current['중성'])
    jong = JONGSUNG_LIST.index(current['종성'])
    return chr(0xAC00 + (cho * 21 * 28) + (jung * 28) + jong)

def combine_if_possible(current_jamo, selected_jamo, combination_map):
    pair = (current_jamo, selected_jamo)
    reverse_pair = (selected_jamo, current_jamo)
    return combination_map.get(pair) or combination_map.get(reverse_pair)

def set_active(part):
    global active_part
    active_part = part
    update_status()

def select_jamo(val):
    global middle_stack
    if active_part == '초성':
        combined = combine_if_possible(current['초성'], val, double_initials)
        if combined:
            current['초성'] = combined
            if len(cho_stack) < 2:
                cho_stack.append(val)
        elif val in CHOSUNG_LIST:
            current['초성'] = val
            cho_stack[:] = [val]
    elif active_part == '중성':
        if val in JUNGSUNG_LIST:
            if val not in middle_stack:
                middle_stack.append(val)
            result = compound_vowel_sets.get(frozenset(middle_stack))
            if result:
                current['중성'] = result
                if val not in jung_stack and len(jung_stack) < 3:
                    jung_stack.append(val)
            else:
                current['중성'] = val
                middle_stack[:] = [val]
                jung_stack[:] = [val]
    elif active_part == '종성':
        combined = combine_if_possible(current['종성'], val, double_finals)
        if combined:
            current['종성'] = combined
            if len(jong_stack) < 2:
                jong_stack.append(val)
        elif val in JONGSUNG_LIST:
            current['종성'] = val
            jong_stack[:] = [val]
    update_status()
    update_result_window()
    update_visual_stack()
    refresh_choices()

def update_status():
    active_label.config(text=f"선택 중: {active_part}")

def update_result_window():
    result_label.config(text=combine_syllable())
    jamo_stack = cho_stack + jung_stack + jong_stack
    score, explanation, formula = explain_score(jamo_stack)
    score_label.config(text=f"점수: {score}")
    formula_label.config(text=formula)
    synergy_label.config(text="\n".join(explanation[-5:]))

def sorted_stack_for_display(part, stack):
    compound_display_order = {
        frozenset(['ㅗ', 'ㅏ']): ['ㅗ', 'ㅏ'], frozenset(['ㅗ', 'ㅏ', 'ㅣ']): ['ㅗ', 'ㅏ', 'ㅣ'],
        frozenset(['ㅜ', 'ㅓ']): ['ㅜ', 'ㅓ'], frozenset(['ㅜ', 'ㅓ', 'ㅣ']): ['ㅜ', 'ㅓ', 'ㅣ'],
        frozenset(['ㅗ', 'ㅣ']): ['ㅗ', 'ㅣ'], frozenset(['ㅜ', 'ㅣ']): ['ㅜ', 'ㅣ'],
        frozenset(['ㅡ', 'ㅣ']): ['ㅡ', 'ㅣ'], frozenset(['ㅏ', 'ㅣ']): ['ㅏ', 'ㅣ'],
        frozenset(['ㅓ', 'ㅣ']): ['ㅓ', 'ㅣ'], frozenset(['ㅕ', 'ㅣ']): ['ㅕ', 'ㅣ'], frozenset(['ㅑ', 'ㅣ']): ['ㅑ', 'ㅣ']
    }
    if part == '중성':
        return compound_display_order.get(frozenset(stack), stack)
    elif part == '종성':
        final_orders = {
            frozenset(['ㄱ','ㅅ']): ['ㄱ','ㅅ'], frozenset(['ㄴ','ㅈ']): ['ㄴ','ㅈ'], frozenset(['ㄴ','ㅎ']): ['ㄴ','ㅎ'],
            frozenset(['ㄹ','ㄱ']): ['ㄹ','ㄱ'], frozenset(['ㄹ','ㅁ']): ['ㄹ','ㅁ'], frozenset(['ㄹ','ㅂ']): ['ㄹ','ㅂ'],
            frozenset(['ㄹ','ㅅ']): ['ㄹ','ㅅ'], frozenset(['ㄹ','ㅌ']): ['ㄹ','ㅌ'], frozenset(['ㄹ','ㅍ']): ['ㄹ','ㅍ'],
            frozenset(['ㄹ','ㅎ']): ['ㄹ','ㅎ'], frozenset(['ㅂ','ㅅ']): ['ㅂ','ㅅ']
        }
        return final_orders.get(frozenset(stack), list(stack[::-1]))
    return stack

def update_visual_stack():
    from scorer import point_table
    parts = cho_stack + sorted_stack_for_display('중성', jung_stack) + sorted_stack_for_display('종성', jong_stack)
    labels = ['초성'] * len(cho_stack) + ['중성'] * len(jung_stack) + ['종성'] * len(jong_stack)
    
    for i in range(7):
        text = parts[i] if i < len(parts) else ''
        if i < len(labels):
            part_type = labels[i]
            color = {'초성': 'red', '중성': 'blue', '종성': 'green'}.get(part_type, 'black')
            score = f"+{point_table.get(text, 0)}" if text else ''
        else:
            color = 'black'
            score = ''
        visual_labels[i].config(text=text, fg=color)
        score_visual_labels[i].config(text=score, fg=color)
    

def refresh_choices():
    for widget in choice_frame.winfo_children():
        widget.destroy()
    base = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ',
            'ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ']
    for i, j in enumerate(random.sample(base, 9)):
        btn = tk.Button(choice_frame, text=j, width=6, height=2, font=('Arial', 16),
                        command=lambda val=j: select_jamo(val))
        btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        point = point_table.get(j, 1)
        Tooltip(btn, f"{j}: {point}점")

root = tk.Tk()
root.title("한글 자모 진화 게임")
main_frame = tk.Frame(root)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

result_label = tk.Label(main_frame, text=combine_syllable(), font=('Arial', 48))
result_label.grid(row=0, column=0, pady=10)

score_label = tk.Label(main_frame, text="점수: 0", font=('Arial', 16))
score_label.grid(row=1, column=0)

formula_label = tk.Label(main_frame, text="", font=('Arial', 14), fg="gray20")
formula_label.grid(row=2, column=0, pady=5)

synergy_label = tk.Label(main_frame, text="", font=("Arial", 12), fg="purple")
synergy_label.grid(row=8, column=0, pady=5)

score_visual_labels = []
visual_labels = []

visual_frame = tk.Frame(main_frame)
visual_frame.grid(row=3, column=0, pady=5)

for _ in range(7):
    col_frame = tk.Frame(visual_frame)
    col_frame.pack(side=tk.LEFT, padx=5)

    score_lbl = tk.Label(col_frame, text='', width=3, height=1, font=('Arial', 10))
    score_lbl.pack()

    visual_lbl = tk.Label(col_frame, text='', width=3, height=1, font=('Arial', 20), relief='groove')
    visual_lbl.pack()

    score_visual_labels.append(score_lbl)
    visual_labels.append(visual_lbl)

tk.Label(main_frame, text="초성/중성/종성을 선택 후 자모를 고르세요", font=("Arial", 12)).grid(row=4, column=0, pady=10)

active_label = tk.Label(main_frame, text="선택 중: 종성", font=("Arial", 14))
active_label.grid(row=5, column=0, pady=5)

btn_frame = tk.Frame(main_frame)
btn_frame.grid(row=6, column=0, pady=10)
for part in ['초성', '중성', '종성']:
    tk.Button(btn_frame, text=part, font=("Arial", 12), command=lambda p=part: set_active(p)).pack(side=tk.LEFT, padx=10)

choice_frame = tk.Frame(main_frame)
choice_frame.grid(row=7, column=0, pady=20)

def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)

is_fullscreen = False
def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)

root.bind("<Escape>", exit_fullscreen)
root.bind("<F11>", toggle_fullscreen)

update_status()
update_visual_stack()
refresh_choices()
update_result_window()


# 시너지 정보 프레임
synergy_info_frame = tk.Frame(root, bg='white', bd=2, relief='solid')
synergy_info_frame.place_forget()

synergy_text = tk.Text(synergy_info_frame, width=60, height=20, wrap="word", font=("Arial", 10))
synergy_text.pack(padx=10, pady=10)


def toggle_synergy_info():
    if synergy_info_frame.winfo_ismapped():
        synergy_info_frame.place_forget()
    else:
        synergy_info_frame.place(relx=0.5, rely=0.5, anchor="center")
        synergy_text.delete("1.0", tk.END)
        try:
            with open(os.path.join(BASE_DIR, "synergy_rules.json"), encoding="utf-8") as f:
                rules = json.load(f)
            for r in rules:
                synergy_text.insert(tk.END, f"• {r['desc']}\n")
                if 'condition_desc' in r and r['condition_desc']:
                    synergy_text.insert(tk.END, f"   └ 조건: {r['condition_desc']}\n\n")
        except Exception as e:
            synergy_text.insert(tk.END, f"시너지 정보를 불러올 수 없습니다: {e}")

synergy_btn = tk.Button(main_frame, text='📘 시너지 보기', command=toggle_synergy_info)
synergy_btn.grid(row=9, column=0, pady=10)

root.mainloop()
