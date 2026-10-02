"""
SET (set) - Python's unordered collection of UNIQUE items.

What is a set?
--------------
A set is a collection that holds each item at most once, with no particular
order. It is written with curly braces (or built with the set() function):

    colours = {"red", "green", "blue"}

Think of a set as a bag of marbles where every marble is a different colour --
you can ask "is this colour in the bag?" instantly, but the bag has no
numbering, so there is no index 0 or 1.

How does it work?
-----------------
* UNIQUE: duplicates are automatically removed. `{"a", "a"}` is `{"a"}`.
* UNORDERED: the order of items is not guaranteed and can change between
  runs. Never rely on set order.
* MUTABLE: you can add and remove items.
* HASHABLE: the items inside must be hashable (str, int, float, tuple) --
  you cannot put a list or dict inside a set.
* VERY FAST membership tests: `x in my_set` is far quicker than scanning a
  list, which makes sets ideal for de-duplication and fast lookups.
* Set operations (union, intersection, difference) mirror set theory in maths.

Run this file:  python3 set.py
"""


# ---------------------------------------------------------------------------
# 1. Creating sets
# ---------------------------------------------------------------------------
# Curly braces, comma-separated.
colours = {"red", "green", "blue"}

# The KEY POINT: duplicates vanish automatically.
duplicates = {"a", "b", "a", "c", "b"}
print("colours              ->", colours)
print("with duplicates      ->", duplicates)   # {'a', 'b', 'c'} -- dupes removed
print("len(duplicates)      ->", len(duplicates))  # 3, not 5

# THE CRITICAL TRAP: {} is an EMPTY DICTIONARY, not an empty set!
print("\n--- the {} trap ---")
print("type({})             ->", type({}).__name__)          # dict  !!
print("type(set())          ->", type(set()).__name__)      # set   correct
empty = set()                                          # always use this
print("empty set length     ->", len(empty))

# The set() constructor works from any iterable:
print("set([1, 2, 2, 3])   ->", set([1, 2, 2, 3]))     # {1, 2, 3}
print("set('hello')         ->", set("hello"))          # {'h','e','l','o'}
print("type(colours)        ->", type(colours))
print("isinstance(c,set)    ->", isinstance(colours, set))


# ---------------------------------------------------------------------------
# 2. Sets are unordered -- why order is not guaranteed
# ---------------------------------------------------------------------------
# Python stores set items in a hash table, so the order looks arbitrary and
# can differ between runs and versions. NEVER rely on it.
nums = {10, 20, 30}
print("\n--- unordered ---")
print("set of ints          ->", nums)   # order is not guaranteed!
print("indexing nums[0]     -> NOT POSSIBLE (TypeError: not subscriptable)")

# If you need a predictable order, sort it or convert to a list:
print("sorted(set)          ->", sorted(nums))    # [10, 20, 30]
print("list(set)            ->", list(nums))      # arbitrary order


# ---------------------------------------------------------------------------
# 3. Adding and removing items
# ---------------------------------------------------------------------------
fruits = {"apple", "banana"}

# add() inserts one item (no-op if already present):
fruits.add("cherry")
fruits.add("cherry")          # adding twice changes nothing
print("\nafter add()          ->", fruits)

# update() adds MANY items at once:
fruits.update(["date", "elderberry"])
print("after update()       ->", fruits)

# remove() deletes an item but RAISES KeyError if it is missing:
fruits.remove("banana")
# fruits.remove("banana")    # would raise KeyError the second time
print("after remove()       ->", fruits)

# discard() is the safe version -- it does nothing if the item is absent:
fruits.discard("banana")      # already gone; no error
fruits.discard("banana")      # still no error
print("discard() is safe    ->", fruits)

# pop() removes and returns an ARBITRARY element (no order guarantee):
arbitrary = fruits.pop()
print("pop() returned       ->", arbitrary, "(arbitrary)")

# clear() empties the set:
temp = {1, 2, 3}
temp.clear()
print("after clear()        ->", temp)


# ---------------------------------------------------------------------------
# 4. Set operations (the maths!)
# ---------------------------------------------------------------------------
# Sets support the classic operations from set theory, using | & - ^ or the
# named methods. These are the biggest reason to reach for a set.
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

print("\n--- set operations (a={1..5}, b={4..8}) ---")
print("a | b   (union)      ->", a | b)          # everything in either
print("a & b   (intersection)->", a & b)          # common to both
print("a - b   (difference) ->", a - b)          # in a, not in b
print("b - a   (reverse diff)->", b - a)          # in b, not in a
print("a ^ b   (symmetric)  ->", a ^ b)          # in either, not both

# The same operations as named methods:
print("\n--- as methods ---")
print("a.union(b)           ->", a.union(b))
print("a.intersection(b)    ->", a.intersection(b))
print("a.difference(b)      ->", a.difference(b))
print("a.symmetric_diff(b)  ->", a.symmetric_difference(b))
print("a.issubset(b)        ->", a.issubset(b))       # False
print("a.isdisjoint(b)      ->", a.isdisjoint(b))     # False (they share 4,5)

# Realistic example: find who follows both accounts.
ada_follows = {"bob", "carol", "dave"}
ben_follows = {"carol", "dave", "erin"}
print("\nmutual followers     ->", ada_follows & ben_follows)   # {'carol','dave'}


# ---------------------------------------------------------------------------
# 5. Membership testing -- where sets shine
# ---------------------------------------------------------------------------
# `x in aset` is O(1) -- instant. For a list, Python must scan every item.
# Membership checks are much faster on sets than on lists.
aset = {10, 20, 30}
alist = [10, 20, 30]

print("\n--- membership ---")
print("20 in aset           ->", 20 in aset)     # True
print("99 in aset           ->", 99 in aset)     # False
print("20 in alist          ->", 20 in alist)    # True (same answer, slower)

# Removing duplicates from a list -- THE classic set use case:
numbers = [1, 2, 2, 3, 3, 3, 4, 1]
unique = list(set(numbers))
print("\noriginal list        ->", numbers)
print("deduplicated         ->", sorted(unique))    # sorted for stable output
# Note: set() does NOT preserve order. Sort it if order matters.

# Find duplicates in a list:
seen = set()
dupes = {x for x in numbers if x in seen or seen.add(x)}
print("duplicates found     ->", sorted(dupes))   # {1, 2, 3}


# ---------------------------------------------------------------------------
# 6. Sets only hold hashable items
# ---------------------------------------------------------------------------
# You cannot store a list or a dict inside a set (they are unhashable).
valid = {1, "two", 3.0, (4, 5)}    # int, str, float, tuple -- all fine
print("\n--- hashable items only ---")
print("valid set            ->", valid)

try:
    {[1, 2, 3]}
except TypeError as e:
    print("list in a set        -> FAILS:", e)
try:
    {{"a": 1}}
except TypeError as e:
    print("dict in a set        -> FAILS:", e)

# Workaround: convert to a tuple first (a tuple IS hashable):
print("tuple instead of list ->", {(1, 2, 3)})   # works
print("frozenset of a set   ->", frozenset({1, 2, 3}))   # immutable set


# ---------------------------------------------------------------------------
# 7. Comparing sets
# ---------------------------------------------------------------------------
a = {1, 2, 3}
b = {1, 2, 3}
c = {3, 2, 1}       # different literal order...

print("\n--- comparing sets ---")
print("a == b             ->", a == b)   # True
print("a == c             ->", a == c)   # True! (order does not matter)


# ---------------------------------------------------------------------------
# 8. Common beginner mistakes
# ---------------------------------------------------------------------------
def common_mistakes():
    """The set errors beginners hit most often."""
    print("--- common mistakes ---")

    # MISTAKE 1: {} is an empty DICT, not an empty set.
    print("  1. {} is a", type({}).__name__, "-- use set() for an empty set")

    # MISTAKE 2: expecting set() to preserve order.
    # list(set([3,1,2])) has an arbitrary order. Sort if order matters.
    print("  2. set order is arbitrary ->", sorted(set([3, 1, 2])))

    # MISTAKE 3: trying to index a set. Sets have no order, so no indexing.
    s = {1, 2, 3}
    # s[0]   -> TypeError: 'set' object is not subscriptable
    print("  3. no indexing on sets; use list(s) or sorted(s) instead")

    # MISTAKE 4: remove() vs discard().
    # remove() raises KeyError if absent; discard() does not.
    s = {1, 2}
    s.discard(99)     # safe
    # s.remove(99)    # would raise KeyError
    print("  4. discard() is safe; remove() raises if missing ->", s)

    # MISTAKE 5: using a set when order matters (e.g. displaying a list).
    # If you care about order, use a list or sort() the set.

    # MISTAKE 6: thinking a set changes a list in place. set(x) makes a NEW set.
    original = [1, 2, 2, 3]
    _ = set(original)     # does NOT modify original
    print("  5. set(list) builds a new set; original stays ->", original)


# ---------------------------------------------------------------------------
# 9. Best practices -- a short summary
# ---------------------------------------------------------------------------
def best_practices():
    """
    Guidelines for working with sets:
      1. Use a set when you need uniqueness or fast membership tests
         (`x in my_set`).
      2. Use set(list) to de-duplicate, then sort() if order matters.
      3. Prefer the named methods (.union, .intersection, .difference) or
         the operators (|, &, -) -- both are clear and fast.
      4. Remember {} is an empty dict; always use set() for an empty set.
      5. Sets are unordered -- never rely on iteration order or indexing.
      6. Only hashable items (str, int, float, tuple) can go in a set.
      7. Use frozenset() when you need an immutable, hashable set (e.g. as
         a dict key or another set's member).
      8. use discard() for safe removal; remove() if missing should error.
    """
    print("--- best practices (see docstring) ---")
    print("frozenset is hashable:", isinstance(frozenset({1, 2}), frozenset))


# Run every demo when the file is executed directly.
def main():
    common_mistakes()
    best_practices()
    print("\nAll set examples finished.")


if __name__ == "__main__":
    main()
