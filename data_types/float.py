"""
FLOAT (float) - Python's decimal (floating-point) data type.

What is a float?
----------------
A float is a number written with a decimal point or in scientific notation,
such as 3.14, -0.5, 2.0, or 6.02e23. The name comes from "floating point",
the standard way computers approximate real numbers using binary.

How does it work?
-----------------
* Write a number with a `.` in it (3.14) or an exponent (1e-3), and Python
  makes it a float automatically.
* Floats are stored as 64-bit binary fractions (IEEE 754). A consequence is
  that most decimal fractions cannot be represented exactly, so tiny rounding
  errors appear. `0.1 + 0.2` is famously `0.30000000000000004`, not `0.3`.
* Float is what `/` division returns -- even for whole numbers (`6 / 2`
  is `3.0`).
* Floats are immutable and hashable, just like ints.
* `float('nan')` and `float('inf')` exist for special "not a number" and
  "infinity" cases.

Run this file:  python3 float.py
"""


# ---------------------------------------------------------------------------
# 1. Creating floats
# ---------------------------------------------------------------------------
pi = 3.14159
price = 19.99
temperature = -40.5
whole_but_float = 2.0          # the ".0" forces a float
large = 1.5e10                # scientific notation: 1.5 * 10**10
tiny = 1e-6

print("pi                   ->", pi)
print("whole_but_float      ->", whole_but_float, " type:", type(whole_but_float))
print("large (1.5e10)       ->", large)
print("tiny (1e-6)          ->", tiny)
print("type(3.14159)        ->", type(3.14159))
print("type(2.0)            ->", type(2.0))        # float
print("type(2)              ->", type(2))          # int -- no decimal point!
print("type(1_000)          ->", type(1_000))      # int (underscores don't change type)


# ---------------------------------------------------------------------------
# 2. The famous rounding problem (binary floating point)
# ---------------------------------------------------------------------------
# 0.1 cannot be stored exactly in binary, just like 1/3 cannot be stored
# exactly in decimal. Adding two approximations leaves a tiny error.
print("\n--- floating point imprecision ---")
print("0.1 + 0.2            ->", 0.1 + 0.2)
print("is it == 0.3?        ->", 0.1 + 0.2 == 0.3)   # False!
print("0.1 + 0.2 == 0.3 ?   ->", 0.1 + 0.2 == 0.3)   # not reliable

# Solution 1: round before comparing.
print("\nround(0.1 + 0.2, 10) ->", round(0.1 + 0.2, 10), " (== 0.3:",
      round(0.1 + 0.2, 10) == 0.3, ")")

# Solution 2: use math.isclose for float comparisons.
import math
print("math.isclose(a, b)   ->", math.isclose(0.1 + 0.2, 0.3))  # True

# Solution 3: for money, use the `decimal` module (exact base-10).
from decimal import Decimal
total = Decimal("0.1") + Decimal("0.2")
print("Decimal sum is exact ->", total, " (== 0.3:",
      total == Decimal("0.3"), ")")


# ---------------------------------------------------------------------------
# 3. Basic arithmetic
# ---------------------------------------------------------------------------
a, b = 10.0, 3.0

print("\n--- arithmetic (a=10.0, b=3.0) ---")
print("a + b    ->", a + b)     # 13.0
print("a - b    ->", a - b)     # 7.0
print("a * b    ->", a * b)     # 30.0
print("a / b    ->", a / b)     # 3.333... (always float division)
print("a // b   ->", a // b)    # 3.0  (float floor division)
print("a % b    ->", a % b)     # 1.0
print("a ** b   ->", a ** b)    # 1000.0
print("-a       ->", -a)        # -10.0

# Integer / float mixing: Python handles it, promoting to float.
print("\n10 / 5   ->", 10 / 5, type(10 / 5).__name__)   # 2.0 float
print("10 + 5.0 ->", 10 + 5.0)                          # 15.0 float
print("2 * 1.5  ->", 2 * 1.5)                           # 3.0  float


# ---------------------------------------------------------------------------
# 4. Rounding
# ---------------------------------------------------------------------------
# round() returns an int if you give it no digits, otherwise a float.
value = 3.14159

print("\n--- rounding ---")
print("round(3.14159)       ->", round(value))        # 3    (int!)
print("type(round(3.14159)) ->", type(round(value)).__name__)
print("round(3.14159, 2)    ->", round(value, 2))     # 3.14 (float)
print("round(3.14159, 4)    ->", round(value, 4))     # 3.1416
print("round(2.5)           ->", round(2.5))          # 2  (banker's rounding!)
print("round(3.5)           ->", round(3.5))          # 4  (round-half-to-even)

# Note the banker's rounding surprise: .5 rounds to the nearest EVEN number.
# This matters for things like round(0.5), round(1.5), round(2.5) -> 0, 2, 2.
# If you need "always round half up", use decimal or math.floor(x + 0.5).
print("round(0.5), round(1.5), round(2.5) ->",
      round(0.5), round(1.5), round(2.5))


# ---------------------------------------------------------------------------
# 5. Type conversion
# ---------------------------------------------------------------------------
print("\n--- conversions ---")
print("float('3.14')        ->", float("3.14"))     # str -> float
print("float(3)             ->", float(3))          # int -> float, easy
print("int(3.99)            ->", int(3.99))         # float -> int, TRUNCATES to 3
print("round(int) alternative: round(3.99) ->", round(3.99))   # 4

# Unlike int(), float() CAN parse decimal strings directly:
print("int('3.99') would ERROR, but float('3.99') ->", float("3.99"))

# bool converts to float too:
print("float(True)          ->", float(True))       # 1.0


# ---------------------------------------------------------------------------
# 6. Special values: infinity and NaN
# ---------------------------------------------------------------------------
infinity = float("inf")
not_a_number = float("nan")

print("\n--- special float values ---")
print("float('inf')         ->", infinity)
print("float('-inf')        ->", float("-inf"))
print("1e400 -> float('inf')->", float("1e400"))    # overflows to inf
print("float('nan')         ->", not_a_number)
print("inf + 1              ->", infinity + 1)      # still inf
print("nan == nan           ->", not_a_number == not_a_number)  # False!

# NaN is not equal to anything, even itself, so compare with math.isnan().
print("math.isnan(nan)      ->", math.isnan(not_a_number))       # True


# ---------------------------------------------------------------------------
# 7. Useful math operations
# ---------------------------------------------------------------------------
import math

print("\n--- math module ---")
print("math.sqrt(16)        ->", math.sqrt(16))     # 4.0
print("math.floor(3.7)      ->", math.floor(3.7))   # 3 (int, always down)
print("math.ceil(3.2)       ->", math.ceil(3.2))    # 4 (int, always up)
print("math.pi              ->", math.pi)
print("math.e               ->", math.e)
print("math.pow(2, 3)       ->", math.pow(2, 3))    # 8.0
print("math.fabs(-2.5)      ->", math.fabs(-2.5))   # 2.5 (float absolute value)

# floor and ceil are handy for converting to int after rounding in a
# particular direction:
print("int(math.floor(3.7)) ->", int(math.floor(3.7)))  # 3
print("int(math.ceil(3.2))  ->", int(math.ceil(3.2)))   # 4


# ---------------------------------------------------------------------------
# 8. Precision and formatting
# ---------------------------------------------------------------------------
# Use f-strings to control how many decimals are displayed. Note this only
# changes how it PRINTS; the stored value is unchanged.
amount = 1234.5678

print("\n--- formatting ---")
print(f"{amount:.2f}            -> 2 decimal places")
print(f"{amount:.0f}            -> 0 decimal places (rounded for display)")
print(f"{amount:,.2f}          -> with thousands separator")
print(f"{amount:.3e}            -> scientific notation")

# Common use: always show money with two decimals.
cost = 9.5
print(f"Total: ${cost:.2f}")   # Total: $9.50


# ---------------------------------------------------------------------------
# 9. Common beginner mistakes
# ---------------------------------------------------------------------------
def common_mistakes():
    """The float errors beginners hit most often."""
    print("--- common mistakes ---")

    # MISTAKE 1: comparing floats with == after arithmetic.
    # Because of rounding error this is often False when it "should" be True.
    print("  1. (0.1 + 0.2) == 0.3 ->", (0.1 + 0.2) == 0.3, " (unreliable!)")
    print("     Use math.isclose() instead ->", math.isclose(0.1 + 0.2, 0.3))

    # MISTAKE 2: forgetting that / returns float.
    avg = 10 / 3
    print("  2. 10 / 3 =", avg, " (float). Use 10 // 3 for", 10 // 3,
          "if you want an int floor.")

    # MISTAKE 3: using floats for money. 0.1 + 0.2 != 0.3 breaks accounting.
    print("  3. For money, use Decimal('0.1') or store whole cents as int")

    # MISTAKE 4: int() truncates toward zero, it does not round.
    print("  4. int(2.9) ->", int(2.9), "(truncates). round(2.9) ->", round(2.9))

    # MISTAKE 5: thinking 2.0 and 2 are equal types.
    print("  5. 2 == 2.0 is True, but type differs:",
          type(2).__name__, "vs", type(2.0).__name__)

    # MISTAKE 6: NaN comparisons always fail, so `==` never catches it.
    n = float("nan")
    print("  6. nan == nan is", n == n, "-- use math.isnan(n) instead")


# ---------------------------------------------------------------------------
# 10. Best practices -- a short summary
# ---------------------------------------------------------------------------
def best_practices():
    """
    Guidelines for working with floats:
      1. Never compare floats for exact equality after arithmetic; use
         math.isclose(a, b) or round() to a sensible precision.
      2. Use the `decimal.Decimal` type for money and financial work --
         floats cannot represent values like 0.1 exactly.
      3. Use `math.floor` / `math.ceil` when you need explicit rounding
         direction; remember `round()` uses banker's rounding.
      4. Use f-string formatting (`{x:.2f}`) to control display precision.
      5. Remember `/` always returns a float; use `//` for integer results.
      6. Be careful with `inf` and `nan` -- they propagate through
         arithmetic in surprising ways.
      7. Convert with `float(x)`; `int(x)` truncates rather than rounds.
    """
    print("--- best practices (see docstring) ---")
    print("safe comparison:", math.isclose(0.1 + 0.2, 0.3))


# Run every demo when the file is executed directly.
def main():
    common_mistakes()
    best_practices()
    print("\nAll float examples finished.")


if __name__ == "__main__":
    main()
