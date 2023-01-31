from __future__ import annotations


def test_package_can_be_imported() -> None:
    from pleno_common import __version__

    assert len(__version__) > 0
