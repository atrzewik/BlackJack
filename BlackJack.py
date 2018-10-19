from random import shuffle

from aenum import Enum, NoAlias

from UserInputProvider import *

import re


class Color(Enum):
    HEART = 1
    DIAMOND = 2
    SPADE = 3
    CLUB = 4

    @classmethod
    def values(cls):
        return list(cls)


class Sign(Enum):
    _settings_ = NoAlias
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10
    QUEEN = 10
    KING = 10

    @classmethod
    def values(cls):
        return list(cls)


class Card(object):

    def __init__(self, sign, color):
        self.sign = sign
        self.color = color

    def __repr__(self):
        return self.sign.name + " " + self.color.name


class Deck(object):

    def __init__(self):
        self.cards = []
        for color in Color.values():
            for sign in Sign.values():
                self.cards.append(Card(sign, color))
        self.shuffle_deck()

    def shuffle_deck(self):
        return shuffle(self.cards)

    def get_card(self):
        card = self.cards[0]
        self.__delete_card_from_deck(card)
        return card

    def __delete_card_from_deck(self, card):
        self.cards.remove(card)


class Contestant(object):

    def __init__(self):
        self.hand = []

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def count_score(self):
        score = 0
        for card in self.hand:
            score += card.sign.value
        if self.__ace_in_hand() and score <= 11:
            score += 10
        return score

    def __ace_in_hand(self):
        list_of_signs = [card.sign for card in self.hand]
        return Sign.ACE in list_of_signs


class Croupier(Contestant):

    def __init__(self):
        super().__init__()
        self.name = "Croupier"
        self.casino = 0
        self.cash = 0

    def should_draw_cards(self):
        return self.count_score() <= 16

    def get_single_card(self):
        return self.hand[0]

    def get_money_from_player(self, player):
        player.pay_bet_value()
        self.casino += player.bet_value
        player.double_bet_value()


class MoveType(Enum):
    _settings_ = NoAlias
    NONE = 'n'
    STAND = 'st'
    HIT = 'h'
    DOUBLE = 'd'
    SPLIT = 'sp'

    @classmethod
    def match_move(cls, player_move):
        for last_move in cls.values():
            if last_move.value == player_move:
                return last_move

    @classmethod
    def values(cls):
        return list(cls)

    @classmethod
    def remove_value_from_values(cls, values, value):
        values.remove(value)
        return values

    @classmethod
    def values_without_none(cls):
        return cls.remove_value_from_values(cls.values(), cls.NONE)

    @classmethod
    def values_without_none_split(cls):
        return cls.remove_value_from_values(cls.values_without_none(), cls.SPLIT)

    @classmethod
    def values_without_none_split_double(cls):
        return cls.remove_value_from_values(cls.values_without_none_split(), cls.DOUBLE)

    @classmethod
    def all_values(cls):
        return [value.value for value in cls.values_without_none()]

    @classmethod
    def values_no_split(cls):
        return [value.value for value in cls.values_without_none_split()]

    @classmethod
    def values_no_split_double(cls):
        return [value.value for value in cls.values_without_none_split_double()]

    @classmethod
    def values_up_low(cls, values):
        all_values = values
        upper_case_values = [value.upper() for value in values]
        all_values.extend(upper_case_values)
        return all_values

    @classmethod
    def all_values_up_low(cls):
        return cls.values_up_low(cls.all_values())

    @classmethod
    def values_no_split_up_low(cls):
        return cls.values_up_low(cls.values_no_split())

    @classmethod
    def values_no_split_double_up_low(cls):
        return cls.values_up_low(cls.values_no_split_double())


class Player(Contestant):

    def __init__(self, name, cash):
        super().__init__()
        self.name = name
        self.cash = cash
        self.bet_value = 0
        self.last_move = MoveType.NONE
        self.second_hand = []

    def add_card_to_second_hand(self, card):
        self.second_hand.append(card)

    def split(self):
        self.second_hand.append(self.__get_card_from_hand())

    def set_last_move(self, move_type):
        self.last_move = move_type

    def set_bet_value(self, bet):
        self.bet_value = bet

    def same_cards_value(self):
        return self.hand[0].sign.value == self.hand[1].sign.value

    def pay_bet_value(self):
        self.cash -= self.bet_value

    def double_bet_value(self):
        self.bet_value *= 2

    def __get_card_from_hand(self):
        card = self.hand[0]
        self.hand.remove(card)
        return card


class Game(object):

    def __init__(self, number_of_players):
        self.croupier = Croupier()
        self.players = []
        self.deck = Deck()
        self.create_players(number_of_players)
        self.deal_cards()
        self.print_croupier_card()
        self.players_betting()
        self.players_auction()
        self.get_croupier_cards()
        self.get_results()

    def create_players(self, number_of_players):
        for i in range(number_of_players):
            player_name = UserInputProvider().collect_str_from_user("Please enter player name: ")
            player_cash = UserInputProvider().collect_int_in_range_min_from_user(1, "Please enter amount of cash for %s: " % player_name)
            self.players.append(Player(player_name, player_cash))

    def deal_cards(self):
        for card_number in range(2):
            for player in self.players:
                card = self.deck.get_card()
                player.add_card_to_hand(card)
            self.croupier.add_card_to_hand(self.deck.get_card())

    def players_auction(self):
        while not all(
                player_last_move == MoveType.STAND or player_last_move == MoveType.DOUBLE for player_last_move in [player.last_move for player in self.players]):
            for player in self.players:
                if len(player.hand) >= 11:
                    player.set_last_move(MoveType.STAND)
                if player.last_move != MoveType.STAND and player.last_move != MoveType.DOUBLE:
                    print("%s have: %s, %s points" % (player.name, player.hand, player.count_score()))
                    choice = self.get_user_choice(player)
                    player.last_move = MoveType.match_move(choice)
                    self.game_action(choice, player)

    def get_user_choice(self, player):
        if player.cash >= player.bet_value and player.last_move == MoveType.NONE:
            return (UserInputProvider().collect_proper_str_from_user(MoveType.values_no_split_up_low(),
                                                                         "%s, please enter h for hit, st for stand or dd for double down: " % player.name)).lower()
        else:
            return (UserInputProvider().collect_proper_str_from_user(MoveType.values_no_split_double_up_low(),
                                                                     "%s, please enter h for hit or st for stand: " % player.name)).lower()

    def game_action(self, choice, player):
        if choice == MoveType.HIT.value:
            player.add_card_to_hand(self.deck.get_card())
        elif choice == MoveType.DOUBLE.value:
            player.add_card_to_hand(self.deck.get_card())
            self.croupier.get_money_from_player(player)
            player.set_last_move(MoveType.DOUBLE)
            print("You have %s, %s points and your bet value now is equal: %s" % (
                player.hand, player.count_score(), player.bet_value))

    def get_croupier_cards(self):
        while self.croupier.should_draw_cards():
            print("Croupier have: %s, %s points" % (self.croupier.hand, self.croupier.count_score()))
            self.croupier.add_card_to_hand(self.deck.get_card())
        else:
            print("Croupier have: %s, %s points" % (self.croupier.hand, self.croupier.count_score()))

    def print_croupier_card(self):
        print("Croupier have: ", self.croupier.get_single_card())

    def players_betting(self):
        for player in self.players:
            print("%s have: %s, %s points" % (player.name, player.hand, player.count_score()))
            player.set_bet_value(UserInputProvider().collect_int_in_range_min_max_from_user(1, player.cash,
                                                                                      "%s please enter your bet bigger than 1$: " % player.name))
            self.croupier.get_money_from_player(player)

    def add_croupier_to_players(self):
        return self.players.append(self.croupier)

    def remove_players_from_all_players(self, players):
        [self.players.remove(player) for player in players]

    def get_busters(self):
        self.add_croupier_to_players()
        busters = [player for player in self.players if player.count_score() > 21]
        self.remove_players_from_all_players(busters)
        return busters

    def get_scores(self, player):
        return player.count_score()

    def sort_players(self, players, boolean):
        return sorted(players, key=self.get_scores, reverse=boolean)

    def get_winners(self):
        self.players = self.sort_players(self.players, True)
        winners = [player for player in self.players if player.count_score() == self.players[0].count_score()]
        self.remove_players_from_all_players(winners)
        return winners

    def get_win_prize(self, winners):
        return int(self.croupier.casino / len(winners))

    def get_results(self):
        sorted_busters = self.sort_players(self.get_busters(), False)
        winners = self.get_winners()
        win_prize = self.get_win_prize(winners)
        if len(winners) > 0:
            if len(winners) > 1:
                print("The winners are: ", end="")
                for winner in winners:
                    winner.cash += win_prize
                    print("%s with %s points and %s $ prize - his cash capital is equal %s $" % (
                        winner.name, winner.count_score(), win_prize, winner.cash), end=", ")
            else:
                for winner in winners:
                    winner.cash += win_prize
                    print("The winner is: %s with %s points and %s $ prize - his cash capital is equal %s $" % (
                        winner.name, winner.count_score(), win_prize, winner.cash))
        while len(self.players) > 0:
            check_equals = self.check_if_equals(self.players)
            if len(check_equals) > 1:
                print("A draw have: ", end="")
                for equal in check_equals:
                    print("%s with %s points and cash capital equal %s $" % (equal.name, equal.count_score(), equal.cash), end=", ")
            else:
                for equal in check_equals:
                    print("%s have %s points and cash capital equal %s $" % (equal.name, equal.count_score(), equal.cash))
        while len(sorted_busters) > 0:
            check_equals = self.check_if_equals(sorted_busters)
            if len(check_equals) > 1:
                print("A busters with draw are: ", end="")
                for equal in check_equals:
                    print("%s with %s points and cash capital equal %s $" % (
                        equal.name, equal.count_score(), equal.cash))
            else:
                for equal in check_equals:
                    print("The buster is: %s with %s points and cash capital equal %s $" % (
                        equal.name, equal.count_score(), equal.cash))

    def check_if_equals(self, players):
        equal = []
        points = [player.count_score() for player in players]
        regex = (str(points[0]))
        results = re.findall(regex, str(points))
        for result in results:
            for player in players:
                if player.count_score() == int(result):
                    players.remove(player)
                    equal.append(player)
        return equal


Game(4)
