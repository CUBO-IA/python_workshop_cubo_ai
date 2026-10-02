"""
INTEGER (int) - Python's whole-number data type.

What is an integer?
-------------------
An integer is a whole number with no decimal point: ..., -2, -1, 0, 1, 2, ...
Python calls the type `int`. Integers are exact -- 3 is exactly 3, no matter
how big it gets. This is a key difference from most other languages (C, Java,
JavaScript), where whole numbers have a fixed maximum size and can "wrap
around" on overflow. In Python, ints are arbitrary precision:

    print(2 ** 100)   # a 31-digit number, computed exactly

How does it work?
-----------------
* Write a plain number with no decimal point and no quotes: `x = 42`.
* Arithmetic works as you'd expect: + - * / // % ** and unary minus.
* Division `/` always returns a float; `//` (floor division) returns an int.
* Integers are immutable -- once created, they can never be changed.
* They are hashable, so they can be used as dict keys and set members.
* Python ints have no overflow, so there is no need for long/int distinction.

Run this file:  python3 integer.py
"""


# ---------------------------------------------------------------------------
# 1. Creating integers
# ---------------------------------------------------------------------------
a = 42
b = -7
zero = 0

# Underscores are allowed for readability in large numbers (Python 3.6+):
population = 8_000_000_000
print("population           ->", population)
print("type(population)     ->", type(population))  # still an int

# Python 3 also supports literal bases other than 10:
print("0b1010 (binary)      ->", 0b1010)   # 10
print("0o17   (octal)       ->", 0o17)     # 15
print("0xFF   (hex)          ->", 0xFF)     # 255
print("1_000_000 == 1000000 ->", 1_000_000 == 1000000)


# ---------------------------------------------------------------------------
# 2. Checking the type
# ---------------------------------------------------------------------------
print("\ntype(42)            ->", type(42))          # <class 'int'>
print("isinstance(42, int)  ->", isinstance(42, int))
print("isinstance(True,int) ->", isinstance(True, int))  # bool is an int too
print("isinstance(4.0, int) ->", isinstance(4.0, int))  # False: that's a float


# ---------------------------------------------------------------------------
# 3. Basic arithmetic operators
# ---------------------------------------------------------------------------
x, y = 17, 5

print("\n--- arithmetic (x=17, y=5) ---")
print("x + y   (addition)   ->", x + y)    # 22
print("x - y   (subtraction)->", x - y)    # 12
print("x * y   (multiplication)->", x * y) # 85
print("x / y   (true division)->", x / y)   # 3.4  <- returns a FLOAT
print("x // y  (floor division)->", x // y) # 3    <- returns an INT
print("x % y   (modulo/remainder)->", x % y)  # 2
print("x ** y  (exponent)   ->", x ** y)   # 1419857
print("-x      (negation)   ->", -x)        # -17

# divmod() gives quotient and remainder in one call:
quotient, remainder = divmod(x, y)
print("divmod(17, 5)       ->", (quotient, remainder))  # (3, 2)


# ---------------------------------------------------------------------------
# 4. `/` vs `//` vs `%` -- the classic confusion
# ---------------------------------------------------------------------------
# `/`  true division: always float, keeps the fractional part.
# `//` floor division: int result, drops the fractional part (rounds DOWN).
# `%`  modulo: the remainder after floor division.

print("\n--- division detail ---")
print("7 / 2   ->", 7 / 2)    # 3.5  (float)
print("7 // 2  ->", 7 // 2)   # 3    (int)
print("7 % 2   ->", 7 % 2)    # 1
print("7.0 / 2 ->", 7.0 / 2)  # 3.5  (float // float is float too)
print("7.0 // 2->", 7.0 // 2) # 3.0  (float result, even with //)

# Floor division rounds toward negative infinity, which surprises people:
print("\n-7 // 2  ->", -7 // 2)   # -4, NOT -3 (rounds down)
print("-7 % 2   ->", -7 % 2)    # 1  (result always has y's sign)

# Very common use: checking if a number is even, without modulo on floats:
n = 42
if n % 2 == 0:
    print(f"\n{n} is even")


# ---------------------------------------------------------------------------
# 5. Arbitrary precision (no overflow)
# ---------------------------------------------------------------------------
# Unlike most languages, Python integers grow to fit any value, so overflow
# errors essentially do not exist for ints.
huge = 2 ** 100
print("\n2 ** 100             ->", huge)
print("digits in 2**100     ->", len(str(huge)))
print("big + big is exact   ->", (2 ** 100) + (2 ** 100) == 2 ** 101)  # True

# The only "limit" is memory: asking for 2 ** 10_000_000 will hang or crash.
# Don't do that.


# ---------------------------------------------------------------------------
# 6. Immutability
# ---------------------------------------------------------------------------
# Integers are immutable: you can't change one in place. Every "change"
# actually creates a brand-new int object. This is why ints are safe to use
# as dictionary keys and set elements.

n = 10
n += 5        # this creates a NEW int object, then rebinds the name
print("\nn after n += 5      ->", n)     # 15

# Because of this, integers are hashable and can be dict keys:
ages = {20: "twenty", 30: "thirty"}
print("ages[30]            ->", ages[30])


# ---------------------------------------------------------------------------
# 7. Type conversion
# ---------------------------------------------------------------------------
# You often need to move between int, float and string. Use the built-in
# conversion functions -- never rely on implicit conversions.

print("\n--- conversions ---")
print("int('42')            ->", int("42"))        # str -> int
print("int(3.99)            ->", int(3.99))        # float -> int, TRUNCATES
# int() CANNOT parse a string containing a decimal point -- it raises:
try:
    int("3.99")
except ValueError as e:
    print("int('3.99')          -> ERROR:", e)
# The safe way to parse a float string into an int:
print("int(float('3.99'))   ->", int(float("3.99")))  # 3
print("float(42)            ->", float(42))        # int -> float
print("str(42)              ->", str(42))          # int -> str
print("round(3.7)           ->", round(3.7))       # 4 (returns int here)

# Beware: bool converts to int too (True -> 1)
print("int(True)            ->", int(True))


# ---------------------------------------------------------------------------
# 8. Bitwise operators
# ---------------------------------------------------------------------------
# Integers are stored as bits, so you can manipulate them at the bit level.
# Useful for low-level programming, masks, and flags.

p, q = 12, 10     # 12 = 1100, 10 = 1010 in binary

print("\n--- bitwise (p=12=1100, q=10=1010) ---")
print("p & q   (AND)        ->", p & q)    # 1000 -> 8
print("p | q   (OR)         ->", p | q)    # 1110 -> 14
print("p ^ q   (XOR)        ->", p ^ q)    # 0110 -> 6
print("~p      (NOT)        ->", ~p)       # -(p+1) -> -13
print("p << 1  (left shift) ->", p << 1)   # 11000 -> 24 (multiply by 2)
print("p >> 1  (right shift)->", p >> 1)   # 110  -> 6  (divide by 2)


# ---------------------------------------------------------------------------
# 9. Useful built-in functions
# ---------------------------------------------------------------------------
print("\n--- built-ins ---")
print("abs(-9)              ->", abs(-9))
print("min(3, 1, 2)         ->", min(3, 1, 2))
print("max(3, 1, 2)         ->", max(3, 1, 2))
print("sum([1, 2, 3])       ->", sum([1, 2, 3]))
print("pow(2, 10)           ->", pow(2, 10))       # same as 2 ** 10
print("round(3.14159, 2)    ->", round(3.14159, 2)) # round to 2 decimals
print("divmod(17, 5)        ->", divmod(17, 5))


# ---------------------------------------------------------------------------
# 10. Common beginner mistakes
# ---------------------------------------------------------------------------
def common_mistakes():
    """The integer errors beginners hit most often."""
    print("--- common mistakes ---")

    # MISTAKE 1: `/` is true division and gives a float, even when the result
    # is whole. Use `//` if you specifically want an integer result.
    print("  1. 10 / 5 gives ->", 10 / 5, "  (a float, not an int!)")
    print("     10 // 5 gives ->", 10 // 5, " (an int)")

    # MISTAKE 2: int() truncates toward zero, it does not round.
    print("  2. int(2.9) ->", int(2.9), " (truncates; use round(2.9) ->",
          round(2.9), "to round instead)")

    # MISTAKE 3: dividing by zero raises ZeroDivisionError (crashes).
    # d = 0
    # d / 0   -> ZeroDivisionError: division by zero
    print("  3. dividing by zero raises ZeroDivisionError -- always guard it")

    # MISTAKE 4: leading zeros are not allowed.
    # n = 0755  -> SyntaxError (this was allowed in Python 2; use 0o755)
    print("  4. use 0o755 for an octal literal, not 0755")

    # MISTAKE 5: floats in disguise. If a value ever holds a decimal,
    # it is a float, not an int.
    price = 10.0     # note the .0
    print("  5. type(10.0) ->", type(price), " (a float, even though it looks whole)")


# ---------------------------------------------------------------------------
# 11. Best practices -- a short summary
# ---------------------------------------------------------------------------
def best_practices():
    """
    Guidelines for working with integers:
      1. Use `_` separators for big numbers: 1_000_000 (not 1000000).
      2. Prefer `//` or `%` when you mean "whole number" or "remainder";
         remember `/` always returns a float.
      3. Use `divmod(a, b)` when you need both quotient and remainder.
      4. Use `round(x)` to round, not `int(x)` which truncates.
      5. Convert strings explicitly with `int(s)`; never mix types
         implicitly.
      6. Remember ints are immutable and unlimited in size -- no overflow
         guard needed.
      7. Use `isinstance(n, int)` to check the type when you must.
    """
    print("--- best practices (see docstring) ---")
    print("even/odd without modulo:", 42 // 2 * 2 == 42)


# Run every demo when the file is executed directly.
def main():
    common_mistakes()
    best_practices()
    print("\nAll integer examples finished.")


if __name__ == "__main__":
    main()
