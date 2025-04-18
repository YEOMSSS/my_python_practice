import random
from collections import Counter

# ♠ 카드 무늬와 숫자 정의
suits = ['♠', '♦', '♥', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
rank_order = {r: i for i, r in enumerate(ranks)}

# 🃏 52장의 전체 덱을 생성합니다.
def create_deck():
    return [r + s for s in suits for r in ranks]

# 📤 덱에서 n장의 카드를 꺼내 손패를 만듭니다.
def deal_hand(deck, n=5):
    return [deck.pop() for _ in range(n)]

# 🔢 손패를 rank 기준으로 내림차순 정렬합니다.
def sort_hand(hand):
    return sorted(hand, key=lambda c: rank_order[c[:-1]], reverse=True)

# 🧠 주어진 손패의 족보를 분석하고 점수를 매깁니다.
# 반환: (족보 이름, 우선순위 숫자, 비교용 랭크 리스트)
def evaluate_hand(hand):
    ranks_sorted = sorted([rank_order[c[:-1]] for c in hand], reverse=True)
    suits_ = [c[-1] for c in hand]
    rank_counts = Counter(c[:-1] for c in hand)
    count_vals = sorted(rank_counts.values(), reverse=True)
    most_common = rank_counts.most_common()

    unique_ranks = sorted(set(ranks_sorted))
    is_flush = len(set(suits_)) == 1
    is_straight = len(unique_ranks) == 5 and unique_ranks[-1] - unique_ranks[0] == 4

    # A-2-3-4-5 스트레이트 처리
    if set(ranks_sorted) == {12, 0, 1, 2, 3}:
        is_straight = True
        ranks_sorted = [3, 2, 1, 0, -1]

    if is_straight and is_flush and max(ranks_sorted) == 12:
        return "Royal Flush", 1, ranks_sorted
    elif is_straight and is_flush:
        return "Straight Flush", 2, ranks_sorted
    elif count_vals == [4, 1]:
        q = [rank_order[r] for r, c in most_common if c == 4][0]
        k = [rank_order[r] for r, c in most_common if c == 1][0]
        return "Four of a Kind", 3, [q, k]
    elif count_vals == [3, 2]:
        t = [rank_order[r] for r, c in most_common if c == 3][0]
        p = [rank_order[r] for r, c in most_common if c == 2][0]
        return "Full House", 4, [t, p]
    elif is_flush:
        return "Flush", 5, ranks_sorted
    elif is_straight:
        return "Straight", 6, ranks_sorted
    elif count_vals == [3, 1, 1]:
        t = [rank_order[r] for r, c in most_common if c == 3][0]
        ks = sorted([rank_order[r] for r, c in most_common if c == 1], reverse=True)
        return "Three of a Kind", 7, [t] + ks
    elif count_vals == [2, 2, 1]:
        ps = sorted([rank_order[r] for r, c in most_common if c == 2], reverse=True)
        k = [rank_order[r] for r, c in most_common if c == 1][0]
        return "Two Pair", 8, ps + [k]
    elif count_vals == [2, 1, 1, 1]:
        p = [rank_order[r] for r, c in most_common if c == 2][0]
        ks = sorted([rank_order[r] for r, c in most_common if c == 1], reverse=True)
        return "One Pair", 9, [p] + ks
    else:
        return "High Card", 10, ranks_sorted

# ⚔️ 플레이어와 봇의 족보 결과를 비교합니다.
# 반환: "player", "bot", "tie"
def compare_hands(player_eval, bot_eval):
    _, ps, pv = player_eval
    _, bs, bv = bot_eval
    if ps != bs:
        return "player" if ps < bs else "bot"
    for p, b in zip(pv, bv):
        if p != b:
            return "player" if p > b else "bot"
    return "tie"

# 🤖 봇이 자신의 핸드를 평가하고, 전략적으로 일부 카드만 교체합니다.
def bot_replace(hand, deck):
    if not deck:
        return hand[:]

    hand_eval = evaluate_hand(hand)
    hand_name, score, _ = hand_eval
    ranks_in_hand = [card[:-1] for card in hand]
    counter = Counter(ranks_in_hand)

    keep_indices = set()

    # 좋은 족보는 유지
    if score <= 6:
        return hand[:]

    elif hand_name == "Three of a Kind":
        three_rank = [r for r, c in counter.items() if c == 3][0]
        keep_indices = {i for i, c in enumerate(hand) if c[:-1] == three_rank}

    elif hand_name == "Two Pair":
        pair_ranks = [r for r, c in counter.items() if c == 2]
        keep_indices = {i for i, c in enumerate(hand) if c[:-1] in pair_ranks}

    elif hand_name == "One Pair":
        pair_rank = [r for r, c in counter.items() if c == 2][0]
        keep_indices = {i for i, c in enumerate(hand) if c[:-1] == pair_rank}

    elif hand_name == "High Card":
        max_rank = max(hand, key=lambda c: rank_order[c[:-1]])
        keep_indices = {i for i, c in enumerate(hand) if c == max_rank}

    new_hand = []
    for i in range(5):
        if i in keep_indices:
            new_hand.append(hand[i])
        elif deck:
            new_hand.append(deck.pop())
        else:
            new_hand.append(hand[i])

    return sort_hand(new_hand)
