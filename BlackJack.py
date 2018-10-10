from random import sample
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

    def shuffle_deck(self):
        return sample(self.cards, len(self.cards))

    def delete_card_from_deck(self, deck, card):
        deck.remove(card)

    def get_cards(self, hand, deck, number):
        for i in range(number):
            hand.append(deck[0])
            Deck().delete_card_from_deck(deck, deck[0])


class Contestant(object):

    def __init__(self, name, bet_value, hand):
        self.name = name
        self.hand = hand
        self.bet_value = bet_value
        self.score = 0

    def count_score(self):
        result = 0
        for card in self.hand:
            result += card.sign.value
        return result

    def check_if_ace_in_hand(self):
        list_of_signs = [card.sign for card in self.hand]
        if Sign.ACE in list_of_signs:
            return True

    def print_cards(self):
        return self.hand


class Croupier(Contestant):

    def action_if_ace_in_croupier_hand(self, deck):
        score = self.count_score()
        if 16 < score + 10 <= 21:
            score += 10
            return score
        else:
            Deck().get_cards(self.hand, deck, 1)
            print("Croupier have: ", self.print_cards())
            return self.get_croupier_score(deck)

    def get_croupier_score(self, deck):
        score = self.count_score()
        if score <= 16:
            if self.check_if_ace_in_hand():
                return self.action_if_ace_in_croupier_hand(deck)
            else:
                Deck().get_cards(self.hand, deck, 1)
                print("Croupier have: ", self.print_cards())
                return self.get_croupier_score(deck)
        else:
            return score


class Player(Contestant):

    def select_activity(self, deck):
        activity = UserInputProvider().collect_proper_str_from_user(["h", "st", "dd"], "%s please enter h for hit, st for stand or dd for double down: " % self.name)
        if activity == "h":
            self.hit(deck)
        elif activity == "st":
            self.stand()
        elif activity == "dd":
            self.double_down(deck)

    def hit(self, deck):
        Deck().get_cards(self.hand, deck, 1)
        print("You have: ", self.print_cards())
        self.select_activity(deck)

    def stand(self):
        self.score = self.get_player_score()
        print("Your score is: ", self.score)

    def double_down(self, deck):
        Deck().get_cards(self.hand, deck, 1)
        self.bet_value = self.bet_value * 2
        print("You have: ", self.print_cards(), "Your bet is equal to: %s $" % self.bet_value)
        self.select_activity(deck)

    def get_player_score(self):
        score = self.count_score()
        if self.check_if_ace_in_hand():
            decision = int(UserInputProvider().collect_proper_str_from_user(["1", "11"], "What value of ACE do you prefer? Enter 1 or 11: "))
            if decision == 11:
                score += 10
        return score


class Game(object):

    def __init__(self):
        self.croupier = Croupier("Croupier", 0, [])
        self.number_of_players = UserInputProvider().collect_int_in_range_from_user(1, 6, "Please enter number of players: 1 - 6: ")
        self.players = []
        for i in range(self.number_of_players):
            player = Player(self.give_name(i), 0, [])
            self.players.append(player)
        deck = Deck().shuffle_deck()
        Deck().get_cards(self.croupier.hand, deck, 2)
        print("Croupier have: ", self.croupier.hand[0])
        for player in self.players:
            Deck().get_cards(player.hand, deck, 2)
            print("%s have: " % player.name, player.hand)
            player.bet_value = self.bet(player.name)
            player.select_activity(deck)
        self.croupier.score = self.croupier.get_croupier_score(deck)
        print("Croupier score is: ", self.croupier.score)
        self.players.append(self.croupier)
        self.check_the_buster()
        self.check_the_winner()

    @staticmethod
    def give_name(player_s_number):
        name = UserInputProvider().collect_str_from_user("Please enter name for %s player: " % (player_s_number + 1))
        return name

    @staticmethod
    def bet(name):
        return int(UserInputProvider().collect_int_in_range_from_user(5, 500, "%s please enter your amount of bet bigger than 5$, less then 500$: " % name))

    def check_the_buster(self):
        busters = []
        for player in self.players:
            if player.score > 21:
                print("%s bust" % player.name)
                busters.append(player)
                self.croupier.bet_value += player.bet_value
        for buster in busters:
            self.players.remove(buster)

    def check_the_winner(self):
        players_scores = []
        for player in self.players:
            players_scores.append(player.score)
        winning_score = max(players_scores)
        winners = []
        for player in self.players:
            if player.score == winning_score:
                winners.append(player)
            else:
                self.croupier.bet_value += player.bet_value
                print("%s lose" % player.name)
        if len(winners) > 1:
            for winner in winners:
                print(winner.name, "won %s $" % winner.bet_value, end=", ")
            print("and they have a draw")
        else:
            winner = winners[0]
            print("%s is the winner, and won %s $" % (winner.name, winner.bet_value))


print(Game())
