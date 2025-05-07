import nox

nox.options.default_venv_backend = 'uv'

PYPROJECT = nox.project.load_toml('pyproject.toml')
PYTHON_VERSIONS = nox.project.python_versions(PYPROJECT, max_version='3.14')
PYTHON_LATEST = '3.13'


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
def tests(session: nox.Session) -> None:
    """Install dependencies from lockfile and run tests."""
    session.run_install(
        'uv',
        'sync',
        '--active',
        '--group=dev',
        '--frozen',
        '--quiet',
        f'--python={session.virtualenv.location}',
    )
    if session.python == PYTHON_LATEST:
        session.run('coverage', 'erase')
        session.run('coverage', 'run', '-m', 'pytest')
    else:
        session.run('pytest')


@nox.session(tags=['ci'], python=PYTHON_LATEST, requires=[f'tests-{PYTHON_LATEST}'])
def coverage(session):
    """Check test coverage."""
    session.install('coverage')
    session.run('coverage', 'html')
    session.run('coverage', 'report', '--format', 'markdown')


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
        '--quiet',
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
        '--quiet',
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
