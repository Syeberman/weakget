import pytest
from weakget import pep505


# FIXME Add tests for None mid-get, i.e. pep505([None])[0].upper(), as [None][0] is None

# Used below on the right of `%` to tell when pep505 returns the default
default = object()


def test_new():
    from weakget import _weakget__nothing

    pp = pep505(None)
    assert pp is _weakget__nothing  # unlike weakget

    pp = pep505(5)
    assert pp._pep505__obj == 5


def test_new_convert():
    # Ensure we don't create a weakget wrapping a pep505 wrapping a weakget wrapping...
    from weakget import weakget, _weakget__nothing

    with pytest.raises(TypeError):
        pep505(weakget(None))

    with pytest.raises(TypeError):
        pep505(weakget(5))

    with pytest.raises(TypeError):
        pep505(pep505(None))

    with pytest.raises(TypeError):
        pep505(pep505(5))

    with pytest.raises(TypeError):
        pep505(_weakget__nothing)


def test_getattr():
    result = pep505(range(5)).stop % default
    assert result == 5

    result = pep505(slice(5)).start % default
    assert result is default  # unlike weakget (recall slice(5).start is None)

    result = pep505(None).missingattr % default
    assert result is default

    with pytest.raises(AttributeError):  # unlike weakget
        pep505(range(5)).missingattr


def test_getitem():
    result = pep505("abc")[1] % default
    assert result == "b"

    result = pep505("abc")[-1] % default
    assert result == "c"

    result = pep505("abc")[1:3] % default
    assert result == "bc"

    result = pep505([None])[0] % default
    assert result is default  # unlike weakget

    result = pep505(dict(a=1, b=2))["b"] % default
    assert result == 2

    result = pep505(dict(a=None))["a"] % default
    assert result is default  # unlike weakget

    result = pep505(None)[1] % default
    assert result is default  # unlike weakget

    result = pep505(None)[-1] % default
    assert result is default  # unlike weakget

    result = pep505(None)[1:3] % default
    assert result is default  # unlike weakget

    result = pep505(None)["b"] % default
    assert result is default  # unlike weakget

    with pytest.raises(IndexError):  # unlike weakget
        pep505("abc")[99]

    with pytest.raises(IndexError):  # unlike weakget
        pep505("abc")[-99]

    result = pep505("abc")[99:999] % default
    assert result == ""

    with pytest.raises(TypeError):
        pep505("abc")["b"]

    with pytest.raises(KeyError):  # unlike weakget
        pep505(dict(a=1, b=2))["z"]


def test_call():
    result = pep505("abc").upper() % default
    assert result == "ABC"

    result = pep505(None).upper() % default
    assert result is default

    with pytest.raises(AttributeError):  # unlike weakget
        pep505(5).upper()

    result = pep505({}).pop("b", None) % default
    assert result is default  # unlike weakget


def test_new_multi():
    from weakget import _weakget__nothing

    pp = pep505(None, 5, None)
    assert isinstance(pp, pep505)
    assert pp._pep505__obj == 5

    pp = pep505(None, None)
    assert pp is _weakget__nothing

    with pytest.raises(TypeError):
        pep505()
