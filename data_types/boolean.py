"""
BOOLEAN (bool) - Python's simplest and most fundamental data type.

What is a boolean?
------------------
A boolean represents one of only two possible values: True or False.
It is the type of the answer to a yes/no question:

    Is the user logged in?        -> True
    Is the password correct?      -> False
    Does the list contain 42?     -> True

Booleans are named after George Boole, an English mathematician who
invented Boolean algebra in the 19th century.

How does it work?
-----------------
* There are exactly two boolean literals in Python: True and False
  (note the CAPITAL first letter -- `true` and `false` are NameErrors).
* Internally a bool is a subclass of int, and True behaves like 1 and
  False behaves like 0. This makes booleans usable anywhere a number
  is expected (handy, but also a common source of bugs).
* Comparisons (`==`, `<`, `in`, `is`, ...) do NOT return True/False
  directly -- they return a bool. So conditions are built by asking
  questions about values.
* Python treats several other values as "falsy" in a condition even
  though they are not literally False. See "Truthiness" below.

Run this file:  python3 boolean.py
"""


# ---------------------------------------------------------------------------
# 1. Creating booleans
# ---------------------------------------------------------------------------
# The only two ways to make a bool are to write the literals True/False
# or to produce them from a comparison or a boolean operator.

is_python_fun = True
is_pizza_healthy = False

# Comparisons produce booleans:
print("5 == 5              ->", 5 == 5)
print("5 == 6              ->", 5 == 6)
print("'cat' < 'dog'       ->", "cat" < "dog")   # string comparison
print("10 >= 10            ->", 10 >= 10)
print("3 in [1, 2, 3]      ->", 3 in [1, 2, 3])  # membership test
# Identity (`is`) asks "are these the SAME object?", not "do these have the
# same value?". Use it for None (and small ints/bools), never for text.
nothing = None
print("None is None        ->", nothing is None)  # the correct identity test


# ---------------------------------------------------------------------------
# 2. Checking the type
# ---------------------------------------------------------------------------
# type() tells you the exact class. Note that bool is NOT the same as
# int even though bool inherits from int -- type() says "bool".
print("\ntype(True)          ->", type(True))
print("type(1)             ->", type(1))        # int, not bool!
print("isinstance(True,int)->", isinstance(True, int))  # True: bool IS an int


# ---------------------------------------------------------------------------
# 3. Boolean operators: and / or / not
# ---------------------------------------------------------------------------
# These combine or negate booleans to build more complex conditions.
# They are the words you use to write rules in plain English.

# not -> negates. True becomes False.
print("\nnot True            ->", not True)
print("not (5 > 3)         ->", not (5 > 3))

# and -> True only if BOTH sides are True
print("True and True       ->", True and True)
print("True and False      ->", True and False)

# or -> True if AT LEAST ONE side is True
print("False or True       ->", False or True)
print("False or False      ->", False or False)

# A realistic example: a login check needs the right user AND right password.
username = "ada"
password = "hunter2"

can_log_in = (username == "ada") and (password == "hunter2")
print("can_log_in          ->", can_log_in)

# or lets you offer alternatives:
favourite_colour = input_colour = "blue"
use_dark_mode = favourite_colour == "black" or favourite_colour == "blue"
print("use_dark_mode       ->", use_dark_mode)


# ---------------------------------------------------------------------------
# 4. Short-circuit evaluation
# ---------------------------------------------------------------------------
# `and` and `or` do NOT always evaluate both sides. Python stops as soon
# as the answer is already known. This is a real performance win and the
# standard way to guard a risky operation.
#
# Rule of thumb:
#   A and B  -> if A is False, return False without touching B
#   A or B   -> if A is True,  return True  without touching B

def risky_operation():
    print("    !! risky_operation() actually ran!")
    return True

print("\nShort-circuit with and:")
result = False and risky_operation()   # risky_operation is never called
print("  result             ->", result)

print("Short-circuit with or:")
result = True or risky_operation()    # risky_operation is never called
print("  result             ->", result)

# Practical use: don't divide by zero unless the divisor is non-zero.
def safe_divide(a, b):
    # b != 0 is checked first, so the division never runs when b is 0
    return a / b if b != 0 else "undefined"

print("\nsafe_divide(10, 2)  ->", safe_divide(10, 2))
print("safe_divide(10, 0)  ->", safe_divide(10, 0))


# ---------------------------------------------------------------------------
# 5. TRUTHINESS -- the most important concept in this file
# ---------------------------------------------------------------------------
# In a condition, Python converts a value to a bool. Almost anything
# non-empty is True; empty things are False. This is called "truthiness".
#
#   FALSY values:                      TRUTHY values:
#   --------------------------------    ---------------------------------
#   False, None                         any non-empty string
#   0, 0.0, 0j (any zero number)       any non-zero number, even 0.1
#   "" (empty string)                   any non-empty list/tuple/dict/set
#   [] {} () set()  (empty containers)  any non-empty custom object
#   range(0)                            almost everything else
#
# This is why you can write `if items:` instead of `if len(items) > 0:`

print("\n--- truthiness checks ---")
print("bool(0)             ->", bool(0))
print("bool(0.0)           ->", bool(0.0))
print("bool('')            ->", bool(""))
print("bool('hello')       ->", bool("hello"))
print("bool([])            ->", bool([]))
print("bool([0])           ->", bool([0]))   # a list holding zero is non-empty!
print("bool(None)          ->", bool(None))

# Idiomatic emptiness checks -- prefer these over len() comparisons
shopping_cart = []
if shopping_cart:
    print("cart is not empty")
else:
    print("cart is empty (use: `if not cart:`)")

name = ""
if not name:
    print("name is empty (use: `if not name:`)")


# ---------------------------------------------------------------------------
# 6. The classic gotcha: `==` vs truthiness
# ---------------------------------------------------------------------------
# Because "" and 0 are falsy, `if value:` and `if value != 0:` are NOT
# always equivalent. It matters when 0.0 or "" is a legitimate input.

# This is a subtle behaviour of empty containers and booleans:
def describe(value):
    # Truthiness: 0 and False both read as "nothing here"
    if not value:
        return "falsy -> treated as empty"
    return f"truthy ({type(value).__name__})"

print("\ndescribe(0)         ->", describe(0))
print("describe(0.1)       ->", describe(0.1))
print("describe(False)     ->", describe(False))


# ---------------------------------------------------------------------------
# 7. `is` vs `==` for booleans
# ---------------------------------------------------------------------------
# For booleans (and None) `is` and `==` always agree, because there is
# only one True object and one False object in Python.
# Prefer `is None` / `is not None` -- never write `== None`.

value = None
if value is None:
    print("\nvalue is None       -> True (this is the correct way to check None)")


# ---------------------------------------------------------------------------
# 8. Common beginner mistakes
# ---------------------------------------------------------------------------
def common_mistakes():
    """Demonstrate the errors beginners hit most often with booleans."""
    print("--- common mistakes ---")

    # MISTAKE 1: lowercase true/false is a NameError in Python.
    # Correct:  value = True

    # MISTAKE 2: Any non-empty string is True, so `if name:` is True even
    # for the string "False". Be careful with user input.
    name = "False"
    if name:                        # True! Because the string is non-empty
        print(f"  1. if '{name}': -> True  (string is non-empty!)")
    # If you need the text meaning, parse it:
    if name.lower() == "false":
        print("     parsing the text properly -> treated as False")

    # MISTAKE 3: Chained comparisons. `0 < x < 10` is a feature, not a bug,
    # but `x > 0 and x < 10` is the same thing written longhand.
    x = 5
    if 0 < x < 10:
        print("  2. `0 < x < 10` is valid Python and evaluates in one go")

    # MISTAKE 4: Using `=` (assignment) instead of `==` (comparison).
    # if x = 5:  -> SyntaxError

    # MISTAKE 5: Bitwise & and | on booleans work but are almost always
    # a mistake -- they evaluate BOTH sides (no short-circuit).
    a, b = True, False
    print("  3. True & False  ->", a & b, "(bitwise: no short-circuit, avoid)")


# ---------------------------------------------------------------------------
# 9. Best practices -- a short summary
# ---------------------------------------------------------------------------
def best_practices():
    """
    Rules of thumb for writing readable boolean code:
      1. Compare against True/False directly; don't use numbers as flags.
         Use: `is_admin = True`, not `is_admin = 1`.
      2. Use `is None` / `is not None`, never `== None`.
      3. Prefer truthiness (`if items:`) over `if len(items) > 0:`.
      4. Use `not x` rather than `x == False`.
      5. Name booleans readably: `is_valid`, `has_access`, `should_retry`.
      6. Keep conditions short; if an `if` needs many `and`s, extract
         well-named boolean variables or a helper function.
      7. Remember that bool subclasses int, so `sum([True, True]) == 2`.
    """
    print("--- best practices (see docstring) ---")
    print("bool values count as numbers:", True + True)


# Run every demo when the file is executed directly.
def main():
    common_mistakes()
    best_practices()
    print("\nAll boolean examples finished.")


if __name__ == "__main__":
    main()
