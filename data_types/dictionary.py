"""
DICTIONARY (dict) - Python's key-value mapping.

What is a dictionary?
---------------------
A dictionary stores data as key-value pairs in curly braces:

    person = {"name": "Ada", "age": 36}

Each key is a unique label, and each value is the data stored under that label.
You look things up BY KEY rather than by position. Think of a real dictionary:
you search for a word (the key) to find its definition (the value).

How does it work?
-----------------
* Keys must be UNIQUE. Setting an existing key OVERWRITES its value.
* Keys must be HASHABLE: strings, numbers, and tuples work; lists and dicts
  do NOT (they are unhashable and raise TypeError).
* Values can be anything at all -- including other lists and dicts.
* Insertion order is preserved (Python 3.7+), so iteration is predictable.
* Dictionaries are MUTABLE: you can add, update, and delete entries.
* Lookup, insert, and delete are all very fast (average O(1)) because of
  how Python hashes keys internally.
* As of Python 3.7 a dict also guarantees that iterating over it yields keys
  in insertion order.

Run this file:  python3 dictionary.py
"""


# ---------------------------------------------------------------------------
# 1. Creating dictionaries
# ---------------------------------------------------------------------------
# Curly braces with key: value pairs.
person = {"name": "Ada", "age": 36, "city": "London"}

# Keys can be strings, numbers, or tuples:
scores = {95: "excellent", 80: "good", 60: "pass"}
coordinates = {(0, 0): "origin", (1, 1): "diagonal"}   # tuple keys

# Empty dictionary -- note {} is an EMPTY DICT, not an empty set.
# (an empty set is set())
empty = {}

# The dict() constructor is an alternative:
from_pairs = dict(name="Ada", age=36)

print("person               ->", person)
print("scores               ->", scores)
print("coordinates          ->", coordinates)
print("empty dict           ->", empty, " length:", len(empty))
print("type(person)         ->", type(person))        # <class 'dict'>
print("dict() constructor   ->", from_pairs)
print("len(person)          ->", len(person))         # 3 pairs


# ---------------------------------------------------------------------------
# 2. Accessing values
# ---------------------------------------------------------------------------
person = {"name": "Ada", "age": 36}

# Square brackets + the KEY (not an index):
print("\n--- accessing values ---")
print("person['name']       ->", person["name"])   # 'Ada'
print("person['age']        ->", person["age"])    # 36

# A missing key raises KeyError:
# person["email"]  -> KeyError: 'email'

# .get() is the SAFE way -- it returns a default instead of crashing:
print("\n.get('name')         ->", person.get("name"))            # 'Ada'
print(".get('email')        ->", person.get("email"))           # None
print(".get('email','n/a')  ->", person.get("email", "n/a"))    # 'n/a'

# Nested dict access: go step by step.
settings = {"user": {"name": "Ada", "lang": "python"}}
print("\nnested access        ->", settings["user"]["lang"])     # 'python'
# .get() chains safely, even if the key is missing:
print("nested .get chain    ->", settings.get("nope", {}).get("lang", "unknown"))


# ---------------------------------------------------------------------------
# 3. Adding and updating values
# ---------------------------------------------------------------------------
person = {"name": "Ada", "age": 36}

# Assigning to a NEW key adds it:
person["city"] = "London"
print("\nafter adding city    ->", person)

# Assigning to an EXISTING key overwrites it:
person["age"] = 37
print("after updating age   ->", person)   # age is now 37

# update() merges another dict (adds new keys, overwrites matching ones):
person.update({"age": 38, "job": "mathematician"})
print("after update()       ->", person)

# setdefault() adds a key ONLY if it is not already present:
person.setdefault("age", 99)        # age exists, so nothing changes
person.setdefault("country", "UK")  # country is new, so it is added
print("after setdefault()   ->", person)


# ---------------------------------------------------------------------------
# 4. Removing entries
# ---------------------------------------------------------------------------
person = {"name": "Ada", "age": 36, "city": "London"}

# del removes by key (raises KeyError if missing):
del person["city"]
print("\nafter del city       ->", person)

# pop() removes AND returns the value (with an optional default):
age = person.pop("age")
print("pop('age') returned  ->", age)
print("remaining            ->", person)

# pop() with a default is safe:
print("pop('missing', 0)    ->", person.pop("missing", 0))   # 0

# popitem() removes and returns the LAST (key, value) pair:
last = person.popitem()
print("popitem() removed    ->", last)

# clear() empties the whole dict:
temp = {"a": 1, "b": 2}
temp.clear()
print("after clear()        ->", temp)


# ---------------------------------------------------------------------------
# 5. Key rules -- what can be a key?
# ---------------------------------------------------------------------------
# Keys must be HASHABLE. Allowed: str, int, float, bool, tuple, frozenset.
# Not allowed: list, dict, set.
print("\n--- key rules ---")
print("str key              -> OK:  {'a': 1}")
print("int key              -> OK:  {1: 'one'}")
print("float key            -> OK:  {1.5: 'one and a half'}")
print("tuple key            -> OK:  {(1, 2): 'pair'}")

# Lists and dicts CANNOT be keys:
try:
    {[1, 2]: "list key"}
except TypeError as e:
    print("list key             -> FAILS:", e)
try:
    {{"a": 1}: "dict key"}
except TypeError as e:
    print("dict key             -> FAILS:", e)

# Note: 1 and 1.0 and True are all "equal" keys, so they collide:
print("\n1 == 1.0 == True     ->", 1 == 1.0 == True)   # True
collide = {1: "int", 1.0: "float", True: "bool"}
print("colliding keys       ->", collide)   # only one entry survives
print("how many keys?       ->", len(collide))   # 1


# ---------------------------------------------------------------------------
# 6. Checking and searching
# ---------------------------------------------------------------------------
person = {"name": "Ada", "age": 36, "city": "London"}

print("\n--- checking & searching ---")
print("'name' in person     ->", "name" in person)      # True
print("'email' in person    ->", "email" in person)     # False
print("len(person)          ->", len(person))
print("person.keys()        ->", list(person.keys()))   # the keys
print("person.values()      ->", list(person.values())) # the values
print("person.items()       ->", list(person.items()))  # (key, value) pairs

# get() with two different defaults:
print("\n.get('age', 0)       ->", person.get("age", 0))
print(".get('email', 0)     ->", person.get("email", 0))  # 0

# Finding all keys matching a condition:
inventory = {"apple": 5, "banana": 0, "cherry": 12}
in_stock = [k for k, v in inventory.items() if v > 0]
print("items in stock       ->", in_stock)   # ['apple', 'cherry']


# ---------------------------------------------------------------------------
# 7. Iterating over a dictionary
# ---------------------------------------------------------------------------
scores = {"alice": 90, "bob": 78, "carol": 95}

# Iterating a dict gives you the KEYS:
for name in scores:
    print("  key:", name)

# For key AND value, use .items():
print("\n--- iterating ---")
for name, score in scores.items():
    print(f"  {name}: {score}")

# This loop form is the most common dictionary pattern in real code.
total = sum(scores.values())
average = total / len(scores)
print("total / average      ->", total, "/", round(average, 2))

# Finding the highest score:
best = max(scores, key=scores.get)
print("best score holder    ->", best, "with", scores[best])


# ---------------------------------------------------------------------------
# 8. Dict comprehensions
# ---------------------------------------------------------------------------
# Like list comprehensions, but for building a dict.
#   {key_expr: value_expr for item in iterable}
#
# Regular loop:
squares = {}
for n in range(4):
    squares[n] = n * n
print("\nloop squares         ->", squares)

# Same as a dict comprehension:
squares = {n: n * n for n in range(4)}
print("comprehension        ->", squares)

# Invert a dict (swap keys and values):
scores = {"alice": 90, "bob": 78}
inverted = {v: k for k, v in scores.items()}
print("inverted dict        ->", inverted)   # {90: 'alice', 78: 'bob'}

# Filter a dict:
inventory = {"apple": 5, "banana": 0, "cherry": 12}
available = {k: v for k, v in inventory.items() if v > 0}
print("filtered dict        ->", available)


# ---------------------------------------------------------------------------
# 9. Nested dictionaries
# ---------------------------------------------------------------------------
# Values can themselves be dicts. This is how you model structured data.
users = {
    "ada": {
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "roles": ["admin", "editor"],      # a list inside a dict
    },
    "alan": {
        "name": "Alan Turing",
        "email": "alan@example.com",
        "roles": ["viewer"],
    },
}

print("\n--- nested dicts ---")
print("ada's email          ->", users["ada"]["email"])
print("alan's first role    ->", users["alan"]["roles"][0])
print("ada is admin?        ->", "admin" in users["ada"]["roles"])
print("number of users      ->", len(users))

# Safely reaching deep into possibly-missing data with .get():
role = users.get("bob", {}).get("roles", ["no roles"])
print("bob's roles (safe)   ->", role)   # ['no roles']


# ---------------------------------------------------------------------------
# 10. Copying a dictionary
# ---------------------------------------------------------------------------
# A plain assignment is an ALIAS, not a copy.
original = {"a": 1, "nested": {"x": 1}}
alias = original
alias["b"] = 2
print("\n--- copying ---")
print("original (aliased!)  ->", original)   # 'b' appears here too

# .copy() gives a SHALLOW copy: new top level, but nested values are shared.
shallow = original.copy()
shallow["c"] = 3
print("original after .copy ->", original)   # no 'c' (good)
print("shallow              ->", shallow)

# For fully independent nested structures, use deepcopy:
import copy
deep = copy.deepcopy(original)
deep["nested"]["x"] = 999
print("original nested safe ->", original["nested"]["x"])   # still 1 (good)


# ---------------------------------------------------------------------------
# 11. Common beginner mistakes
# ---------------------------------------------------------------------------
def common_mistakes():
    """The dictionary errors beginners hit most often."""
    print("--- common mistakes ---")

    # MISTAKE 1: KeyError from square brackets on a missing key.
    d = {"a": 1}
    # d["b"]      -> KeyError
    # d.get("b")  -> None (safe)
    print("  1. use .get('b') for a safe lookup ->", d.get("b"))

    # MISTAKE 2: using lists as keys (unhashable).
    # {[1, 2]: "x"}  -> TypeError: unhashable type: 'list'
    print("  2. keys must be hashable (str/int/tuple, not list/dict)")

    # MISTAKE 3: confusing a dict with a set. {} is an empty DICT;
    # an empty SET is set(). Watch for this in type annotations.
    print("  3. {{}} is an empty dict; set() is an empty set")

    # MISTAKE 4: modifying a dict while iterating over it -> RuntimeError.
    # Safe fix: iterate over list(d.keys()).
    d = {"a": 1, "b": 2}
    for key in list(d.keys()):    # list() makes a snapshot
        del d[key]
    print("  4. safe delete-while-iterating (list(d.keys())) ->", d)

    # MISTAKE 5: expecting .get() to store a default. It only RETURNS
    # the default if the key is missing; it does not add the key.
    d = {"a": 1}
    d.get("b", 99)                 # returns 99, but d is unchanged
    print("  5. .get() returns a default but does not insert it ->", d)

    # MISTAKE 6: iterating a dict gives KEYS, not key-value pairs.
    # For pairs you need .items().
    d = {"a": 1, "b": 2}
    print("  6. for k in d gives keys:", list(d))


# ---------------------------------------------------------------------------
# 12. Best practices -- a short summary
# ---------------------------------------------------------------------------
def best_practices():
    """
    Guidelines for working with dictionaries:
      1. Use .get(key, default) instead of d[key] when a key might be
         missing, to avoid KeyError.
      2. Choose meaningful, consistent keys -- string keys are most common.
      3. Loop with .items() to get key and value together.
      4. Use dict comprehensions to build or transform dicts concisely.
      5. Remember assignment to an existing key overwrites it; use
         .update() to merge several keys at once.
      6. Use .copy() for a shallow copy and copy.deepcopy() when nested
         data must be independent too.
      7. Test membership with `key in d`, not by catching KeyError.
      8. Iterate over list(d.keys()) if you plan to delete during a loop.
    """
    print("--- best practices (see docstring) ---")
    print("safe pattern:", {"a": 1}.get("b", "default"))   # 'default'


# Run every demo when the file is executed directly.
def main():
    common_mistakes()
    best_practices()
    print("\nAll dictionary examples finished.")


if __name__ == "__main__":
    main()
