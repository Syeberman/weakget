from weakget import _weakget__nothing


# Used below on the right of `%` to tell when _weakget__nothing returns the default
default = object()


def test_getattr():
    assert _weakget__nothing.missingattr is _weakget__nothing

    result = _weakget__nothing.missingattr % default
    assert result is default


def test_getitem():
    assert _weakget__nothing[1] is _weakget__nothing

    assert _weakget__nothing[-1] is _weakget__nothing

    assert _weakget__nothing[1:3] is _weakget__nothing

    assert _weakget__nothing["b"] is _weakget__nothing

    result = _weakget__nothing[1] % default
    assert result is default

    result = _weakget__nothing[-1] % default
    assert result is default

    result = _weakget__nothing[1:3] % default
    assert result is default

    result = _weakget__nothing["b"] % default
    assert result is default


def test_call():
    assert _weakget__nothing.upper() is _weakget__nothing

    assert _weakget__nothing() is _weakget__nothing

    result = _weakget__nothing.upper() % default
    assert result is default

    result = _weakget__nothing() % default
    assert result is default
