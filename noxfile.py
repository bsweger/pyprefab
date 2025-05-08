import nox

nox.options.default_venv_backend = 'uv'

PYPROJECT = nox.project.load_toml('pyproject.toml')
PYTHON_VERSIONS = nox.project.python_versions(PYPROJECT)
# assume that the programming version classifies in pyproject.toml are in ascending order
PYTHON_LATEST = PYTHON_VERSIONS[-1]
COVERAGE_THRESHOLD = 90


@nox.session(tags=['checks', 'ci'])
def lint(session: nox.Session) -> None:
    """Run the linter."""
    session.install('ruff')
    session.run('ruff', 'check', '.')


@nox.session(tags=['checks', 'ci'])
def typecheck(session: nox.Session) -> None:
    """Run static type checking."""
    session.install('mypy')
    session.run('mypy', 'src', 'test')


@nox.session(python=PYTHON_VERSIONS, tags=['checks', 'ci'])
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
    session.run('pytest')


@nox.session(tags=['checks', 'ci'], python=PYTHON_LATEST, requires=[f'tests-{PYTHON_LATEST}'])
def coverage(session) -> None:
    """Check test coverage."""
    session.run_install(
        'uv',
        'sync',
        '--active',
        '--group=dev',
        '--frozen',
        '--quiet',
        f'--python={session.virtualenv.location}',
    )
    session.run('coverage', 'erase', silent=True)
    session.run('coverage', 'run', '-m', 'pytest', '--quiet', '--no-header', '--no-summary', silent=True)
    session.run('coverage', 'html', '--skip-covered', '--skip-empty', silent=True)
    session.run(
        'coverage',
        'report',
        '--format',
        'markdown',
        f'--fail-under={COVERAGE_THRESHOLD}',
    )


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


@nox.session(python=PYTHON_VERSIONS, tags=['checks', 'ci'])
def docs(session: nox.Session) -> None:
    """Build the documentation."""
    session.run_install(
        'uv',
        'sync',
        '--active',
        '--group=docs',
        '--frozen',
        #'--quiet',
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
