
# scorer.py

from synergy import apply_synergy

# 복합 자모 분해 함수 (점수 계산에 사용함)
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

# 자모별 점수 정의
point_table = {
    # 기본 자음 (1점)
    'ㄱ': 1, 'ㄴ': 1, 'ㅁ': 1, 'ㅅ': 1, 'ㅇ': 1,
    # 가획 1회 자음 (2점)
    'ㄷ': 2, 'ㅂ': 2, 'ㅈ': 2, 'ㅋ': 2,
    # 가획 2회 자음 (3점)
    'ㅊ': 3, 'ㅌ': 3, 'ㅍ': 3, 'ㅎ': 3,
    # ㄹ (독립 점수)
    'ㄹ': 4,
    # 모음 (3점)
    'ㅏ': 3, 'ㅑ': 3, 'ㅓ': 3, 'ㅕ': 3, 'ㅗ': 3, 'ㅛ': 3,
    'ㅜ': 3, 'ㅠ': 3, 'ㅡ': 3, 'ㅣ': 3
}

def calculate_score(jamo_stack):
    total = 0
    decomposed = []
    for j in jamo_stack:
        decomposed.extend(decompose_if_needed(j))
    for d in decomposed:
        total += point_table.get(d, 1)
    final_score, _ = apply_synergy(decomposed, total * len(decomposed))
    return final_score

def explain_score(jamo_stack):
    explanation = []
    total = 0
    decomposed = []
    for j in jamo_stack:
        decomposed.extend(decompose_if_needed(j))
    for d in decomposed:
        pt = point_table.get(d, 1)
        total += pt
        explanation.append(f"{d}: +{pt}")
    base_count = len(decomposed)
    score_before_synergy = total * base_count if base_count else 0
    final_score, synergy_descriptions = apply_synergy(decomposed, score_before_synergy)
    if base_count:
        explanation.append(f"자모 {base_count}개 사용 보너스: x{base_count}")
        explanation.extend(synergy_descriptions)
        formula = f"({total}) × {base_count}" + (" × " + " × ".join([d.split('×')[1] for d in synergy_descriptions]) if synergy_descriptions else "") + f" = {final_score}"
    else:
        final_score = 0
        formula = "0점"
    return final_score, explanation, formula

# 디버그 테스트
if __name__ == '__main__':
    example = ['ㄱ', 'ㄴ', 'ㅁ', 'ㅗ', 'ㅣ', 'ㄹ', 'ㄱ']
    score, details, formula = explain_score(example)
    print(f"{example} => {score}점")
    for line in details:
        print(" -", line)
    print("수식:", formula)
