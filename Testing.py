from BlackJack import *


cards = ["ACE DIAMOND", "TWO CLUB", "KING HEART", "QUEEN DIAMOND", "THREE SPADE", "FOUR SPADE", "SIX DIAMOND", "FIVE HEART", "SEVEN CLUB", "EIGHT HEART", "NINE SPADE", "TEN DIAMOND", "JACK CLUB"]


def count_score_test():
    score = Croupier().count_score(cards)
    assert score == 85
    return True


def checking_if_ace_test():
    ace_test = Croupier().check_if_ace_in_hand(cards)
    assert ace_test
    return True


def draw_busters_test():
    game = Game(init_or_dont=0)
    game.player.score = 22
    game.croupier.score = 23
    condition = game.check_the_buster()
    assert condition[0] == 0
    return True


def player_buster_test():
    game = Game(init_or_dont=0)
    game.player.score = 22
    game.croupier.score = 20
    condition = game.check_the_buster()
    assert condition[0] == -1
    return True


def croupier_buster_test():
    game = Game(init_or_dont=0)
    game.player.score = 20
    game.croupier.score = 22
    game.bet_value = 0
    condition = game.check_the_buster()
    assert condition[0] == 1
    return True


def draw_test():
    game = Game(init_or_dont=0)
    game.player.score = 20
    game.croupier.score = 20
    condition = game.check_the_winner()
    assert condition == 0
    return True


def croupier_win_test():
    game = Game(init_or_dont=0)
    game.player.score = 20
    game.croupier.score = 21
    condition = game.check_the_winner()
    assert condition == -1
    return True


def player_win_test():
    game = Game(init_or_dont=0)
    game.player.score = 21
    game.croupier.score = 20
    game.bet_value = 0
    condition = game.check_the_winner()
    assert condition == 1
    return True


def player_score_if_ace_eleven_test():
    player = Player()
    player.hand = ["ACE DIAMOND", "KING HEART"]
    player.get_player_score()
    assert player.score == 21
    return True


print(count_score_test())
print(checking_if_ace_test())
print(draw_busters_test())
print(player_buster_test())
print(croupier_buster_test())
print(draw_test())
print(croupier_win_test())
print(player_win_test())
print(player_score_if_ace_eleven_test())