class Cards(object):

    def __init__(self):
        self.cards = list(self.waist().keys())
        self.cards_and_values = self.waist()

    def waist(self):
        waist = {}
        waist = self.cards_and_values(waist, self.heart())
        waist = self.cards_and_values(waist, self.diamond())
        waist = self.cards_and_values(waist, self.peak())
        waist = self.cards_and_values(waist, self.club())
        return waist

    def heart(self):
        key_list = self.key_list()
        key_list = [key + " heart" for key in key_list]
        return key_list

    def diamond(self):
        key_list = self.key_list()
        key_list = [key + " diamond" for key in key_list]
        return key_list

    def peak(self):
        key_list = self.key_list()
        key_list = [key + " peak" for key in key_list]
        return key_list

    def club(self):
        key_list = self.key_list()
        key_list = [key + " club" for key in key_list]
        return key_list

    def cards_and_values(self, dict_of_colour, key_colour_list):
        for key, value in zip(key_colour_list, self.value_list()):
            dict_of_colour[key] = value
        return dict_of_colour

    def key_list(self):
        key = list(self.cards_with_number().keys())
        key.extend(list(self.figures().keys()))
        key.extend(list(self.ace().keys()))
        return key

    def value_list(self):
        value = list(self.cards_with_number().values())
        value.extend(list(self.figures().values()))
        value.extend(list(self.ace().values()))
        return value

    @staticmethod
    def cards_with_number():
        return {str(x+2): x+2 for x in range(9)}

    @staticmethod
    def figures():
        figures = ["Jack", "Queen", "King"]
        return {figures[x]: 10 for x in range(len(figures))}

    @staticmethod
    def ace():
        return {"Ace": [1, 11]}


print(Cards().cards)
print(Cards().cards_and_values)
