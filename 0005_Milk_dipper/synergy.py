
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "synergy_rules.json"), encoding="utf-8") as f:
    synergy_rules = json.load(f)

def match_condition(condition, jamo, index, jamo_stack, context):
    if condition == "is_first":
        return index == 0
    elif condition == "alone":
        return jamo_stack.count(jamo) == 1
    elif condition == "no_synergy":
        return not context.get("has_synergy", False)
    elif condition == "has_all_parts":
        return context.get("has_cho") and context.get("has_jung") and context.get("has_jong")
    elif condition.startswith("includes:"):
        target = condition.split(":")[1]
        return target in jamo_stack
    return False

def apply_synergy(jamo_stack, base_score):
    total_multiplier = 1.0
    total_bonus = 0
    descriptions = []

    has_cho = len(jamo_stack) > 0
    has_jung = len(jamo_stack) > 1
    has_jong = len(jamo_stack) > 2

    for i, jamo in enumerate(jamo_stack):
        for rule in synergy_rules:
            if rule["target"] != jamo:
                continue

            context = {
                "has_synergy": True,
                "has_cho": has_cho,
                "has_jung": has_jung,
                "has_jong": has_jong
            }

            matched = True
            for cond in rule.get("conditions", []):
                if not match_condition(cond, jamo, i, jamo_stack, context):
                    matched = False
                    break

            if matched:
                total_multiplier *= rule.get("multiplier", 1.0)
                total_bonus += rule.get("bonus", 0)
                descriptions.append(rule["desc"])

    final_score = int(base_score * total_multiplier + total_bonus)
    return final_score, descriptions, total_multiplier, total_bonus
