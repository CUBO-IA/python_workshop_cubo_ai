"""
NONE (NoneType) - Python's way of saying "there is no value here".

What is None?
-------------
`None` is the single value of the `NoneType` class. It represents the ABSENCE
of a value: no result, nothing found, not applicable, or "unset". It is the
closest Python has to "nothing".

    result = None          # nothing yet
    print(result)          # -> None

Think of the difference between an empty box and no box at all. An empty list
`[]` is a real list containing zero items. `None` means there is no list here
at all.

How does it work?
-----------------
* `None` is a SINGLETON: there is exactly one None object in Python. Every
  reference to None points at that same object.
* Its type is `NoneType`, and `None` is that type's only instance.
* It is FALSY, so `if not value:` treats it as empty -- but it is NOT equal
  to False or 0. `None == False` is False!
* You compare it with `is None`, never with `== None`.
* It is hashable, so it can go in sets and be a dict key.
* Many things return it automatically: a function with no `return`, a failed
  `.get()` lookup, a regex `.search()` with no match.
* Almost nothing can be done TO it -- no arithmetic, no len(), no indexing.

Run this file:  python3 none.py
"""


# ---------------------------------------------------------------------------
# 1. Creating and inspecting None
# ---------------------------------------------------------------------------
# There is no way to create a *new* None. You either use the keyword None or
# let Python produce one for you.
value = None

print("value                ->", value)
print("type(value)          ->", type(value))          # <class 'NoneType'>
print("repr(value)          ->", repr(value))          # None
print("str(value)           ->", str(value))           # None
print("value is None        ->", value is None)        # True
print("isinstance(v,NoneType)->", isinstance(value, type(None)))  # True

# NoneType is a real, callable class -- and calling it just gives back None.
# This is a curiosity rather than something to use, but it proves None is a
# singleton: there is no way to have a second one.
print("type(None)()         ->", type(None)())         # None
print("type(None)() is None ->", type(None)() is None)  # True


# ---------------------------------------------------------------------------
# 2. The None / False / 0 distinction (a critical gotcha)
# ---------------------------------------------------------------------------
# None is FALSY, meaning it behaves like False in a condition. But it is NOT
# EQUAL to False or 0. This distinction catches people out constantly.
print("\n--- falsy but not equal ---")
print("bool(None)           ->", bool(None))        # False (falsy)
print("None == False        ->", None == False)     # False !
print("None == 0            ->", None == 0)         # False !
print("None is False        ->", None is False)     # False
print("None is None         ->", None is None)      # True

# So in a condition they behave the same, but in a comparison they differ.
# NEVER write `if x == None:` -- it is wrong style and can be subtly incorrect.


# ---------------------------------------------------------------------------
# 3. Checking for None -- always use `is None`
# ---------------------------------------------------------------------------
# `is` compares IDENTITY: "is this the very same None object?"
# Because None is a singleton, `is None` is always correct and always fast.
def describe(value):
    if value is None:
        return "value is None (nothing here)"
    return f"value is {value!r}"

print("\n--- identity checks ---")
print("describe(None)       ->", describe(None))
print("describe(0)          ->", describe(0))
print("describe('')         ->", describe(""))
print("describe(False)      ->", describe(False))

# PEP 8 rule: use `is None` / `is not None`, never `== None` / `!= None`.


# ---------------------------------------------------------------------------
# 4. Where None comes from
# ---------------------------------------------------------------------------
# You rarely type None yourself. Python hands it back to you in several
# common situations.

# (a) A function that has no `return` statement returns None implicitly.
def greet_no_return():
    print("    (this function says hello)")

result = greet_no_return()
print("\n--- where None comes from ---")
print("func with no return  ->", result, "(returned None implicitly)")

# (b) `return` with no value also gives None.
def bare_return():
    return

print("bare 'return'        ->", bare_return())

# (c) A dict `.get()` on a missing key returns None.
user = {"name": "Ada"}
print("dict.get('email')    ->", user.get("email"))    # None

# (d) A regex `.search()` with no match returns None.
import re
match = re.search("z+", "abc")
print("re.search no match   ->", match)                 # None

# (e) `input()` returns a string, but some library calls return None on failure.


# ---------------------------------------------------------------------------
# 5. None in containers and defaults
# ---------------------------------------------------------------------------
# None can be stored in lists, tuples, sets, and dicts like any other value.
mixed = [1, None, 3]
print("\n--- None in containers ---")
print("list with None       ->", mixed)
print("2 in mixed           ->", 2 in mixed)     # False
print("None in mixed        ->", None in mixed)  # True

# A very common pattern is using None as a "not set yet" placeholder, then
# checking before use.
best_score = None          # not set yet
if best_score is None:
    print("best_score unset     -> initialising to 0")
    best_score = 0
best_score += 10
print("best_score now       ->", best_score)

# None is hashable, so it works as a dict value and (surprisingly) even a key.
print("None as dict key     ->", {None: "means nothing"})  # valid!


# ---------------------------------------------------------------------------
# 6. None as a default argument (the safe pattern)
# ---------------------------------------------------------------------------
# A classic Python bug: a mutable default argument is shared across calls,
# because the default is created ONCE when the function is defined.
def add_item_wrong(item, bucket=[]):     # BUG: default created once
    bucket.append(item)
    return bucket

print("\n--- mutable default anti-pattern ---")
print("first call           ->", add_item_wrong("a"))
print("second call          ->", add_item_wrong("b"), "<- 'a' leaked in!")

# The fix: default to None (immutable), then create the list inside.
def add_item_right(item, bucket=None):
    if bucket is None:      # create a fresh list each call
        bucket = []
    bucket.append(item)
    return bucket

print("\n--- correct pattern ---")
print("first call           ->", add_item_right("a"))
print("second call          ->", add_item_right("b"))   # no leak

# This "if x is None: build a default" pattern is idiomatic Python and shows
# up everywhere in the standard library.


# ---------------------------------------------------------------------------
# 7. Type hints: saying "this might be None"
# ---------------------------------------------------------------------------
# Modern Python uses `|` to say a value may be a type OR None. This is how
# you document a function that can return "nothing".
from typing import Optional

def find_user(user_id: int) -> dict | None:
    """Return the user dict, or None if not found."""
    users = {1: {"name": "Ada"}}
    return users.get(user_id)   # .get() gives None if the key is missing

print("\n--- type hints ---")
print("find_user(1)         ->", find_user(1))
print("find_user(99)        ->", find_user(99))     # None

# `dict | None` is shorthand for `Optional[dict]`. Both mean "a dict or None".
# These hints are NOT enforced at runtime -- they help humans and type checkers.


# ---------------------------------------------------------------------------
# 8. What you CANNOT do with None
# ---------------------------------------------------------------------------
# None is deliberately inert. Almost every operation raises TypeError.
print("\n--- operations that fail on None ---")
try:
    None + 1
except TypeError as e:
    print("None + 1             -> TypeError:", e)

try:
    len(None)
except TypeError as e:
    print("len(None)            -> TypeError:", e)

try:
    None.upper()
except AttributeError as e:
    print("None.upper()         -> AttributeError:", e)

# You cannot index it or iterate it either. None is a signal, not a container.


# ---------------------------------------------------------------------------
# 9. Practical example: optional search results
# ---------------------------------------------------------------------------
def first_even(numbers):
    """Return the first even number, or None if there isn't one."""
    for n in numbers:
        if n % 2 == 0:
            return n
    return None          # explicit: we reached the end and found nothing

def describe_search(numbers):
    found = first_even(numbers)
    if found is None:
        return "no even number found"
    return f"first even number is {found}"

print("\n--- practical: search returning None ---")
print(describe_search([1, 3, 5]))     # no even number
print(describe_search([1, 4, 6]))     # first even number is 4


# ---------------------------------------------------------------------------
# 10. Common beginner mistakes
# ---------------------------------------------------------------------------
def common_mistakes():
    """The None errors beginners hit most often."""
    print("--- common mistakes ---")

    # MISTAKE 1: writing `== None` instead of `is None`. It happens to work
    # for None itself, but it is not the correct identity test and breaks the
    # moment a class overrides __eq__.
    # WRONG:  if x == None:
    # RIGHT:  if x is None:
    x = None
    print("  1. use `is None`, not `== None` ->", x is None)

    # MISTAKE 2: treating None like an empty value and calling methods on it.
    # result = maybe_list.append(1)  -> AttributeError if maybe_list is None
    maybe_list = None
    safe = (maybe_list or [])     # None and [] both become []
    print("  2. `x or []` guards against None ->", safe)

    # MISTAKE 3: confusing "None" (falsy) with "False" (also falsy but a
    # real value). This distinction matters in functions that return
    # True/False/None to signal three different outcomes.
    def check(value):
        if value is None:
            return "not provided"
        if value is False:
            return "explicitly False"
        return "provided"
    print("  3. three states differ ->",
          [check(None), check(False), check(1)])

    # MISTAKE 4: using a mutable default argument (shown in section 6).
    # Always default to None and build inside the function.

    # MISTAKE 5: assuming a function returned a value when it may return None.
    # def f(): pass ; f().some_method() -> AttributeError
    # Always check `if result is not None:` before using the result.


# ---------------------------------------------------------------------------
# 11. Best practices -- a short summary
# ---------------------------------------------------------------------------
def best_practices():
    """
    Guidelines for working with None:
      1. Test with `is None` / `is not None`, never `== None`.
      2. Remember None is falsy but not equal to False or 0 -- know which
         behaviour you actually need.
      3. Use None as the default for optional parameters, then create the real
         value inside the function. Never use a mutable default like [] or {}.
      4. Annotate return types that may be None as `T | None` (or
         `Optional[T]`) so callers know to check.
      5. Distinguish "not provided" (None) from "provided but empty/False"
         when a function can return three states.
      6. Never call methods on a value until you have confirmed it is not None.
      7. Use `x or default` for a quick fallback when None and empty values can
         share a default.
    """
    print("--- best practices (see docstring) ---")
    print("None is falsy:", not None)


# Run every demo when the file is executed directly.
def main():
    common_mistakes()
    best_practices()
    print("\nAll None examples finished.")


if __name__ == "__main__":
    main()
