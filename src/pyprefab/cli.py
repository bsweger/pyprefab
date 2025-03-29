"""Command-line interface for the pyprefab package."""

import shutil
import sys
from pathlib import Path
from typing import Optional

import structlog
import typer
from jinja2 import Environment, FileSystemLoader
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme
from typing_extensions import Annotated

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
    help='Generate python project scaffolding based on pyprefab.',
    rich_markup_mode='rich',
)


def validate_project_name(name: str) -> bool:
    """Validate project name follows Python package naming conventions."""
    return name.isidentifier() and name.islower()


def render_templates(context: dict, templates_dir: Path, target_dir: Path):
    """Render Jinja templates to target directory."""
    # Process templates
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    # For rendering path names
    path_env = Environment(
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
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
            help='Name of the project',
            prompt=typer.style('Project name 🐍', fg=typer.colors.MAGENTA, bold=True),
            show_default=False,
        ),
    ],
    author: Annotated[
        Optional[str],
        typer.Option(
            help='Project author',
            prompt=typer.style('Project author 👤', fg=typer.colors.MAGENTA, bold=True),
        ),
    ] = 'None',
    description: Annotated[
        Optional[str],
        typer.Option(
            help='Project description',
            prompt=typer.style('Project description 📝', fg=typer.colors.MAGENTA, bold=True),
        ),
    ] = 'None',
    project_dir: Annotated[
        Path,
        typer.Option(
            '--dir',
            help='Directory that will contain the project',
            prompt=typer.style('Project directory 🎬', fg=typer.colors.MAGENTA, bold=True),
        ),
    ] = Path.cwd(),
    docs: Annotated[
        Optional[bool],
        typer.Option(
            help='Include Sphinx documentation files',
            prompt=typer.style('Include Sphinx docs? 📄', fg=typer.colors.MAGENTA, bold=True),
        ),
    ] = False,
):
    """
    🐍 Create Python package boilerplate 🐍
    """
    if not validate_project_name(name):
        err_console = Console(stderr=True)
        err_console.print(
            Panel.fit(
                f'⛔️ Package not created: {name} is not a valid Python package name',
                title='pyprefab error',
                border_style='red',
            )
        )
        raise typer.Exit(1)

    if project_dir.exists() and any(project_dir.iterdir()):
        err_console = Console(stderr=True)
        err_console.print(
            Panel.fit(
                f'⛔️ Package not created: {str(project_dir)} is not an empty directory',
                title='pyprefab error',
                border_style='red',
            )
        )
        raise typer.Exit(1)

    templates_dir = Path(__file__).parent / 'templates'
    target_dir = project_dir or Path.cwd() / name

    try:
        # Create project directory
        target_dir.mkdir(parents=True, exist_ok=True)

        # Template context
        context = {
            'project_name': name,
            'author': author,
            'description': description,
            'docs': docs,
        }

        # Write Jinja templates to project directory
        render_templates(context, templates_dir, target_dir)
        panel_msg = (
            f'✨ Created new project [bold green]{name}[/] in {target_dir}\n'
            f'Author: [blue]{author}[/]\n'
            f'Description: {description}'
        )
        if docs:
            panel_msg += f'\nDocumentation: {target_dir}/docs'
        print(
            Panel.fit(
                panel_msg,
                title='Project Created Successfully',
                border_style='green',
            )
        )

    except Exception as e:
        err_console = Console(stderr=True)
        err_console.print(
            Panel.fit(
                f'⛔️ Error creating project: {str(e)}',
                title='pyprefab error',
                border_style='red',
            )
        )
        typer.secho(f'Error creating project: {str(e)}', fg=typer.colors.RED)
        if target_dir.exists():
            shutil.rmtree(target_dir)
        raise typer.Exit(1)


if __name__ == '__main__':
    sys.exit(app())  # pragma: no cover
