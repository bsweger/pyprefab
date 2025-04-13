"""Command-line interface for the pyprefab package."""

import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import structlog
import typer
from jinja2 import Environment, FileSystemLoader, select_autoescape
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme
from typing_extensions import Annotated

from pyprefab import __version__
from pyprefab.exceptions import PyprefabBadParameter
from pyprefab.logging import setup_logging

setup_logging()
logger = structlog.get_logger()

cli_theme = Theme(
    {
        'help': 'bold cyan',
        'option': 'bold yellow',
        'argument': 'bold magenta',
    }
)

# Create a console with the custom theme
console = Console(theme=cli_theme)
app = typer.Typer(
    add_completion=False,
    help='Generate python package scaffolding based on pyprefab.',
    rich_markup_mode='rich',
)


def validate_package_name(value: str) -> str:
    """Validate that package name follows Python package naming conventions."""
    if not value.isidentifier():
        if value[0].isdigit():
            msg = 'Python package names cannot start with a number'
        else:
            msg = 'Python package names must contain letters, numbers, or underscores'
        raise PyprefabBadParameter(msg)
    else:
        return value


def version_callback(value: bool):
    """Return the package version."""
    if value:
        print(f'pyprefab {__version__}')
        raise typer.Exit()


def render_templates(context: dict, templates_dir: Path, target_dir: Path):
    """Render Jinja templates to target directory."""
    # Process templates
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        autoescape=select_autoescape(),
    )
    # For rendering path names
    path_env = Environment(
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        autoescape=select_autoescape(),
    )

    for template_file in templates_dir.rglob('*'):
        if template_file.is_file():
            rel_path = template_file.relative_to(templates_dir)
            if str(rel_path.parents[0]).startswith('docs') and not context.get('docs'):
                continue
            template = env.get_template(str(rel_path))
            output = template.render(**context)

            # Process path parts through Jinja
            path_parts = []
            for part in rel_path.parts:
                # Render each path component through Jinja
                rendered_part = path_env.from_string(part).render(**context)
                if rendered_part.endswith('.j2'):
                    rendered_part = rendered_part[:-3]
                path_parts.append(rendered_part)

            # Create destination path preserving structure
            dest_file = target_dir.joinpath(*path_parts)
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_file, 'w', encoding='utf-8', newline='\n') as f:
                f.write(output)


@app.command()
def main(
    name: Annotated[
        Optional[str],
        typer.Option(
            help='Name of the package',
            prompt=typer.style('Package name 🐍', fg=typer.colors.MAGENTA, bold=True),
            callback=validate_package_name,
            show_default=False,
        ),
    ],
    author: Annotated[
        Optional[str],
        typer.Option(
            help='Package author',
            prompt=typer.style('Package author 👤', fg=typer.colors.MAGENTA, bold=True),
        ),
    ] = 'None',
    description: Annotated[
        Optional[str],
        typer.Option(
            help='Package description',
            prompt=typer.style('Package description 📝', fg=typer.colors.MAGENTA, bold=True),
        ),
    ] = 'None',
    package_dir: Annotated[
        Path,
        typer.Option(
            '--dir',
            help='Directory that will contain the package',
            prompt=typer.style('Package directory 🎬', fg=typer.colors.MAGENTA, bold=True),
        ),
    ] = Path.cwd(),
    docs: Annotated[
        Optional[bool],
        typer.Option(
            help='Include Sphinx documentation files',
            prompt=typer.style('Include Sphinx docs? 📄', fg=typer.colors.MAGENTA, bold=True),
        ),
    ] = False,
    version: Annotated[
        Optional[bool],
        typer.Option('--version', callback=version_callback, is_eager=True),
    ] = None,
):
    """
    🐍 Create Python package boilerplate 🐍
    """
    # If there is already content in the package directory, exit (unless
    # the directory is on the exception list below)
    allow_existing = ['.git']
    exceptions = [allow for allow in allow_existing if (package_dir / allow).is_dir()]

    if package_dir.exists() and sum(1 for item in package_dir.iterdir()) - len(exceptions) > 0:
        err_console = Console(stderr=True)
        err_console.print(
            Panel.fit(
                f'⛔️ Package not created: {str(package_dir)} is not an empty directory',
                title='pyprefab error',
                border_style='red',
            )
        )
        raise typer.Exit(1)

    templates_dir = Path(__file__).parent / 'templates'
    target_dir = package_dir or Path.cwd() / name

    current_year = datetime.now().year

    try:
        # Create package directory
        target_dir.mkdir(parents=True, exist_ok=True)
        # Template context
        context = {
            'author': author,
            'current_year': current_year,
            'description': description,
            'docs': docs,
            'package_name': name,
        }

        # Write Jinja templates to package directory
        render_templates(context, templates_dir, target_dir)
        panel_msg = (
            f'✨ Created new package [bold green]{name}[/] in {target_dir}\n'
            f'Author: [blue]{author}[/]\n'
            f'Description: {description}'
        )
        if docs:
            panel_msg += f'\nDocumentation: {target_dir}/docs'
        print(
            Panel.fit(
                panel_msg,
                title='Package Created Successfully',
                border_style='green',
            )
        )

    except Exception as e:
        err_console = Console(stderr=True)
        err_console.print(
            Panel.fit(
                f'⛔️ Error creating package: {str(e)}',
                title='pyprefab error',
                border_style='red',
            )
        )
        typer.secho(f'Error creating package: {str(e)}', fg=typer.colors.RED)
        if target_dir.exists():
            shutil.rmtree(target_dir)
        raise typer.Exit(1)


if __name__ == '__main__':
    sys.exit(app())  # pragma: no cover
