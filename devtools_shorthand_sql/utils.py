"""

fatal_error: Used when user input cannot be processed and program must terminate.

info_message: Print message to user that is informational in content only and does not indicate an error.

"""
import sys


def fatal_error(message):
    print('Error: ' + message)
    sys.exit()


def info_message(message):
    print('Info: ' + message)
