
# synergy.py

def apply_synergy(jamo_stack, base_score):
    bonus_multiplier = 1
    description = []

    # 시너지 1: 기본자 3개 이상
    base_roots = {'ㄱ', 'ㄴ', 'ㅁ', 'ㅅ', 'ㅇ'}
    base_root_count = sum(1 for j in jamo_stack if j in base_roots)
    if base_root_count >= 3:
        bonus_multiplier *= 2
        description.append("기본자 3개 이상 시너지 ×2")

    # 향후 시너지 추가 예정
    # 예시:
    # if {'ㄹ', 'ㅣ'} <= set(jamo_stack):
    #     bonus_multiplier *= 1.5
    #     description.append("ㄹ + ㅣ 시너지 ×1.5")

    return base_score * bonus_multiplier, description
