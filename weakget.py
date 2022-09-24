"""weakget - Chain multiple `getattr` and `.get` calls into one expression
"""

__version__ = "1.0"


class weakget:
    """weakget allows chaining multiple attribute and item lookups into a single expression,
    returning a default value if any one of the lookups fail.

        weakget(obj).attr[5].meth()['key'] % default
    """

    __slots__ = "_weakget__obj"

    def __new__(cls, obj):
        if isinstance(obj, _weakget__types):
            raise TypeError("weakget() argument must not be a fellow weakget object")

        self = super().__new__(cls)
        self._weakget__obj = obj
        return self

    def __getattr__(self, name):
        try:
            obj = getattr(self._weakget__obj, name)
        except AttributeError:
            return _weakget__nothing
        return weakget(obj)

    def __getitem__(self, key):
        try:
            obj = self._weakget__obj[key]
        except LookupError:
            return _weakget__nothing
        return weakget(obj)

    def __call__(self, *args, **kwargs):
        return weakget(self._weakget__obj(*args, **kwargs))

    def __mod__(self, default):
        return self._weakget__obj

    # Unsupported operations (this disables the Python-provided default implementations)
    __bool__ = None
    __eq__ = None
    __ne__ = None
    __hash__ = None


class pep505:
    """pep505 performs None-aware lookups similar to those described in PEP 505. It allows chaining
    multiple attribute and item lookups into a single expression, returning a default value if any
    one of the lookups return None.

        pep505(obj).attr[5].meth()['key'] % default

    Additionally, pep505 can be called with multiple arguments, returning the first non-None
    argument, or the default if all are None.

        pep505(obj1, obj2, obj3) % default
    """

    __slots__ = "_pep505__obj"

    def __new__(cls, *objs):
        if not objs:
            raise TypeError("pep505() expected >0 arguments")

        # Choose the first non-None argument (à la ??), then wrap it in a pep505 object (à la ?.)
        for obj in objs:
            if obj is not None:
                return pep505._new1(obj)
        return _weakget__nothing

    @classmethod
    def _new1(cls, obj):
        if obj is None:
            return _weakget__nothing

        if isinstance(obj, _weakget__types):
            raise TypeError("pep505() argument must not be a fellow weakget object")

        self = super().__new__(cls)
        self._pep505__obj = obj
        return self

    def __getattr__(self, name):
        return pep505._new1(getattr(self._pep505__obj, name))

    def __getitem__(self, key):
        return pep505._new1(self._pep505__obj[key])

    def __call__(self, *args, **kwargs):
        return pep505._new1(self._pep505__obj(*args, **kwargs))

    def __mod__(self, default):
        return self._pep505__obj

    # Unsupported operations
    __bool__ = None
    __eq__ = None
    __ne__ = None
    __hash__ = None


class _weakget__NothingType:
    """Sentinel singleton signifying unsuccessful salvage of state.

    ...or in other words...

    The object returned when weakget or pep505 fails to retrieve a value.
    """

    __slots__ = ()

    def __getattr__(self, name):
        return self

    def __getitem__(self, key):
        return self

    def __call__(self, *args, **kwargs):
        return self

    def __mod__(self, default):
        return default

    # Unsupported operations
    __bool__ = None
    __eq__ = None
    __ne__ = None
    __hash__ = None


_weakget__nothing = _weakget__NothingType()


_weakget__types = (weakget, pep505, _weakget__NothingType)


# TODO We _could_ support `__bool__`, returning `True` iff we haven't failed a get and
# `_weakget__obj` evaluates to `True`. This could be used like `if weakget(x).foo`. However, this
# would enable the `or` operator (`weakget(x).foo or 50`), which might confuse people who might
# expect `or` to work like `%`. Remember: one of the goals of this library is to avoid the
# confusion described here: https://peps.python.org/pep-0505/#specialness-of-none.

# TODO Similarly, we _could_ support `__eq__` and `__ne__`, allowing for `if weakget(x).foo == 33`.
# It's pretty clear that `==` would return `False` on a failed get, but what about `!=`?  If
# `__ne__` also returns `False`, then the objects would be neither equal nor not-equal, which is
# very surprising. If `__ne__` instead returns `True`, then `if weakget(x).foo != 33` would be
# true even though `x.foo` doesn't exist. How can something that doesn't exist not equal `33`?

# TODO Need a better name for `pep505`. Current favourite is `PP`, because it looks like the
# proposed `??` operator (also used in C#).
