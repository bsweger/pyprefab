"""Test functionality of a Python package created by pyprefab."""

import ast
import subprocess


def test_build(cli_output):
    """Files created should build a valid python package."""
    package_path, cli_result = cli_output

    # pyprefab output should be a valid Python package
    result = subprocess.run(
        ['python', '-m', 'build', '--sdist', '--wheel'], capture_output=True, cwd=package_path, text=True
    )
    assert result.returncode == 0


def test_lint(cli_output):
    """Files created by CLI should lint without errors."""
    package_path, cli_result = cli_output

    result = subprocess.run(['ruff', 'check', package_path], capture_output=True, text=True)
    assert result.returncode == 0


def test_logging(cli_output):
    """Generated Python package should have functional logging."""
    package_path, cli_result = cli_output

    module_path = package_path / 'src'
    with open(module_path / 'log_test.py', 'w', encoding='utf-8') as f:
        f.write('from transporter_logs import app\n')
        f.write('app.logger.info("log test")\n')

    result = subprocess.run(['python', 'log_test.py'], capture_output=True, cwd=module_path, text=True)
    logs = ast.literal_eval(result.stdout)
    assert logs.get('event').lower() == 'log test'
    assert logs.get('level').lower() == 'info'
