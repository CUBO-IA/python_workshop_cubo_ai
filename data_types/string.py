"""
STRING (str) - Python's text data type.

What is a string?
-----------------
A string is a sequence of characters. In Python it is written between quotes,
either single `'like this'` or double `"like this"`. The two are equivalent;
use double quotes when the text itself contains an apostrophe, and vice versa.

    name = 'Ada'
    quote = "It's fine"

How does it work?
-----------------
* Strings are IMMUTABLE: you cannot change a character in place. Every method
  that "changes" a string actually returns a brand-new string.
* They are SEQUENCES, so indexing (`s[0]`), slicing (`s[1:4]`) and looping all
  work on them.
* Indexing starts at 0 and negative indices count from the end (`s[-1]`).
* Unicode is fully supported: `"café"`, `"日本"`, and emoji all work, and
  `len()` counts characters (not bytes) for these.
* Strings are hashable, so they can be dict keys and set members.
* Triple-quoted strings span multiple lines and are used for docstrings.

Run this file:  python3 string.py
"""


# ---------------------------------------------------------------------------
# 1. Creating strings
# ---------------------------------------------------------------------------
# Single quotes, double quotes -- both create the same type:
single = 'Hello'
double = "Hello"
print("single == double     ->", single == double)   # True

# Use the other quote style to avoid escaping:
msg = "It's Python's job to be readable"
print("apostrophe inside    ->", msg)

# Escapes: a backslash lets you put special characters inside a string.
print("\n--- escape sequences ---")
print(r"\n (backslash n)     ->", "line1\nline2")   # newline
print(r"\t (backslash t)     ->", "col1\tcol2")     # tab
print(r"\\ (two backslash)  ->", "C:\\Users\\ada")  # literal backslash
print(r"\" (escaped quote)  ->", "She said \"hi\"")
print("newline via print    ->"); print("line1\nline2")

# Triple quotes: multi-line strings and docstrings.
multi_line = """This is
a multi-line
string."""
print("multi-line length    ->", len(multi_line))

# Raw strings: backslashes are taken literally (great for file paths/regex).
windows_path = r"C:\Users\ada\Documents"
print("raw string path      ->", windows_path)


# ---------------------------------------------------------------------------
# 2. Checking the type
# ---------------------------------------------------------------------------
print("\ntype('hello')        ->", type("hello"))              # <class 'str'>
print("isinstance('h', str) ->", isinstance("hello", str))
print("len('hello')         ->", len("hello"))               # 5 characters
# len() counts characters, not bytes -- important for Unicode:
print("len('café')          ->", len("café"))   # 4 characters
print("len('日本')          ->", len("日本"))          # 2 characters


# ---------------------------------------------------------------------------
# 3. Indexing -- accessing single characters
# ---------------------------------------------------------------------------
s = "Python"
#              P  y  t  h  o  n
# index:       0  1  2  3  4  5
# negative:   -6 -5 -4 -3 -2 -1
print("\n--- indexing on 'Python' ---")
print("s[0]   (first char)  ->", s[0])    # 'P'
print("s[2]                 ->", s[2])    # 't'
print("s[-1]  (last char)   ->", s[-1])   # 'n'
print("s[-2]                ->", s[-2])   # 'o'
print("s[len(s)-1]           ->", s[len(s) - 1])  # same as s[-1]

# Out-of-range index raises IndexError:
# s[100]  -> IndexError: string index out of range
print("s[0].upper()         ->", s[0].upper())


# ---------------------------------------------------------------------------
# 4. Slicing -- accessing a substring
# ---------------------------------------------------------------------------
# Syntax: s[start : stop : step]
#   start = index to begin at (inclusive, default 0)
#   stop  = index to end at EXCLUSIVE (not included)
#   step  = jump size (default 1)
s = "Python"
print("\n--- slicing on 'Python' ---")
print("s[0:3]   (start:stop)->", s[0:3])    # 'Pyt' (chars 0,1,2)
print("s[:3]    (to index 3)->", s[:3])     # 'Pyt'
print("s[3:]    (from 3)    ->", s[3:])     # 'hon'
print("s[:]     (whole copy)->", s[:])      # 'Python'
print("s[::2]   (every 2nd) ->", s[::2])    # 'Pto'
print("s[::-1]  (reversed)  ->", s[::-1])   # 'nohtyP'
print("s[-3:]   (last 3)    ->", s[-3:])    # 'hon'
print("s[1:-1]  (drop ends) ->", s[1:-1])   # 'yth'


# ---------------------------------------------------------------------------
# 5. Strings are immutable
# ---------------------------------------------------------------------------
# You cannot assign to an index. This raises TypeError:
#   s[0] = 'J'  -> TypeError: 'str' object does not support item assignment
#
# Instead, build a NEW string:
name = "python"
renamed = "J" + name[1:]
print("\n--- immutability ---")
print("name                 ->", name)          # unchanged
print("'J' + name[1:]       ->", renamed)       # 'Jython' as a new string

# This is why string methods return new strings and never edit in place.
print("'  hi  '.strip() is a new string ->", repr("  hi  ".strip()))


# ---------------------------------------------------------------------------
# 6. String methods -- the essentials
# ---------------------------------------------------------------------------
# Strings have a huge set of built-in methods. These are the ones you will
# use most often. Methods are called with dot notation: s.method(args).

# --- CASE methods ---
text = "Hello World"
print("\n--- case methods ---")
print("text.lower()         ->", text.lower())     # 'hello world'
print("text.upper()         ->", text.upper())     # 'HELLO WORLD'
print("text.title()         ->", text.title())     # 'Hello World'
print("text.swapcase()      ->", text.swapcase())  # swap each letter's case
print("text.capitalize()    ->", text.capitalize())# 'Hello world' (first only)

# --- STRIP / WHITESPACE methods ---
padded = "   spaced out   "
print("\n--- whitespace methods ---")
print("padded.strip()       ->", repr(padded.strip()))   # both ends
print("padded.lstrip()      ->", repr(padded.lstrip()))  # left only
print("padded.rstrip()      ->", repr(padded.rstrip()))  # right only

# --- FINDING & COUNTING ---
print("\n--- finding & counting ---")
print("text.find('World')   ->", text.find("World"))   # 6 (index, -1 if absent)
print("text.find('Python')  ->", text.find("Python"))  # -1 (not found)
print("text.index('World')  ->", text.index("World"))  # 6 (raises if absent)
print("'banana'.count('a')  ->", "banana".count("a"))  # 3

# find returns the FIRST match; rfind returns the LAST:
print("'a-b-a'.find('a')    ->", "a-b-a".find("a"))     # 0
print("'a-b-a'.rfind('a')   ->", "a-b-a".rfind("a"))    # 4

# --- REPLACING ---
print("\n--- replacing ---")
print("text.replace('World','There') ->", text.replace("World", "There"))
print("replace only first  ->", "a-a-a".replace("a", "b", 1))  # count=1

# --- SPLITTING and JOINING ---
print("\n--- splitting & joining ---")
csv = "a,b,c,d"
parts = csv.split(",")               # split on a separator -> list
print("'a,b,c'.split(',')   ->", csv.split(","))
print("'one two three'.split() ->", "one two three".split())  # split on whitespace
print("'-'.join(parts)      ->", "-".join(parts))   # list -> string: 'a-b-c-d'
print("', '.join(['x','y']) ->", ", ".join(["x", "y"]))  # 'x, y'

# --- CHECKING (these return bool) ---
print("\n--- checking methods (return bool) ---")
print("'Hello'.startswith('He')  ->", "Hello".startswith("He"))
print("'Hello'.endswith('lo')    ->", "Hello".endswith("lo"))
print("'a1b2'.isalpha()     ->", "a1b2".isalpha())   # all letters? False
print("'123'.isdigit()      ->", "123".isdigit())    # all digits? True
print("'   '.isspace()     ->", "   ".isspace())    # all whitespace? True
print("'Hi'.isupper()       ->", "Hi".isupper())     # all upper? False
print("'hi'.islower()       ->", "hi".islower())     # all lower? True
print("'True'.isidentifier()->", "True".isidentifier())  # valid Python name?


# ---------------------------------------------------------------------------
# 7. String formatting -- f-strings (the modern way)
# ---------------------------------------------------------------------------
# f-strings (formatted string literals) are the cleanest way to build strings.
# Put an `f` before the quote and put expressions inside {}.
name = "Ada"
age = 36
score = 95.678

print("\n--- f-strings ---")
print(f"My name is {name} and I am {age} years old.")
print(f"Next year I will be {age + 1}.")         # expressions are allowed
print(f"2 + 3 equals {2 + 3}.")                 # even function calls work
print(f"Score: {score:.1f} out of 100")        # .1f -> 1 decimal place
print(f"Large number: {1234567:,}")             # thousands separator
print(f"Hex: {255:x}")                         # base-16

# Nested quotes inside f-strings (fine as long as the outer quotes differ):
print(f'{name} said "hello"')

# Debug helper: = prints the expression AND its value.
print(f"{name=}")    # name='Ada'  -- great for debugging


# ---------------------------------------------------------------------------
# 8. Other formatting methods (older but still useful)
# ---------------------------------------------------------------------------
print("\n--- other formatting methods ---")
print(".format()            ->", "Hello, {}! You are {}.".format(name, age))
print(".format() with index->", "Hello, {0}. Bye, {0}.".format(name))
print("f-string             ->", f"Hello, {name}! You are {age} years old.")

# The % operator (old C-style formatting, still seen in older code):
print("%-style              ->", "Hello, %s. You are %d." % (name, age))


# ---------------------------------------------------------------------------
# 9. Strings are iterable
# ---------------------------------------------------------------------------
# You can loop over a string one character at a time.
word = "banana"
print("\n--- iterating ---")
chars = [c for c in word if c == "a"]
print("count of 'a' via loop ->", len(chars))   # 3

# Common beginner task: reverse a string
print("reversed word        ->", word[::-1])

# Check if a word is a palindrome (same forwards and backwards):
candidate = "racecar"
print(f"'{candidate}' is a palindrome ->", candidate == candidate[::-1])


# ---------------------------------------------------------------------------
# 10. Practical mini-examples
# ---------------------------------------------------------------------------
def practical_examples():
    """Realistic small programs built from string operations."""
    print("\n--- practical examples ---")

    # 1. Clean up user input
    raw = "   Ada Lovelace   "
    print("1. clean input       ->", repr(raw.strip().title()))

    # 2. Initials from a full name
    full_name = "grace brewster murray hopper"
    initials = "".join(part[0] for part in full_name.split()).upper()
    print("2. initials          ->", initials)   # GBMH

    # 3. Title-case a sentence
    sentence = "the quick brown fox jumps"
    print("3. title case        ->", sentence.title())

    # 4. Count word occurrences in a sentence
    text = "to be or not to be that is the question"
    print("4. 'to' appears      ->", text.count("to"), "times")

    # 5. Extract a file extension
    filename = "report.pdf"
    stem, dot, ext = filename.rpartition(".")
    print("5. filename stem/ext ->", stem, "/", ext)

    # 6. URL-ish manipulation
    url = "https://example.com/page"
    domain = url.split("//")[1].split("/")[0]
    print("6. domain            ->", domain)

    # 7. Mask a credit card number
    card = "4111111111111111"
    masked = card[:-4] + "*" * 4
    print("7. masked card       ->", masked)

    # 8. Check a valid-looking email (simple check)
    email = "ada@example.com"
    is_valid_shape = "@" in email and "." in email.split("@")[-1]
    print("8. email looks valid ->", is_valid_shape)


# ---------------------------------------------------------------------------
# 11. Common beginner mistakes
# ---------------------------------------------------------------------------
def common_mistakes():
    """The string errors beginners hit most often."""
    print("--- common mistakes ---")

    # MISTAKE 1: forgetting quotes -> becomes a variable name (NameError).
    # text = hello       -> NameError: name 'hello' is not defined
    # text = "hello"     -> correct
    print("  1. Always quote your text: 'hello' not hello")

    # MISTAKE 2: mixing quotes when the text has an apostrophe.
    # bad:  msg = 'It's fine'     -> SyntaxError
    good = "It's fine"           # use double quotes outside
    print("  2. mix quote styles to avoid errors ->", good)

    # MISTAKE 3: `+` does not add a space, and fails for non-strings.
    first, last = "Ada", "Lovelace"
    print("  3. first + ' ' + last ->", first + " " + last)
    # print("x: " + 5)   -> TypeError (can't concat str and int)
    print("     use f-strings instead ->", f"x: {5}")   # works with any type

    # MISTAKE 4: using + in a loop is slow (builds a new string each time).
    # For many pieces, use ''.join(list) or an f-string.
    print("  4. prefer ''.join(parts) or f-strings over repeated +")

    # MISTAKE 5: strings are immutable, so `.strip()` etc. do NOT change
    # the variable unless you reassign it.
    s = "  hi  "
    _ = s.strip()          # result discarded -- s is unchanged!
    print("  5. s = s.strip() to keep the result; s is still", repr(s))


# ---------------------------------------------------------------------------
# 12. Best practices -- a short summary
# ---------------------------------------------------------------------------
def best_practices():
    """
    Guidelines for working with strings:
      1. Use f-strings for formatting -- they are fast and the most readable.
      2. Prefer the built-in methods (split, join, strip, replace, find)
         over manual loops for common string tasks.
      3. Remember strings are immutable: any "modifying" method returns a
         new string, so you must reassign the result.
      4. Use raw strings (r"...") for regular expressions and Windows paths
         to avoid escape-sequence surprises.
      5. Choose a consistent quote style (PEP 8 prefers double quotes) and
         switch style to avoid escaping.
      6. Use triple-quoted strings for docstrings and multi-line text.
      7. For simple membership, use `x in s` rather than `s.find(x) != -1`.
    """
    print("--- best practices (see docstring) ---")
    print("membership test:", "world" in "hello world")  # True


# Run every demo when the file is executed directly.
def main():
    practical_examples()
    common_mistakes()
    best_practices()
    print("\nAll string examples finished.")


if __name__ == "__main__":
    main()
