import pytest
from weakget import weakget


# Used below on the right of `%` to tell when weakget returns the default
default = object()


def test_new():
    wg = weakget(None)
    assert wg._weakget__obj is None

    wg = weakget(5)
    assert wg._weakget__obj == 5


def test_new_convert():
    # Ensure we don't create a weakget wrapping a pep505 wrapping a weakget wrapping...
    from weakget import pep505, _weakget__nothing

    with pytest.raises(TypeError):
        weakget(weakget(None))

    with pytest.raises(TypeError):
        weakget(weakget(5))

    with pytest.raises(TypeError):
        weakget(pep505(None))

    with pytest.raises(TypeError):
        weakget(pep505(5))

    with pytest.raises(TypeError):
        weakget(_weakget__nothing)


def test_getattr():
    result = weakget(range(5)).stop % default
    assert result == 5

    result = weakget(slice(5)).start % default
    assert result is None

    result = weakget(None).missingattr % default
    assert result is default

    result = weakget(range(5)).missingattr % default
    assert result is default


def test_getitem():
    result = weakget("abc")[1] % default
    assert result == "b"

    result = weakget("abc")[-1] % default
    assert result == "c"

    result = weakget("abc")[1:3] % default
    assert result == "bc"

    result = weakget([None])[0] % default
    assert result is None

    result = weakget(dict(a=1, b=2))["b"] % default
    assert result == 2

    result = weakget(dict(a=None))["a"] % default
    assert result is None

    with pytest.raises(TypeError):
        weakget(None)[1]

    with pytest.raises(TypeError):
        weakget(None)[-1]

    with pytest.raises(TypeError):
        weakget(None)[1:3]

    with pytest.raises(TypeError):
        weakget(None)["b"]

    result = weakget("abc")[99] % default
    assert result is default

    result = weakget("abc")[-99] % default
    assert result is default

    result = weakget("abc")[99:999] % default
    assert result == ""

    with pytest.raises(TypeError):
        weakget("abc")["b"]

    result = weakget(dict(a=1, b=2))["z"] % default
    assert result is default


def test_call():
    result = weakget("abc").upper() % default
    assert result == "ABC"

    result = weakget(None).upper() % default
    assert result is default

    result = weakget(5).upper() % default
    assert result is default

    result = weakget({}).pop("b", None) % default
    assert result is None
