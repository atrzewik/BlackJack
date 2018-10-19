class UserInputProvider(object):

    @staticmethod
    def collect_int_in_range_min_max_from_user(minimum, maximum, message):
        user_input = UserInputProvider.collect_int_from_user(message)
        if minimum <= user_input <= maximum:
            return user_input
        else:
            UserInputProvider.__print_error(
                "You must input value in range: {} - {}! Please try again: ".format(minimum, maximum))
            return UserInputProvider.collect_int_in_range_min_max_from_user(minimum, maximum, message)

    @staticmethod
    def collect_int_in_range_min_from_user(minimum, message):
        user_input = UserInputProvider.collect_int_from_user(message)
        if minimum <= user_input:
            return user_input
        else:
            UserInputProvider.__print_error(
                "You must input value bigger then {} ! Please try again: ".format(minimum))
            return UserInputProvider.collect_int_in_range_min_from_user(minimum, message)

    @staticmethod
    def collect_proper_str_from_user(list_of_string, message):
        user_input = UserInputProvider.collect_str_from_user(message)
        if user_input in list_of_string:
            return user_input
        else:
            UserInputProvider.__print_error(
                "You must input string: {}! Please try again: ".format(list_of_string))
            return UserInputProvider.collect_proper_str_from_user(list_of_string, message)

    @staticmethod
    def collect_str_from_user(message):
        return UserInputProvider.__collect_user_input_in_type(message, str)

    @staticmethod
    def collect_int_from_user(message):
        return UserInputProvider.__collect_user_input_in_type(message, int)

    @staticmethod
    def __collect_user_input_in_type(message, input_type):
        while True:
            try:
                return input_type(UserInputProvider.collect_user_input(message))
            except ValueError:
                UserInputProvider.__print_error("Input must be {}! Try again: ".format(input_type))
                continue

    @staticmethod
    def collect_user_input(message):
        return input(message)

    @staticmethod
    def __print_error(error_message):
        print(error_message)

