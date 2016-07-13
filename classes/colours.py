""" Module containing coloured output methods. """


class ColourPrint(object):
    """ class to allow printing in different colours. """

    def print_green(self, value):
        """ Prints the given value in green. """
        print("\033[0;32m{}\033[0m".format(value))

    def print_blue(self, value):
        """ Prints the given value in blue. """
        print("\033[0;36m{}\033[0m".format(value))

    def print_yellow(self, value):
        """ Prints the given value in yellow. """
        print("\033[0;33m{}\033[0m".format(value))

    def print_red(self, value):
        """ Prints the given value in yellow. """
        print("\033[0;31m{}\033[0m".format(value))
