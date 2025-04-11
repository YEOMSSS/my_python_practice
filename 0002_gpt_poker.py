import random
from collections import Counter  # 추가

suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

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
    for i in [x - 1 for x in replace_numbers]:
        if deck:
            hand[i] = deck.pop()
        else:
            print("덱에 더 이상 카드가 없습니다!")
            break

    print("\n[바꾼 후] Player의 카드:")
    print_hand(hand, "Player")
    return hand
#봇이 페어 여부에 따라 3장을 교체체
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
    rank_order = {r: i for i, r in enumerate(ranks)}  # ranks는 이미 전역에 있어
    rank_counts = Counter(card[:-1] for card in hand)
    suit_counts = Counter(card[-1] for card in hand)

    ranks_sorted = sorted([rank_order[card[:-1]] for card in hand], reverse=True)
    unique_ranks = sorted(set(ranks_sorted))

    is_flush = len(suit_counts) == 1
    is_straight = (
        len(unique_ranks) == 5 and
        unique_ranks[-1] - unique_ranks[0] == 4
    )

    # A-2-3-4-5 스트레이트 예외 처리
    if set(ranks_sorted) == {12, 0, 1, 2, 3}:
        is_straight = True
        ranks_sorted = [3, 2, 1, 0, -1]

    count_values = sorted(rank_counts.values(), reverse=True)
    most_common = rank_counts.most_common()

    # 족보 판별
    if is_straight and is_flush and max(ranks_sorted) == 12:
        return "Royal Flush", 1
    elif is_straight and is_flush:
        return "Straight Flush", 2
    elif count_values == [4, 1]:
        return "Four of a Kind", 3
    elif count_values == [3, 2]:
        return "Full House", 4
    elif is_flush:
        return "Flush", 5
    elif is_straight:
        return "Straight", 6
    elif count_values == [3, 1, 1]:
        return "Three of a Kind", 7
    elif count_values == [2, 2, 1]:
        return "Two Pair", 8
    elif count_values == [2, 1, 1, 1]:
        return "One Pair", 9
    else:
        return "High Card", 10

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
    player_hand = player_replace_cards(player_hand, deck)
    player_hand = sort_hand(player_hand)

    # 봇 카드 교체
    bot_hand = bot_replace_cards(bot_hand, deck)
    bot_hand = sort_hand(bot_hand)
    print("\n[최종 핸드]")
    print_hand(player_hand, "Player")
    print_hand(bot_hand, "Bot")

    player_rank, player_score = evaluate_hand(player_hand)
    bot_rank, bot_score = evaluate_hand(bot_hand)

    print(f"\nPlayer 족보: {player_rank}")
    print(f"Bot 족보: {bot_rank}")

    if player_score < bot_score:
        print("\n🎉 Player 승리!")
    elif player_score > bot_score:
        print("\n🤖 Bot 승리!")
    else:
        print("\n무승부!")

if __name__ == "__main__":
    main()


    
