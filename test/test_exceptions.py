"""Test pyprefab exceptions."""

from pyprefab.exceptions import PyprefabBadParameter


def test_pyprefab_bad_parameter_show(capsys):
    """PyprefabBadParameter show method works as expected."""
    pyprefab_exception = PyprefabBadParameter("oops!")
    assert pyprefab_exception.show_color is True
    assert pyprefab_exception.message == "❌ oops!"
    pyprefab_exception.show()
    captured = capsys.readouterr()
    assert "❌ oops!" in captured.err.strip()
