import tkinter as tk
import random

# 자모 리스트
CHOSUNG_LIST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
JUNGSUNG_LIST = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
JONGSUNG_LIST = ['', 'ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

# 쌍자음, 겹받침 조합 (순서 무관)
double_initials = {('ㄱ', 'ㄱ'): 'ㄲ', ('ㄷ', 'ㄷ'): 'ㄸ', ('ㅂ', 'ㅂ'): 'ㅃ', ('ㅅ', 'ㅅ'): 'ㅆ', ('ㅈ', 'ㅈ'): 'ㅉ'}
double_finals = {
    ('ㄱ', 'ㅅ'): 'ㄳ', ('ㄴ', 'ㅈ'): 'ㄵ', ('ㄴ', 'ㅎ'): 'ㄶ',
    ('ㄹ', 'ㄱ'): 'ㄺ', ('ㄹ', 'ㅁ'): 'ㄻ', ('ㄹ', 'ㅂ'): 'ㄼ',
    ('ㄹ', 'ㅅ'): 'ㄽ', ('ㄹ', 'ㅌ'): 'ㄾ', ('ㄹ', 'ㅍ'): 'ㄿ',
    ('ㄹ', 'ㅎ'): 'ㅀ', ('ㅂ', 'ㅅ'): 'ㅄ'
}

# 중성은 누적 가능한 모음 집합 조합으로 진화
compound_vowel_sets = {
    frozenset(['ㅗ', 'ㅏ']): 'ㅘ',
    frozenset(['ㅗ', 'ㅏ', 'ㅣ']): 'ㅙ',
    frozenset(['ㅜ', 'ㅓ']): 'ㅝ',
    frozenset(['ㅜ', 'ㅓ', 'ㅣ']): 'ㅞ',
    frozenset(['ㅗ', 'ㅣ']): 'ㅚ',
    frozenset(['ㅜ', 'ㅣ']): 'ㅟ',
    frozenset(['ㅡ', 'ㅣ']): 'ㅢ',
    frozenset(['ㅑ', 'ㅣ']): 'ㅒ',
    frozenset(['ㅕ', 'ㅣ']): 'ㅖ',
    frozenset(['ㅏ', 'ㅣ']): 'ㅐ',
    frozenset(['ㅓ', 'ㅣ']): 'ㅔ'
}

# 초기 상태
current = {
    '초성': random.choice(['ㄱ','ㄴ','ㅁ','ㅅ','ㅇ']),
    '중성': random.choice(['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ']),
    '종성': ''
}

# 누적 중성 조합 리스트
middle_stack = [current['중성']]  # 처음은 단일 중성으로 시작

active_part = '종성'
result_window = None
result_label = None

def combine_syllable():
    cho = CHOSUNG_LIST.index(current['초성'])
    jung = JUNGSUNG_LIST.index(current['중성'])
    jong = JONGSUNG_LIST.index(current['종성'])
    return chr(0xAC00 + (cho * 21 * 28) + (jung * 28) + jong)

def combine_if_possible(current_jamo, selected_jamo, combination_map):
    pair = (current_jamo, selected_jamo)
    reverse_pair = (selected_jamo, current_jamo)
    if pair in combination_map:
        return combination_map[pair]
    elif reverse_pair in combination_map:
        return combination_map[reverse_pair]
    return None

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
        elif val in CHOSUNG_LIST:
            current['초성'] = val
    elif active_part == '중성':
        if val in JUNGSUNG_LIST:
            if val not in middle_stack:
                middle_stack.append(val)
            result = compound_vowel_sets.get(frozenset(middle_stack))
            if result:
                current['중성'] = result
            elif val in JUNGSUNG_LIST:
                current['중성'] = val
                middle_stack = [val]
    elif active_part == '종성':
        combined = combine_if_possible(current['종성'], val, double_finals)
        if combined:
            current['종성'] = combined
        elif val in JONGSUNG_LIST:
            current['종성'] = val
    update_status()
    refresh_choices()
    update_result_window()

def update_status():
    result_char = combine_syllable()
    status_label.config(text=f"현재 글자: {result_char}")
    active_label.config(text=f"선택 중: {active_part}")

def refresh_choices():
    for widget in choice_frame.winfo_children():
        widget.destroy()
    base = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ','ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ']
    candidates = random.sample(base, 9)
    for i, j in enumerate(candidates):
        btn = tk.Button(choice_frame, text=j, width=6, height=2, font=('Arial', 16),
                        command=lambda val=j: select_jamo(val))
        btn.grid(row=i//3, column=i%3, padx=5, pady=5)

def create_result_window():
    global result_window, result_label
    result_window = tk.Toplevel(root)
    result_window.title("저장된 글자")
    result_window.geometry("250x200")
    result_label = tk.Label(result_window, text=combine_syllable(), font=('Arial', 48))
    result_label.pack(expand=True)

def update_result_window():
    if result_label:
        result_label.config(text=combine_syllable())

# UI 구성
root = tk.Tk()
root.title("한글 자모 진화 게임")
root.geometry("400x500")

tk.Label(root, text="초성/중성/종성을 선택 후 자모를 고르세요", font=("Arial", 12)).pack(pady=10)

active_label = tk.Label(root, text="선택 중: 종성", font=("Arial", 14))
active_label.pack()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="초성", font=("Arial", 12), command=lambda: set_active('초성')).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="중성", font=("Arial", 12), command=lambda: set_active('중성')).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="종성", font=("Arial", 12), command=lambda: set_active('종성')).pack(side=tk.LEFT, padx=10)

choice_frame = tk.Frame(root)
choice_frame.pack(pady=20)

status_label = tk.Label(root, text="", font=("Arial", 16))
status_label.pack()

# 초기 실행
create_result_window()
update_status()
refresh_choices()

root.mainloop()
