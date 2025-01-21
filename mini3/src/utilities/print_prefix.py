import builtins

_original_print = builtins.print  # Store the original print function


def set_print_prefix(prefix):
    """
    Overrides the built-in print function to add a custom prefix.
    """

    def custom_print(*args, **kwargs):
        # Add the prefix before all print statements
        _original_print(f"[{prefix}]".ljust(12), *args, **kwargs)

    # Override the built-in print function
    builtins.print = custom_print
