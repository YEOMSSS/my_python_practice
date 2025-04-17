# scorer.py

# 자모 능력 정의
effects = {
    'ㄱ': {'type': 'add', 'value': 2}, 'ㄲ': {'type': 'add', 'value': 4},
    'ㄴ': {'type': 'add', 'value': 1},
    'ㄷ': {'type': 'add', 'value': 2}, 'ㄸ': {'type': 'add', 'value': 4},
    'ㄹ': {'type': 'add', 'value': 3},
    'ㅁ': {'type': 'add', 'value': 5},
    'ㅂ': {'type': 'add', 'value': 2}, 'ㅃ': {'type': 'add', 'value': 4},
    'ㅅ': {'type': 'add', 'value': 2}, 'ㅆ': {'type': 'add', 'value': 4},
    'ㅇ': {'type': 'add', 'value': 1},
    'ㅈ': {'type': 'add', 'value': 3}, 'ㅉ': {'type': 'add', 'value': 5},
    'ㅊ': {'type': 'add', 'value': 4},
    'ㅋ': {'type': 'add', 'value': 5},
    'ㅌ': {'type': 'add', 'value': 5},
    'ㅍ': {'type': 'add', 'value': 4},
    'ㅎ': {'type': 'add', 'value': 3},
    'ㅏ': {'type': 'add', 'value': 3},
    'ㅓ': {'type': 'add', 'value': 3},
    'ㅗ': {'type': 'mul', 'value': 2},
    'ㅜ': {'type': 'mul', 'value': 2},
    'ㅡ': {'type': 'add', 'value': 1},
    'ㅣ': {'type': 'add', 'value': 2},
    'ㅐ': {'type': 'add', 'value': 3}, 'ㅔ': {'type': 'add', 'value': 3},
    'ㅒ': {'type': 'add', 'value': 4}, 'ㅖ': {'type': 'add', 'value': 4},
    '':   {'type': 'add', 'value': 0}  # 받침 없을 때
}

# 복합 자모 분해
def decompose_if_needed(jamo):
    decompose_map = {
        'ㅘ': ['ㅗ', 'ㅏ'], 'ㅙ': ['ㅗ', 'ㅐ'], 'ㅚ': ['ㅗ', 'ㅣ'],
        'ㅝ': ['ㅜ', 'ㅓ'], 'ㅞ': ['ㅜ', 'ㅔ'], 'ㅟ': ['ㅜ', 'ㅣ'], 'ㅢ': ['ㅡ', 'ㅣ'],
        'ㄳ': ['ㄱ', 'ㅅ'], 'ㄵ': ['ㄴ', 'ㅈ'], 'ㄶ': ['ㄴ', 'ㅎ'],
        'ㄺ': ['ㄹ', 'ㄱ'], 'ㄻ': ['ㄹ', 'ㅁ'], 'ㄼ': ['ㄹ', 'ㅂ'],
        'ㄽ': ['ㄹ', 'ㅅ'], 'ㄾ': ['ㄹ', 'ㅌ'], 'ㄿ': ['ㄹ', 'ㅍ'], 'ㅀ': ['ㄹ', 'ㅎ'],
        'ㅄ': ['ㅂ', 'ㅅ']
    }
    return decompose_map.get(jamo, [jamo])


def calculate_score(cho, jung, jong):
    base_score = 0
    additive = 0
    multiplier = 1

    for jamo in [cho, jung, jong]:
        for sub in decompose_if_needed(jamo):
            effect = effects.get(sub)
            if effect:
                if effect['type'] == 'add':
                    additive += effect['value']
                elif effect['type'] == 'mul':
                    multiplier *= effect['value']

    final_score = (base_score + additive) * multiplier
    return final_score


def explain_score(cho, jung, jong):
    explanation = []
    base_score = 0
    additive = 0
    multiplier = 1

    for jamo in [cho, jung, jong]:
        for sub in decompose_if_needed(jamo):
            effect = effects.get(sub)
            if effect:
                if effect['type'] == 'add':
                    additive += effect['value']
                    explanation.append(f"{sub}: +{effect['value']}")
                elif effect['type'] == 'mul':
                    multiplier *= effect['value']
                    explanation.append(f"{sub}: x{effect['value']}")

    formula = f"({base_score} + {additive}) × {multiplier} = {(base_score + additive) * multiplier}"
    final_score = (base_score + additive) * multiplier
    return final_score, explanation, formula


# 디버그용 테스트 코드
if __name__ == '__main__':
    example = ('ㄲ', 'ㅘ', 'ㅄ')  # 복합초성 + 복합모음 + 겹받침
    score, details, formula = explain_score(*example)
    print(f"{example} => {score}점")
    for line in details:
        print(" -", line)
    print("수식:", formula)
