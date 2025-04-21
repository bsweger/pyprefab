import nox

PYTHON_VERSIONS = ['3.9', '3.10', '3.11', '3.12', '3.13']


@nox.session
def lint(session: nox.Session) -> None:
    """Run the linter."""
    session.run('uv', 'pip', 'install', 'ruff', external=True)
    session.run('ruff', 'check', '.')


@nox.session
def typecheck(session: nox.Session) -> None:
    """Run static type checking."""
    session.run('uv', 'pip', 'install', 'mypy', external=True)
    session.run('mypy', 'src', 'test')


@nox.session(python=PYTHON_VERSIONS)
def test(session: nox.Session) -> None:
    """Run tests."""
    session.run('uv', 'sync', external=True)
    session.run('pytest', 'test', '--cov')


@nox.session(python=PYTHON_VERSIONS)
def docs(session: nox.Session) -> None:
    """Build Sphinx documentation."""
    session.run('uv', 'pip', 'install', 'sphinx', 'sphinx-rtd-theme', external=True)
    session.run('sphinx-build', '-W', '-b', 'html', 'docs/source', 'docs/build/html')


@nox.session
def docs_serve(session: nox.Session) -> None:
    """Serve the documentation locally."""
    session.run('uv', 'pip', 'install', 'sphinx', 'sphinx-rtd-theme', 'sphinx-autobuild', external=True)
    session.run('sphinx-autobuild', 'docs/source', 'docs/build/html')
