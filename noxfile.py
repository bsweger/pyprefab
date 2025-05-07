import nox

nox.options.default_venv_backend = 'uv'

PYPROJECT = nox.project.load_toml('pyproject.toml')
PYTHON_VERSIONS = nox.project.python_versions(PYPROJECT, max_version='3.14')


@nox.session(tags=['ci'])
def lint(session: nox.Session) -> None:
    """Run the linter."""
    session.install('ruff')
    session.run('ruff', 'check', '.')


@nox.session(tags=['ci'])
def typecheck(session: nox.Session) -> None:
    """Run static type checking."""
    session.install('mypy')
    session.run('mypy', 'src', 'test')


@nox.session(python=PYTHON_VERSIONS, tags=['ci'])
def test(session: nox.Session) -> None:
    """Install dependencies from lockfile and run tests."""
    session.run_install(
        'uv',
        'sync',
        '--active',
        '--group=dev',
        '--frozen',
        f'--python={session.virtualenv.location}',
    )
    session.run('pytest')


@nox.session(python=PYTHON_VERSIONS)
def test_install(session: nox.Session) -> None:
    """Install as a package and run tests."""
    session.run_install(
        'uv',
        'pip',
        'install',
        '-e',
        '.',
        '--group=dev',
        f'--python={session.virtualenv.location}',
    )
    session.run('pytest')


@nox.session(tags=['ci'])
@nox.parametrize('python', ['3.10', '3.11', '3.12', '3.13'])  # 3.14 can't build
def docs(session: nox.Session) -> None:
    """Build the documentation."""
    session.run_install(
        'uv',
        'sync',
        '--active',
        '--group=docs',
        '--frozen',
        f'--python={session.virtualenv.location}',
    )
    session.run('sphinx-build', '-W', '-b', 'html', 'docs/source', 'docs/_build/html')


@nox.session
def docs_serve(session: nox.Session) -> None:
    """Serve the documentation locally."""
    session.run_install(
        'uv',
        'sync',
        '--active',
        '--group=docs',
        '--frozen',
        f'--python={session.virtualenv.location}',
    )
    session.run('sphinx-autobuild', 'docs/source', 'docs/_build/html', external=True)
