from random import shuffle

from aenum import Enum, NoAlias

from UserInputProvider import *


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


class LastMove(Enum):
    _settings_ = NoAlias
    NONE = 'n'
    STAND = 'st'
    HIT = 'h'
    DOUBLE = 'd'
    SPLIT = 'sp'

    @classmethod
    def select_move(cls, player_move):
        for last_move in cls.values():
            if last_move.value == player_move:
                return last_move

    @classmethod
    def values(cls):
        return list(cls)


class Player(Contestant):

    def __init__(self, name, cash):
        super().__init__()
        self.name = name
        self.cash = cash
        self.bet_value = 0
        self.last_move = LastMove.NONE


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
        self.get_croupier_card()
        self.check_the_winner()

    def create_players(self, number_of_players):
        for i in range(number_of_players):
            player_name = UserInputProvider().collect_str_from_user("Please enter player name: ")
            player_cash = UserInputProvider().collect_int_from_user(
                "Please enter amount of cash for %s: " % player_name)
            self.players.append(Player(player_name, player_cash))

    def deal_cards(self):
        for card_number in range(2):
            for player in self.players:
                card = self.deck.get_card()
                player.add_card_to_hand(card)
            self.croupier.add_card_to_hand(self.deck.get_card())

    def players_auction(self):
        while not all(player_last_move == LastMove.STAND for player_last_move in [player.last_move for player in self.players]):
            for player in self.players:
                if player.last_move != LastMove.STAND:
                    print("%s have: %s, %s points" % (player.name, player.hand, player.count_score()))
                    choice = self.take_user_choice(player)
                    player.last_move = LastMove.select_move(choice)
                    self.game_action(choice, player)

    def take_user_choice(self, player):
        if player.cash < player.bet_value:
            return (UserInputProvider().collect_proper_str_from_user(["h", "st", "H", "ST"],
                                                          "%s, please enter h for hit, st for stand: " % player.name)).lower()
        else:
            return (UserInputProvider().collect_proper_str_from_user(["h", "st", "H", "ST", "dd", "DD"],
                                                          "%s, please enter h for hit, st for stand, dd for double down: " % player.name)).lower()

    def game_action(self, choice, player):
        if choice == "h":
            player.add_card_to_hand(self.deck.get_card())
        elif choice == "dd":
            player.add_card_to_hand(self.deck.get_card())
            player.cash -= player.bet_value
            self.croupier.casino += player.bet_value
            player.bet_value *= 2
            print("Your bet value now is equal: %s" % player.bet_value)

    def get_croupier_card(self):
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
            player.bet_value = int(UserInputProvider().collect_int_in_range_from_user(1, player.cash,
                                                                                      "%s please enter your bet bigger than 1$: " % player.name))
            player.cash -= player.bet_value
            self.croupier.casino += player.bet_value

    def get_busters(self):
        self.players.append(self.croupier)
        busters = [player for player in self.players if player.count_score() > 21]
        [self.players.remove(buster) for buster in busters]
        return busters

    def get_scores(self, player):
        return player.count_score()

    def check_the_winner(self):
        sorted_busters = sorted(self.get_busters(), key=self.get_scores)
        sorted_players = sorted(self.players, key=self.get_scores, reverse=True)
        winners = [player for player in sorted_players if player.count_score() == sorted_players[0].count_score()]
        [sorted_players.remove(player) for player in sorted_players if player in winners]
        if len(winners) > 0:
            win_prize = int(self.croupier.casino / len(winners))
            for winner in winners:
                winner.cash += win_prize
                print("The winner is: %s with %s points and %s $ prize - his cash capital is equal %s $" % (winner.name, winner.count_score(), win_prize, winner.cash))
        if len(sorted_players) > 0:
            for player in sorted_players:
                print("%s have %s points and cash capital equal %s $" % (player.name, player.count_score(), player.cash))
        if len(sorted_busters) > 0:
            for buster in sorted_busters:
                print("The buster is: %s with %s points and cash capital equal %s $" % (buster.name, buster.count_score(), buster.cash))


Game(2)

