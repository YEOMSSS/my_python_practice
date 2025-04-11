#동일 족보여도 높은 숫자로 평가
#플레이어는 손패를 2번 바꿀 수 있다



import random
from collections import Counter  # 추가

suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
rank_order = {r: i for i, r in enumerate(ranks)}  # 2=0, A=12

#52장짜리 덱 리스트 만들기
def create_deck():
    return [rank + suit for suit in suits for rank in ranks]
#두 플레이어카 카드를 5장씩 받는다
def deal_cards(deck, num_players=2, cards_each=5):
    hands = [[] for _ in range(num_players)]
    for _ in range(cards_each):
        for player in hands:
            player.append(deck.pop())
    return hands
#플레이어의 핸드를 보기 좋게 프린트한다
def print_hand(hand, owner="Player", show_index=False):
    if show_index:
        for i, card in enumerate(hand, 1):
            print(f"{i}) {card}", end='   ')
        print()
    else:
        print(f"{owner}'s Hand: ", ' | '.join(hand))
#플레이어가 교체할 핸드를 선택해 교체
def player_replace_cards(hand, deck):
    print("\n바꾸고 싶은 카드의 번호를 띄어쓰기로 입력하세요 (예: 2 4 5)")
    print("중복 없이, 최대 5장까지 선택 가능합니다.")
    print("바꾸고 싶지 않으면 그냥 Enter만 누르세요.")
    print_hand(hand, "Player", show_index=True)

    replace_input = input(">> ").strip()

    if replace_input == "":
        print("카드를 바꾸지 않았습니다.")
        return hand

    tokens = replace_input.split()

    # 1. 숫자만 입력했는지 확인
    if not all(x.isdigit() for x in tokens):
        print("입력이 잘못되었습니다. 숫자만 입력해주세요. 예: 1 3 5")
        return hand

    # 2. 정수로 변환
    replace_numbers = [int(x) for x in tokens]

    # 3. 중복 검사
    if len(set(replace_numbers)) != len(replace_numbers):
        print("중복된 숫자가 있습니다. 같은 카드는 한 번만 선택하세요.")
        return hand

    # 4. 범위 검사 (1~5)
    if not all(1 <= x <= len(hand) for x in replace_numbers):
        print("1~5 사이의 숫자만 입력 가능합니다.")
        return hand

    # 5. 최대 개수 제한
    if len(replace_numbers) > 5:
        print("최대 5장까지만 바꿀 수 있습니다.")
        return hand

    # 6. 카드 바꾸기
    if len(replace_numbers) > len(deck):
        print(f"덱에 남은 카드가 {len(deck)}장뿐입니다. 가능한 만큼만 바꿉니다.")

    # 가능한 수만큼 교체
    for i in [x - 1 for x in replace_numbers][:len(deck)]:
        hand[i] = deck.pop()

    print("\n[바꾼 후] Player의 카드:")
    print_hand(hand, "Player")
    return hand
#봇이 페어 여부에 따라 3장을 교체
def bot_replace_cards(hand, deck):
    # 숫자만 뽑아냄 (무늬 제거)
    ranks_only = [card[:-1] for card in hand]
    rank_counts = Counter(ranks_only)  # 몇 개씩 있는지 세기

    # 가장 많은 랭크 찾기
    most_common = rank_counts.most_common(1)
    if most_common and most_common[0][1] >= 2:
        keep_rank = most_common[0][0]  # 예: '5'
        new_hand = []
        for card in hand:
            if card[:-1] == keep_rank:
                new_hand.append(card)  # 유지
        while len(new_hand) < 5:
            new_hand.append(deck.pop())  # 새 카드 채우기
        print("\n[봇] 한 쌍 이상의 패를 유지하고 나머지 교체함.")
    else:
        # 쌍이 없으면 무작위 2~3장 바꾸기
        indices_to_replace = random.sample(range(5), 3)
        new_hand = hand[:]
        for i in indices_to_replace:
            new_hand[i] = deck.pop()
        print("\n[봇] 쌍이 없어 무작위로 3장 교체함.")

    return new_hand
#핸드를 숫자 내림차순으로 정렬
def sort_hand(hand):
    rank_order = {r: i for i, r in enumerate(ranks)}  # ranks는 전역에 있음
    return sorted(hand, key=lambda card: rank_order[card[:-1]])
#핸드 족보 평가
def evaluate_hand(hand):
    rank_counts = Counter(card[:-1] for card in hand)
    suit_counts = Counter(card[-1] for card in hand)

    ranks_sorted = sorted([rank_order[card[:-1]] for card in hand], reverse=True)
    unique_ranks = sorted(set(ranks_sorted))

    is_flush = len(suit_counts) == 1
    is_straight = (
        len(unique_ranks) == 5 and
        unique_ranks[-1] - unique_ranks[0] == 4
    )

    if set(ranks_sorted) == {12, 0, 1, 2, 3}:
        is_straight = True
        ranks_sorted = [3, 2, 1, 0, -1]

    count_values = sorted(rank_counts.values(), reverse=True)
    most_common = rank_counts.most_common()

    if is_straight and is_flush and max(ranks_sorted) == 12:
        return "Royal Flush", 1, ranks_sorted
    elif is_straight and is_flush:
        return "Straight Flush", 2, ranks_sorted
    elif count_values == [4, 1]:
        quad = [rank_order[r] for r, c in most_common if c == 4][0]
        kicker = [rank_order[r] for r, c in most_common if c == 1][0]
        return "Four of a Kind", 3, [quad, kicker]
    elif count_values == [3, 2]:
        triple = [rank_order[r] for r, c in most_common if c == 3][0]
        pair = [rank_order[r] for r, c in most_common if c == 2][0]
        return "Full House", 4, [triple, pair]
    elif is_flush:
        return "Flush", 5, sorted(ranks_sorted, reverse=True)
    elif is_straight:
        return "Straight", 6, ranks_sorted
    elif count_values == [3, 1, 1]:
        triple = [rank_order[r] for r, c in most_common if c == 3][0]
        kickers = sorted([rank_order[r] for r, c in most_common if c == 1], reverse=True)
        return "Three of a Kind", 7, [triple] + kickers
    elif count_values == [2, 2, 1]:
        pairs = sorted([rank_order[r] for r, c in most_common if c == 2], reverse=True)
        kicker = [rank_order[r] for r, c in most_common if c == 1][0]
        return "Two Pair", 8, pairs + [kicker]
    elif count_values == [2, 1, 1, 1]:
        pair = [rank_order[r] for r, c in most_common if c == 2][0]
        kickers = sorted([rank_order[r] for r, c in most_common if c == 1], reverse=True)
        return "One Pair", 9, [pair] + kickers
    else:
        return "High Card", 10, sorted(ranks_sorted, reverse=True)
#족보 동일 시 높은 숫자로 평가
def compare_hands(player_eval, bot_eval):
    _, player_score, player_values = player_eval
    _, bot_score, bot_values = bot_eval

    if player_score < bot_score:
        return "player"
    elif player_score > bot_score:
        return "bot"
    else:
        for p, b in zip(player_values, bot_values):
            if p > b:
                return "player"
            elif p < b:
                return "bot"
        return "tie"
    

def main():
    print("=== 파이브 카드 드로우 포커 ===\n")
    
    deck = create_deck()
    random.shuffle(deck)

    hands = deal_cards(deck)
    player_hand, bot_hand = hands
    player_hand = sort_hand(player_hand)
    bot_hand = sort_hand(bot_hand)

    print("\n[처음 받은 카드]")
    print_hand(player_hand, "Player")
    print_hand(bot_hand, "Bot")

    # 플레이어 카드 교체
    MAX_REPLACE_TURNS = 2
    for i in range(MAX_REPLACE_TURNS):
        if not deck:
            print("\n⚠️ 덱이 모두 소진되어 더 이상 교체할 수 없습니다.")
            break

        print(f"\n[카드 교체 {i+1}/{MAX_REPLACE_TURNS}]")
        prev_hand = player_hand[:]
        player_hand = player_replace_cards(player_hand, deck)
        player_hand = sort_hand(player_hand)

        if player_hand == prev_hand:
            print("교체 없이 턴 종료됨.")
            break

    # 봇 카드 교체
    bot_hand = bot_replace_cards(bot_hand, deck)
    bot_hand = sort_hand(bot_hand)
    print("\n[최종 핸드]")
    print_hand(player_hand, "Player")
    print_hand(bot_hand, "Bot")

    player_eval = evaluate_hand(player_hand)
    bot_eval = evaluate_hand(bot_hand)

    player_rank, player_score, player_values = player_eval
    bot_rank, bot_score, bot_values = bot_eval

    # 가장 중요한 비교 기준을 괄호 안에 출력 (족보 타이브레이커에서 첫 번째 요소)
    player_main_value = player_values[0] if player_values else -1
    bot_main_value = bot_values[0] if bot_values else -1

    # 역변환: 숫자를 다시 랭크 문자열로
    inv_rank_order = {v: k for k, v in rank_order.items()}
    player_rank_text = f"{player_rank} ({inv_rank_order.get(player_main_value, '?')})"
    bot_rank_text = f"{bot_rank} ({inv_rank_order.get(bot_main_value, '?')})"

    result = compare_hands(player_eval, bot_eval)

    if result == "player":
        winner_text = "🎉 Player 승리!"
    elif result == "bot":
        winner_text = "🤖 Bot 승리!"
    else:
        winner_text = "무승부!"
    
    print(f"\nPlayer 족보: {player_rank_text}")
    print(f"Bot 족보: {bot_rank_text}\n")
    print(winner_text)

if __name__ == "__main__":
    main()


    
