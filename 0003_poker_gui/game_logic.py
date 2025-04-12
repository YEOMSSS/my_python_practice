import random
from collections import Counter

suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
rank_order = {r: i for i, r in enumerate(ranks)}

def create_deck():
    return [r + s for s in suits for r in ranks]

def deal_hand(deck, n=5):
    return [deck.pop() for _ in range(n)]

def sort_hand(hand):
    return sorted(hand, key=lambda c: rank_order[c[:-1]], reverse=True)

def evaluate_hand(hand):
    ranks_sorted = sorted([rank_order[c[:-1]] for c in hand], reverse=True)
    suits_ = [c[-1] for c in hand]
    rank_counts = Counter(c[:-1] for c in hand)
    count_vals = sorted(rank_counts.values(), reverse=True)
    most_common = rank_counts.most_common()

    unique_ranks = sorted(set(ranks_sorted))
    is_flush = len(set(suits_)) == 1
    is_straight = len(unique_ranks) == 5 and unique_ranks[-1] - unique_ranks[0] == 4

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

def compare_hands(player_eval, bot_eval):
    _, ps, pv = player_eval
    _, bs, bv = bot_eval
    if ps != bs:
        return "player" if ps < bs else "bot"
    for p, b in zip(pv, bv):
        if p != b:
            return "player" if p > b else "bot"
    return "tie"

def bot_replace(hand, deck):
    if not deck:
        return hand
    counts = Counter(card[:-1] for card in hand)
    most_common = counts.most_common(1)
    if most_common and most_common[0][1] >= 2:
        keep = most_common[0][0]
        new_hand = [c for c in hand if c[:-1] == keep]
        while len(new_hand) < 5 and deck:
            new_hand.append(deck.pop())
    else:
        new_hand = hand[:]
        for i in random.sample(range(5), min(3, len(deck))):
            new_hand[i] = deck.pop()
    return new_hand
