"""Custom exceptions for PyPrefab."""

import typing as t
from gettext import gettext as _

import click
import typer


def style_message(message) -> str:
    """
    Style the message for display.

    Use Click's style function to format the error message because error
    messages emitted from the callback function of an interactive prompt
    use Click's echo function, which does not support rich text.
    https://click.palletsprojects.com/en/stable/api/#click.style
    """
    message = click.style(f"{message}")  # colors would go here
    message = f"❌ {message}"
    return message


class PyprefabBadParameter(typer.BadParameter):
    """Custom exception for bad parameters in PyPrefab CLI."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = style_message(message)
        self.show_color = True

    def show(self, file: t.Optional[t.IO[t.Any]] = None) -> None:
        """
        Override show() method in Click exceptions.

        This method is currently a no-op, because Click does not
        use the show() method to print exception messages when the
        exception comes from prompted input.

        The related Click code is in termui.prompt(). To override the default
        behavior, you can change the except UsageError block in prompt_func()
        to:

         except UsageError as e:
            if hide_input:
                echo(_("Error: The value you entered was invalid."), err=err)
            else:
               # use the exception's show() method to print the error message
               e.show()
        """
        click.echo(_(self.message), err=True)
