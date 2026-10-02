"""
COMPLEX (complex) - Python's built-in complex-number type.

What is a complex number?
-------------------------
A complex number has a real part and an imaginary part, written as `a + bj`,
where `j` is the imaginary unit and `j*j == -1`:

    z = 3 + 4j        # 3 real, 4 imaginary
    print(z)          # (3+4j)

Python supports complex numbers out of the box (no imports needed) and can mix
them freely with ints and floats. They are essential in signal processing,
Fourier analysis, electrical engineering, and quantum mechanics.

How does it work?
-----------------
* A literal imaginary part uses a trailing `j`: `2j`, `1.5j`. You must write
  `1j`, not `j` (a bare `j` is just an undefined variable name!).
* Imaginary coefficients are FLOATS: `z.real` and `z.imag` always return
  floats, even for `3+4j` -> 3.0 and 4.0.
* Arithmetic: +, -, *, /, ** all work, following the usual complex math.
* abs(z) gives the MAGNITUDE (the distance from the origin), always a float.
* Complex numbers are NOT ordered: `<`, `>`, sorted(), max() all raise
  TypeError, because "greater than" is meaningless for complex values.
* They are hashable and support ==, so they work in sets and as dict keys.
* The `cmath` module provides complex-aware versions of math functions.

Run this file:  python3 complex.py
"""


# ---------------------------------------------------------------------------
# 1. Creating complex numbers
# ---------------------------------------------------------------------------
# A literal uses a trailing `j` for the imaginary part.
a = 3 + 4j             # the classic 3-4-5 triangle
b = 2j                 # real part 0
c = 1.5j               # a float imaginary part
d = complex(7, 8)      # constructor form (real, imag)
e = complex(5)         # real number as complex -> 5+0j
f = complex(0)         # the complex zero -> 0j

print("3 + 4j               ->", a)
print("2j                   ->", b)
print("1.5j                 ->", c)
print("complex(7, 8)        ->", d)
print("complex(5)           ->", e)
print("complex(0)           ->", f)
print("type(3 + 4j)         ->", type(3 + 4j))       # <class 'complex'>

# THE MOST COMMON MISTAKE: a bare `j` is NOT the imaginary unit.
try:
    j
except NameError as e:
    print("bare j               -> NameError:", e)
print("you must write 1j    ->", 1j)   # not `j`


# ---------------------------------------------------------------------------
# 2. Real and imaginary parts
# ---------------------------------------------------------------------------
# .real and .imag are ALWAYS floats, even when the numbers look like ints.
z = 3 + 4j
print("\n--- parts (z = 3+4j) ---")
print("z.real               ->", z.real)        # 3.0 (float!)
print("z.imag               ->", z.imag)        # 4.0 (float!)
print("type(z.real)         ->", type(z.real).__name__)  # float

# conjugate() flips the sign of the imaginary part.
print("z.conjugate()        ->", z.conjugate()) # 3-4j
print("(3+4j).conjugate()   ->", (3 + 4j).conjugate())


# ---------------------------------------------------------------------------
# 3. Magnitude and argument
# ---------------------------------------------------------------------------
# abs() returns the magnitude: sqrt(real^2 + imag^2). It is always a float.
import cmath

z = 3 + 4j
print("\n--- magnitude ---")
print("abs(3+4j)            ->", abs(z))       # 5.0 (the hypotenuse!)
print("type(abs(3+4j))      ->", type(abs(z)).__name__)  # float

# The argument (angle from the positive real axis) comes from cmath.
print("cmath.polar(3+4j)    ->", cmath.polar(z))  # (5.0, 0.927...)
print("cmath.phase(3+4j)    ->", cmath.phase(z))  # 0.927... radians

# cmath.rect() goes the other way: magnitude + angle -> complex number.
print("cmath.rect(5, 0.927) ->", cmath.rect(5, 0.9272952180016122))


# ---------------------------------------------------------------------------
# 4. Arithmetic
# ---------------------------------------------------------------------------
x, y = 1 + 2j, 3 + 4j

print("\n--- arithmetic (x=1+2j, y=3+4j) ---")
print("x + y   (add)        ->", x + y)     # 4+6j
print("x - y   (subtract)   ->", x - y)     # -2-2j
print("x * y   (multiply)   ->", x * y)     # -5+10j
print("y / x   (divide)     ->", y / x)     # (11-2j)/5
print("x ** 2  (power)      ->", x ** 2)    # (-3+4j)
print("-x      (negate)     ->", -x)        # -1-2j

# Mixing complex with int or float just works; the result is complex.
print("\n(1+2j) + 5           ->", (1 + 2j) + 5)     # 6+2j
print("2 * (1+2j)           ->", 2 * (1 + 2j))     # 2+4j
print("1 + 1j               ->", 1 + 1j)           # int promoted to complex

# j*j == -1, the defining property of the imaginary unit:
print("\nj * j                ->", 1j * 1j)   # -1+0j
print("(3+4j)*(3-4j)        ->", (3 + 4j) * (3 - 4j))  # 25+0j (magnitude^2)


# ---------------------------------------------------------------------------
# 5. Equality, but NO ordering
# ---------------------------------------------------------------------------
# Complex numbers support == and != (they can be compared for equality),
# but they are NOT ordered. "<" and ">" raise TypeError because "greater
# than" is not defined for complex numbers.
z1, z2 = 3 + 4j, 4 + 3j
print("\n--- equality vs ordering ---")
print("3+4j == 3+4j         ->", 3 + 4j == 3 + 4j)   # True
print("3+4j == 4+3j         ->", z1 == z2)            # False
print("3+4j == 3+0j         ->", (3 + 4j) == (3 + 0j))  # False

# Ordering is not supported:
try:
    1j < 2j
except TypeError as e:
    print("1j < 2j              -> TypeError:", e)

# Which means you cannot sort or max() a list of complex numbers:
try:
    sorted([3j, 1j, 2j])
except TypeError as e:
    print("sorted([...])        -> TypeError:", e)

# This is a real difference from int/float. Sort by magnitude if you need it:
values = [3 + 4j, 1 + 0j, 0 + 2j]
by_magnitude = sorted(values, key=abs)
print("sorted by abs()      ->", by_magnitude)


# ---------------------------------------------------------------------------
# 6. Truthiness -- a subtle point
# ---------------------------------------------------------------------------
# A complex number is FALSY only when it is exactly zero (0+0j). Any other
# complex number, even a tiny one, is truthy.
print("\n--- truthiness ---")
print("bool(0j)             ->", bool(0j))                 # False
print("bool(1j)             ->", bool(1j))                 # True
print("bool(complex(0,0))   ->", bool(complex(0, 0)))      # False
print("bool(complex(0,1))   ->", bool(complex(0, 1)))      # True
# A common idiom: `if z:` is True whenever z is not exactly zero.


# ---------------------------------------------------------------------------
# 7. The `0j == 0` subtlety
# ---------------------------------------------------------------------------
# A complex zero equals integer and float zero, because its imaginary part
# is zero. This is correct but worth knowing.
print("\n--- zero comparison ---")
print("0j == 0              ->", 0j == 0)      # True !
print("0j == 0.0            ->", 0j == 0.0)    # True
print("1j == 1              ->", 1j == 1)      # False (imag part differs)
print("3+0j == 3            ->", (3 + 0j) == 3)  # True


# ---------------------------------------------------------------------------
# 8. Hashing, sets, and dicts
# ---------------------------------------------------------------------------
# Complex numbers are hashable, so they can be set members and dict keys.
print("\n--- hashing ---")
print("hash works           ->", hash(3 + 4j) == hash(3 + 4j))  # True
print("set dedupes          ->", {1j, 1j, 2j})   # {1j, 2j}
print("dict keyed by complex->", {1j: "i"})       # valid


# ---------------------------------------------------------------------------
# 9. The cmath module
# ---------------------------------------------------------------------------
# Standard `math` functions work on the REAL part only and will fail on
# complex input. The `cmath` module is the complex-aware version.
import math

print("\n--- math vs cmath ---")
print("math.sqrt(16)        ->", math.sqrt(16))        # 4.0 (real only)
try:
    math.sqrt(-1)
except ValueError as e:
    print("math.sqrt(-1)        -> ValueError:", e)    # rejects negatives
print("cmath.sqrt(-1)       ->", cmath.sqrt(-1))       # 1j (the answer!)

print("cmath.exp(1j)        ->", cmath.exp(1j))
print("cmath.log(-1)        ->", cmath.log(-1))        # 3.14159...j (i*pi)
print("cmath.sin(0)         ->", cmath.sin(0))         # 0j
print("cmath.cos(0)         ->", cmath.cos(0))         # (1+0j)

# cmath.polar / cmath.rect convert between rectangular and polar form.


# ---------------------------------------------------------------------------
# 10. Practical example: solving a quadratic
# ---------------------------------------------------------------------------
def solve_quadratic(a, b, c):
    """
    Solve ax^2 + bx + c = 0.
    Uses the quadratic formula with complex sqrt, so it also finds the
    complex roots when the discriminant is negative.
    """
    disc = cmath.sqrt(b * b - 4 * a * c)   # cmath handles negatives
    root1 = (-b + disc) / (2 * a)
    root2 = (-b - disc) / (2 * a)
    return root1, root2

print("\n--- practical: quadratic solver ---")
# x^2 - 5x + 6 = 0 has two real roots: 2 and 3
r1, r2 = solve_quadratic(1, -5, 6)
print("x^2 - 5x + 6  roots  ->", r1, "and", r2)
# x^2 + 1 = 0 has complex roots: +1j and -1j
r1, r2 = solve_quadratic(1, 0, 1)
print("x^2 + 1       roots  ->", r1, "and", r2)


# ---------------------------------------------------------------------------
# 11. Common beginner mistakes
# ---------------------------------------------------------------------------
def common_mistakes():
    """The complex-number errors beginners hit most often."""
    print("--- common mistakes ---")

    # MISTAKE 1: writing `j` instead of `1j`.
    # z = 5 + j    -> NameError (j is an undefined name)
    z = 5 + 1j     # correct
    print("  1. use 1j, not j ->", z)

    # MISTAKE 2: trying to compare complex numbers with < or >.
    # Sorting or max() of complex numbers fails. Sort by abs() instead.
    print("  2. no ordering; sort by abs() ->", sorted([3 + 4j, 1 + 0j], key=abs))

    # MISTAKE 3: using math.sqrt on a negative number.
    # math.sqrt(-1) -> ValueError. Use cmath.sqrt(-1) -> 1j.
    print("  3. use cmath.sqrt(-1) ->", cmath.sqrt(-1))

    # MISTAKE 4: expecting .real/.imag to be ints.
    # (3+4j).real is 3.0, a float, not the int 3.
    print("  4. (3+4j).real is a", type((3 + 4j).real).__name__,
          "->", (3 + 4j).real)

    # MISTAKE 5: thinking 0j is truthy. It is falsy like plain 0.
    print("  5. bool(0j) ->", bool(0j), "(falsy, like 0)")

    # MISTAKE 6: dividing by zero.
    try:
        (1 + 0j) / 0
    except ZeroDivisionError as e:
        print("  6. (1+0j)/0 -> ZeroDivisionError:", e)

    # MISTAKE 7: abs() gives the magnitude, not the complex value itself.
    # abs(3+4j) is 5.0 (a float), not (3+4j). Use the number directly if you
    # want to keep the complex value.


# ---------------------------------------------------------------------------
# 12. Best practices -- a short summary
# ---------------------------------------------------------------------------
def best_practices():
    """
    Guidelines for working with complex numbers:
      1. Always write `1j`, never `j`.
      2. .real and .imag always return floats, even for whole numbers.
      3. Use the cmath module (not math) for complex math; math functions
         either ignore the imaginary part or raise on complex input.
      4. Complex numbers are not ordered: you cannot use <, >, sorted(), or
         max() directly. Sort by key=abs if you need an order.
      5. abs(z) returns the magnitude as a float; use it for comparisons.
      6. 0j is falsy and equals 0; 1j is truthy.
      7. complex(0) and 0j represent the same value; choose one style.
      8. Use them when the maths calls for it (Fourier, circuits, quantum);
         for plain real maths, stick to int/float.
    """
    print("--- best practices (see docstring) ---")
    print("magnitude of 3+4j:", abs(3 + 4j))  # 5.0


# Run every demo when the file is executed directly.
def main():
    common_mistakes()
    best_practices()
    print("\nAll complex examples finished.")


if __name__ == "__main__":
    main()
