"""Custom exceptions for PyPrefab."""

import typer


def style_message(message) -> str:
    """
    Style the message for display.
    """
    message = f"❌ {message}"
    return message


class PyprefabBadParameter(typer.BadParameter):
    """Custom exception for bad parameters in PyPrefab CLI."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = style_message(message)
        self.show_color = True
