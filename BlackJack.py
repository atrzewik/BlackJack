class Card(object):

    def __init__(self, sign_index, colour_index, value_index):
        self.card = [self.sign()[sign_index] + " " + self.colour()[colour_index], self.value()[value_index]]

    def colour(self):
        return ["heart", "diamond", "peak", "club"]

    def sign(self):
        return ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def value(self):
        return [value + 1 for value in range(11)]


class Desk(object):

    def __init__(self):
        self.cards = self.list_of_card()
        self.desk = {}
        for i in range(len(self.cards)):
            self.desk[self.cards[i][0]] = self.cards[i][1]

    def list_of_card(self):
        cards = []
        for i in range(4):
            cards_in_colour = [Card(0, i, 1).card, Card(1, i, 2).card, Card(2, i, 3).card, Card(3, i, 4).card, Card(4, i, 5).card, Card(5, i, 6).card, Card(6, i, 7).card, Card(7, i, 8).card, Card(8, i, 9).card, Card(9, i, 9).card, Card(10, i, 9).card, Card(11, i, 9).card, Card(12, i, 0).card, Card(12, i, 10).card]
            cards.extend(cards_in_colour)
        return cards


print(Desk().desk)
