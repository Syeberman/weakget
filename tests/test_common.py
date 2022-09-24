"""Test behaviours common between "all" weakget objects: weakget, pep505, _weakget__nothing
"""

import pytest
from weakget import weakget, pep505, _weakget__nothing


class attrs:
    def __init__(self):
        self.attr = None


def attr_constructors():
    """A decorator for parametrized tests that test particular (mutable) attribute accesses."""
    return pytest.mark.parametrize(
        "newobj",
        [
            lambda: weakget(attrs()),
            lambda: pep505(attrs()),
            lambda: _weakget__nothing,  # a singleton
        ],
        ids=("weakget", "pep505", "_weakget__nothing"),
    )


def sequence_constructors():
    """A decorator for parametrized tests that test particular (mutable) sequence operations."""
    return pytest.mark.parametrize(
        "newobj",
        [
            lambda: weakget([0, 1, 2]),
            lambda: pep505([0, 1, 2]),
            lambda: _weakget__nothing,  # a singleton
        ],
        ids=("weakget", "pep505", "_weakget__nothing"),
    )


def mapping_constructors():
    """A decorator for parametrized tests that test particular (mutable) mapping operations."""
    return pytest.mark.parametrize(
        "newobj",
        [
            lambda: weakget({"item": 0}),
            lambda: pep505({"item": 0}),
            lambda: _weakget__nothing,  # a singleton
        ],
        ids=("weakget", "pep505", "_weakget__nothing"),
    )


def number_constructors():
    """A decorator for parametrized tests that test particular number operations."""
    return pytest.mark.parametrize(
        "newobj",
        [
            lambda: weakget(0),
            lambda: pep505(0),
            lambda: _weakget__nothing,  # a singleton
        ],
        ids=("weakget", "pep505", "_weakget__nothing"),
    )


@attr_constructors()
def test_setattr(newobj):
    with pytest.raises(AttributeError):
        newobj().attr = None
    with pytest.raises(AttributeError):
        newobj().newattr = None


@attr_constructors()
def test_delattr(newobj):
    with pytest.raises(AttributeError):
        del newobj().attr
    with pytest.raises(AttributeError):
        del newobj().missingattr


@sequence_constructors()
def test_setitem_sequence(newobj):
    with pytest.raises(TypeError):
        newobj()[0] = None
    with pytest.raises(TypeError):
        newobj()[:] = [None]


@mapping_constructors()
def test_setitem_mapping(newobj):
    with pytest.raises(TypeError):
        newobj()["item"] = None
    with pytest.raises(TypeError):
        newobj()["newitem"] = None


@sequence_constructors()
def test_delitem_sequence(newobj):
    with pytest.raises(TypeError):
        del newobj()[0]
    with pytest.raises(TypeError):
        del newobj()[:]


@mapping_constructors()
def test_delitem_mapping(newobj):
    with pytest.raises(TypeError):
        del newobj()["item"]
    with pytest.raises(TypeError):
        del newobj()["missingitem"]


@number_constructors()  # underlying int supports bool
def test_bool(newobj):
    with pytest.raises(TypeError):
        bool(newobj())
    with pytest.raises(TypeError):
        newobj() and None
    with pytest.raises(TypeError):
        newobj() or None
    with pytest.raises(TypeError):
        not newobj()


@number_constructors()  # underlying int supports all comparison operators
def test_comparisons(newobj):
    with pytest.raises(TypeError):
        newobj() == 0
    with pytest.raises(TypeError):
        newobj() != 0
    with pytest.raises(TypeError):
        newobj() > 0
    with pytest.raises(TypeError):
        newobj() >= 0
    with pytest.raises(TypeError):
        newobj() <= 0
    with pytest.raises(TypeError):
        newobj() < 0


@number_constructors()  # underlying int supports hash
def test_hash(newobj):
    with pytest.raises(TypeError):
        hash(newobj())
    with pytest.raises(TypeError):
        {newobj(): None}
