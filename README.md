# weakget - Chaining `getattr` and `.get`

With `weakget`, you can write code like:

```python
x = weakget(obj)[5]['key'].attr.method() % 'default'
```

and `x` will be set to `'default'` if:

- `obj` has just 3 items, or
- `obj[5]` is missing `'key'`, or
- `obj[5]['key']` doesn't have `attr`, or
- `obj[5]['key'].attr` didn't define `method()`

Otherwise, `x` gets set to `obj[5]['key'].attr.method()`. Similar code in pure Python would look like:

```python
try:
  x = obj[5]['key'].attr.method()
except (LookupError, AttributeError):
  x = 'default'
```

`weakget` is better because:

- it doesn't hide `AttributeError` raised from `obj[5]` or `obj[5]['key']`
- it doesn't hide `LookupError` raised from `obj[5]['key'].attr` or `obj[5]['key'].attr.method`
- it doesn't hide **any** exception raised from calling `obj[5]['key'].attr.method()`
- it fits on one line!

## Usage

Install from [PyPI](https://pypi.python.org/pypi) using `pip`:

`pip install weakget`

Then import into your scripts:

```python
>>> from weakget import weakget
>>> obj = []
>>> weakget(obj)[5]['key'].attr.method() % 'default'
'default'
```

## pep505 - None-aware operations à la PEP 505

But wait, there's more! [PEP 505](https://www.python.org/dev/peps/pep-0505) describes adding `None`-aware operators to Python, but you can get that behaviour today from `pep505`:

```python
from weakget import pep505
x = pep505(a.attr, b.attr) % 3    # i.e. a.attr ?? b.attr ?? 3
y = pep505(c)['key'].attr % None  # i.e. c?.['key']?.attr
```

Behind-the-scenes, `pep505` works in much the same way as `weakget`, but where `weakget` looks for `LookupError` or `AttributeError` to be raised, `pep505` only looks for `None`. Similar code in pure Python would look like:

```python
x = a.attr if a.attr is not None else b.attr if b.attr is not None else 3
y = c['key'].attr if (c is not None and c['key'] is not None) else None
```

`pep505` is better because:

- `a.attr`, `b.attr`, and `c['key']` are each evaluated at most **once**
- less typing, which also means...
- less chance for logic errors

## FAQs

**Q:** Why not use `getattr`'s default instead of catching, and possibly hiding, `AttributeError`s?

**A:** Turns out `getattr` also catches `AttributeError`:

```python
>>> class A:
...   @property
...   def b(self):
...     return None.badattr
>>> getattr(A(), 'b')
AttributeError: 'NoneType' object has no attribute 'badattr'
>>> getattr(A(), 'b', 'default')
'default'
```

**Q:** Why not use `.get`'s default argument instead of catching `LookupError`?

**A:** `.get` is implemented on mapping objects like `dict`, but is not available on sequence objects like `list`. Catching the `LookupError` from `obj[key]` is the only way to support both.

**Q:** Why `%` instead of `or`, `|`, or a method?

**A:** `or` isn't an option as it [cannot be directly overloaded](https://www.python.org/dev/peps/pep-0335/#rejection-notice). `|` is enticing as `a | b` reads like "`a` or `b`", but "or" in Python usually refers to truthiness, which [does not distinguish "lack of value" from "false"](https://peps.python.org/pep-0505/#specialness-of-none). Adding a method would hide any method of the same name in the underlying object. `%` is [already overloaded in Python](https://docs.python.org/3/library/stdtypes.html#old-string-formatting), making it the best option among the remaining operators.

**Q:** Can't you come up with a better name than `pep505`?

**A:** Well, `PP` is currently in the lead as it looks like [`??`](https://peps.python.org/pep-0505/#the-coalesce-rule), but I'm open to suggestions!
