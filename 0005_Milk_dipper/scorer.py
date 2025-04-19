import json
import os
from synergy import apply_synergy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "jamo_point_table.json"), encoding="utf-8") as f:
    point_table = json.load(f)

def decompose_if_needed(jamo):
    decompose_map = {
        'ㅘ': ['ㅗ', 'ㅏ'], 'ㅙ': ['ㅗ', 'ㅐ'], 'ㅚ': ['ㅗ', 'ㅣ'],
        'ㅝ': ['ㅜ', 'ㅓ'], 'ㅞ': ['ㅜ', 'ㅔ'], 'ㅟ': ['ㅜ', 'ㅣ'], 'ㅢ': ['ㅡ', 'ㅣ'],
        'ㅐ': ['ㅏ', 'ㅣ'], 'ㅔ': ['ㅓ', 'ㅣ'], 'ㅒ': ['ㅑ', 'ㅣ'], 'ㅖ': ['ㅕ', 'ㅣ'],
        'ㄳ': ['ㄱ', 'ㅅ'], 'ㄵ': ['ㄴ', 'ㅈ'], 'ㄶ': ['ㄴ', 'ㅎ'],
        'ㄺ': ['ㄹ', 'ㄱ'], 'ㄻ': ['ㄹ', 'ㅁ'], 'ㄼ': ['ㄹ', 'ㅂ'],
        'ㄽ': ['ㄹ', 'ㅅ'], 'ㄾ': ['ㄹ', 'ㅌ'], 'ㄿ': ['ㄹ', 'ㅍ'], 'ㅀ': ['ㄹ', 'ㅎ'],
        'ㅄ': ['ㅂ', 'ㅅ'],
        'ㄲ': ['ㄱ', 'ㄱ'], 'ㄸ': ['ㄷ', 'ㄷ'], 'ㅃ': ['ㅂ', 'ㅂ'], 'ㅆ': ['ㅅ', 'ㅅ'], 'ㅉ': ['ㅈ', 'ㅈ']
    }
    return decompose_map.get(jamo, [jamo])

def calculate_score(jamo_stack):
    total = 0
    decomposed = []
    for j in jamo_stack:
        decomposed.extend(decompose_if_needed(j))
    for d in decomposed:
        total += point_table.get(d, 1)
    final_score, _, _, _ = apply_synergy(jamo_stack, total * len(decomposed))
    return final_score

def explain_score(jamo_stack):
    total = 0
    decomposed = []
    for j in jamo_stack:
        decomposed.extend(decompose_if_needed(j))
    for d in decomposed:
        total += point_table.get(d, 1)
    base_count = len(decomposed)
    score_before_synergy = total * base_count if base_count else 0
    final_score, synergy_descriptions, total_multiplier, total_bonus = apply_synergy(jamo_stack, score_before_synergy)

    formula = f"({total}) × {base_count}"
    if total_multiplier != 1.0:
        formula += f" × {total_multiplier:.2f}"
    if total_bonus:
        formula += f" + {total_bonus}"
    formula += f" = {final_score}"

    return final_score, synergy_descriptions, formula

if __name__ == '__main__':
    example = ['ㄱ', 'ㄱ', 'ㅏ', 'ㅣ']
    score, details, formula = explain_score(example)
    print(f"{example} => {score}점")
    for line in details:
        print(" -", line)
    print("수식:", formula)
