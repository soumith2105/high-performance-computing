# Define ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

ALL_COLORS = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]


def print_green(*args, **kwargs):
    print(GREEN + " ".join(args), RESET, **kwargs)


def print_red(*args, **kwargs):
    print(RED + " ".join(args), RESET, **kwargs)


def print_yellow(*args, **kwargs):
    print(YELLOW + " ".join(args), RESET, **kwargs)


def print_blue(*args, **kwargs):
    print(BLUE + " ".join(args), RESET, **kwargs)


def print_magenta(*args, **kwargs):
    print(MAGENTA + " ".join(args), RESET, **kwargs)


def print_cyan(*args, **kwargs):
    print(CYAN + " ".join(args), RESET, **kwargs)


def return_colored_string(color, string):
    return f"{color}{string}{RESET}"
