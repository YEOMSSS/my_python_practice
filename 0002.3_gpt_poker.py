#동일 족보여도 높은 숫자로 평가
#플레이어는 손패를 카드가 사라질 때까지 바꿀 수 있다
#코드 압축
#덱에 카드가 없으면 봇은 바꾸지 않는다다

import random
from collections import Counter

suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
rank_order = {r: i for i, r in enumerate(ranks)}

# 52장의 포커 덱을 생성. 각 카드는 '랭크+무늬' 형식 (예: 'A♠')
def create_deck():
    return [r + s for s in suits for r in ranks]


# 주어진 덱에서 플레이어 수만큼 5장의 카드를 나누어 반환
# 반환 형식: [ [player1의 카드], [player2의 카드] ]
def deal_cards(deck, players=2, cards_each=5):
    return [[deck.pop() for _ in range(cards_each)] for _ in range(players)]


# 핸드를 보기 좋게 출력
# show_index=True이면 번호가 붙어 출력됨 (카드 선택 시 사용)
def print_hand(hand, owner="Player", show_index=False):
    if show_index:
        for i, card in enumerate(hand, 1):
            print(f"{i}) {card}", end='   ')
        print()
    else:
        print(f"{owner}'s Hand: ", ' | '.join(hand))

# 사용자 입력 문자열을 검증하여 유효한 카드 번호 리스트 반환
# 조건: 공백으로 구분된 숫자이며, 중복 없이 1~hand_size 범위, 최대 5개
# 반환값: 유효하면 숫자 리스트, 아니면 None
def validate_replace_input(user_input, hand_size):
    if user_input == "":
        return []
    tokens = user_input.split()
    if not all(x.isdigit() for x in tokens): return None
    nums = [int(x) for x in tokens]
    if len(set(nums)) != len(nums): return None
    if not all(1 <= x <= hand_size for x in nums): return None
    if len(nums) > 5: return None
    return nums


# 플레이어가 교체할 카드 번호를 입력 받아 덱에서 교체 진행
# 입력이 유효하지 않으면 다시 입력 요청
# 유효한 경우 카드 교체 후 갱신된 핸드 반환
def player_replace_cards(hand, deck):
    while True:
        print("\n바꾸고 싶은 카드 번호 (예: 2 4 5), Enter만 치면 패스")
        print_hand(hand, "Player", show_index=True)
        print(f"[남은 카드 수: {len(deck)}장]")

        user_input = input(">> ").strip()
        nums = validate_replace_input(user_input, len(hand))

        if nums is None:
            print("입력이 잘못되었습니다. 다시 시도하세요.")
            continue

        if not nums:
            print("카드를 바꾸지 않았습니다.")
            return hand

        if len(nums) > len(deck):
            print(f"덱에 남은 카드가 {len(deck)}장뿐입니다. 가능한 만큼만 바꿉니다.")

        for i in [x - 1 for x in nums][:len(deck)]:
            hand[i] = deck.pop()

        print("\n[바꾼 후] Player의 카드:")
        print_hand(hand, "Player")
        return hand


# 봇의 카드 교체 로직
# 덱이 비었을 경우 교체하지 않고 그대로 유지
# 페어 이상이면 해당 랭크만 유지하고 나머지 교체
# 없으면 무작위 3장 교체 (덱이 충분한 경우)
def bot_replace_cards(hand, deck):
    if not deck:
        print("\n[봇] 덱이 소진되어 교체하지 않음.")
        return hand

    counts = Counter(card[:-1] for card in hand)
    most_common = counts.most_common(1)

    if most_common and most_common[0][1] >= 2:
        keep = most_common[0][0]
        new_hand = [c for c in hand if c[:-1] == keep]
        while len(new_hand) < 5 and deck:
            new_hand.append(deck.pop())
        print("\n[봇] 페어 이상 유지, 나머지 교체")
    else:
        new_hand = hand[:]
        for i in random.sample(range(5), min(3, len(deck))):
            new_hand[i] = deck.pop()
        print("\n[봇] 무작위 3장 교체")
    return new_hand


# 카드 랭크 기준 내림차순 정렬 (A > K > ... > 2)
def sort_hand(hand):
    return sorted(hand, key=lambda c: rank_order[c[:-1]], reverse=True)


# 주어진 핸드의 족보를 평가
# 반환: (족보 이름, 점수, 비교용 랭크 리스트)
# 족보는 점수가 낮을수록 강함 (1=로열플러시)
def evaluate_hand(hand):
    ranks_sorted = sorted([rank_order[c[:-1]] for c in hand], reverse=True)
    suits = [c[-1] for c in hand]
    rank_counts = Counter(c[:-1] for c in hand)
    count_vals = sorted(rank_counts.values(), reverse=True)
    most_common = rank_counts.most_common()

    unique_ranks = sorted(set(ranks_sorted))
    is_flush = len(set(suits)) == 1
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


# 족보 점수 우선 비교, 동점이면 랭크 리스트로 비교
# 승자: 'player', 'bot', 또는 'tie' 반환
def compare_hands(player_eval, bot_eval):
    _, ps, pv = player_eval
    _, bs, bv = bot_eval
    if ps != bs:
        return "player" if ps < bs else "bot"
    for p, b in zip(pv, bv):
        if p != b:
            return "player" if p > b else "bot"
    return "tie"


# 게임의 메인 흐름을 담당하는 함수
# 덱 생성 → 카드 배분 → 플레이어/봇 교체 → 족보 평가 및 승자 출력
def main():
    print("=== ㅅㅇㄷㅏ 카드 드로우 포커 ===\n")
    deck = create_deck()
    random.shuffle(deck)
    player_hand, bot_hand = map(sort_hand, deal_cards(deck))

    print("\n[처음 받은 카드]")
    print_hand(player_hand, "Player")
    print_hand(bot_hand, "Bot")

    while deck:
        print("\n[카드 교체]")
        prev = player_hand[:]
        player_hand = sort_hand(player_replace_cards(player_hand, deck))
        if player_hand == prev:
            print("교체 없이 턴 종료됨.")
            break
        if not deck:
            print("⚠️ 덱이 소진되어 더 이상 교체할 수 없습니다.")
            break

    bot_hand = sort_hand(bot_replace_cards(bot_hand, deck))
    print("\n[최종 핸드]")
    print_hand(player_hand, "Player")
    print_hand(bot_hand, "Bot")

    pe, be = evaluate_hand(player_hand), evaluate_hand(bot_hand)
    pr, ps, pv = pe
    br, bs, bv = be

    inv_rank = {v: k for k, v in rank_order.items()}
    print(f"\nPlayer 족보: {pr} ({inv_rank.get(pv[0], '?')})")
    print(f"Bot 족보: {br} ({inv_rank.get(bv[0], '?')})\n")

    result = compare_hands(pe, be)
    print("🎉 Player 승리!" if result == "player" else "🤖 Bot 승리!" if result == "bot" else "무승부!")


if __name__ == "__main__":
    main()
