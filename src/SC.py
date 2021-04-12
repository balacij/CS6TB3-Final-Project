# coding: utf-8

# ## P0 Scanner
# #### Original Author: Emil Sekerinski, revised March 2021
# The scanner reads the characters of the source consecutively and recognizes symbols they form:
# - procedure `init(src)` initializes the scanner
# - procedure `getSym()` recognizes the next symbol and assigns it to variables `sym` and `val`.
# - procedure `mark(msg)` prints an error message at the current location in the source.
#
# Symbols are encoded by integer constants.


TIMES = 1
DIV = 2
MOD = 3
AND = 4
PLUS = 5
MINUS = 6
OR = 7
EQ = 8
NE = 9
LT = 10
GT = 11
LE = 12
GE = 13
PERIOD = 14
COMMA = 15
COLON = 16
NOT = 17
LPAREN = 18
RPAREN = 19
LBRAK = 20
RBRAK = 21
LARROW = 22
RARROW = 23
LBRACE = 24
RBRACE = 25
CARD = 26
COMPLEMENT = 27
UNION = 28
INTERSECTION = 29
ELEMENT = 30
SUBSET = 31
SUPERSET = 32
DOTDOT = 33
THEN = 34
DO = 35
BECOMES = 36
NUMBER = 37
IDENT = 38
SEMICOLON = 39
ELSE = 40
IF = 41
WHILE = 42
CONST = 43
TYPE = 44
VAR = 45
SET = 46
PROCEDURE = 47
PROGRAM = 48
INDENT = 49
DEDENT = 50
EOF = 51

ADT_SEP = 100
CASE = 101
OF = 102
DEFAULT = 103
NIL = 104
NOTHING = 105

CHAR = 110

SHOW_WARNINGS = False

# Following variables determine the state of the scanner:
#
# - `(line, pos)` is the location of the current symbol in source
# - `(lastline, lastpos)` is used to more accurately report errors
# - `ch` is the current character
# - `sym` the current symbol, `TIMES` ... `EOF` or `None`
# - if `sym` is `NUMBER`, `val` is the value of the number
# - if `sym` is `IDENT`, `val` is the identifier string
# - `source` is the string with the source program
# - `index` is the index of the next character in `source`
# - `indents` is a stack with indentations
# - `newline` is a boolean indicating the start of a line
#
# The source is specified as a parameter to the procedure `init`:


def init(src):
    global line, lastline, pos, lastpos
    global ch, sym, val, source, index, indents
    line, lastline = 0, 1
    pos, lastpos = 1, 1
    ch, sym, val, source, index = "\n", None, None, src, 0
    indents = [1]
    getChar()
    getSym()


# Procedure `getChar()` assigns the next character in `ch`, or assigns `chr(0)` at the end of the source. Variables `line`, `pos` are updated with the current location in the source and `lastline`, `lastpos` are updated with the location of the previously read character.


def getChar():
    global line, lastline, pos, lastpos, ch, index
    if index == len(source):
        ch, index, pos = chr(0), index + 1, 1
    else:
        lastpos = pos
        if ch == "\n":
            pos, line = 1, line + 1
        else:
            lastline, pos = line, pos + 1
        ch, index = source[index], index + 1


# Procedure `mark(msg)` prints an error message with the current location in the source. To avoid a cascade of errors, only one error message at a source location is printed.


def mark(msg):
    raise Exception("line " + str(lastline) + " pos " + str(lastpos) + " " + msg)


def warning(msg):
    if SHOW_WARNINGS:
        print(f'WARNING: line {str(lastline)}: {msg}')


# Procedure `number()` parses
#
#     number ::= digit {digit}
#     digit ::= '0' | ... | '9'
#
# If the number fits in 32 bits, sets `sym` to `NUMBER` and assigns to number to `val`, otherwise reports an error.


def number():
    global sym, val
    sym, val = NUMBER, 0
    while "0" <= ch <= "9":
        val = 10 * val + int(ch)
        getChar()
    if val >= 2 ** 31:
        mark("number too large")


# Procedure `char()` parses
#
#     char ::= "'" utf8 "'"
#


def char():
    global sym, val
    try:
        sym, val = CHAR, ord(ch)
        getChar()
    except:
        mark(f"invalid char; `{ch}`")

    if ch == "'":
        getChar()
    else:
        mark("expected closing '")


# Procedure `identKW()` parses
#
#     identKW ::= keyword | identifier
#     identifier ::= letter {letter | digit}
#     letter ::= 'A' | ... | 'Z' | 'a' | ... | 'z'
#     keyword ::= 'div' | 'mod' | 'and' | 'or' | 'then' | 'do' | 'else' | 'if' | 'while' |
#                          'const' | 'type' | 'var' | 'set' | 'procedure' | 'program'
#
# The longest sequence of character that matches `letter {letter | digit}` is read. If that sequence is a keyword, `sym` is set accordingly, otherwise `sym` is set to `IDENT`.


KEYWORDS = {
    "div": DIV,
    "mod": MOD,
    "and": AND,
    "or": OR,
    "then": THEN,
    "do": DO,
    "else": ELSE,
    "if": IF,
    "while": WHILE,
    "const": CONST,
    "type": TYPE,
    "var": VAR,
    "set": SET,
    "procedure": PROCEDURE,
    "program": PROGRAM,
    "case": CASE,
    "of": OF,
    "default": DEFAULT,
    "nil": NIL,
    "nothing": NOTHING,
}


def identKW():
    global sym, val
    start = index - 1
    while ("A" <= ch <= "Z") or ("a" <= ch <= "z") or ("0" <= ch <= "9"):
        getChar()
    val = source[start : index - 1]
    sym = KEYWORDS[val] if val in KEYWORDS else IDENT


# Procedure `comment()` parses
#
#     comment ::= '//' {character - '\n'}
#
# A comment is skipped over.


def comment():
    if ch == "/":
        getChar()
    else:
        mark("// expected")
    while chr(0) != ch != "\n":
        getChar()


# Procedure `getSym()` parses
#
#     symbol ::= { ' ' | comment} ( { '\n' {' ' | comment} } | identKW | number | '×' | '*' | '+' | '-' | '=' | '≠' |
#                         '<' | '≤' | '>' | '≥' | ';' | ',' | ':' | ':=' | '.' | '¬' | '(' |  ')' | '[' | ']' | '<-' | '←' | '→' | '->' | '{' | '}' |
#                         '#' | '∁' | '∪' | '∩' | '∈' | '⊆' | '⊇')
#
# If a valid symbol is recognized, `sym` is set accordingly, otherwise an error is reported. The longest match is used for recognizing operators. Blanks that are not at the beginning of a line are skipped. A stack, `indents`, is used to keep track if blanks at the beginning of a line are either ignored or recognized as `INDENT` or `DEDENT`. On the first symbol of a line, `newline` is set to `True` if the indentation is the same as that of the previous line; for all subsequent symbols, `newline` is set to `False`. At the end of the source, `sym` is set to `EOF`.


def getSym():
    global sym, indents, newline
    if pos < indents[0]:
        indents = indents[1:]
        sym = DEDENT
    else:
        while ch in " /":
            if ch == " ":
                getChar()  # skip blanks between symbols
            else:
                comment()
        if ch == "\n":  # possibly INDENT, DEDENT
            while ch == "\n":  # skip blank lines
                getChar()
                while ch in " /":
                    if ch == " ":
                        getChar()  # skip indentation
                    else:
                        comment()
            if pos < indents[0]:
                sym, indents = DEDENT, indents[1:]
                return
            elif pos > indents[0]:
                sym, indents = INDENT, [pos] + indents
                return
        newline = pos == indents[0]
        if "A" <= ch <= "Z" or "a" <= ch <= "z":
            identKW()
        elif "0" <= ch <= "9":
            number()
        elif ch == "'":
            getChar()
            char()
        elif ch == "×":
            getChar()
            sym = TIMES
        elif ch == "*":
            getChar()
            sym = TIMES
        elif ch == "+":
            getChar()
            sym = PLUS
        elif ch == "-":
            getChar()
            sym = MINUS
            if ch == ">":
                getChar()
                sym = RARROW
        elif ch == "=":
            getChar()
            sym = EQ
        elif ch == "≠":
            getChar()
            sym = NE
        elif ch == "<":
            getChar()
            sym = LT
            if ch == "-":
                getChar()
                sym = LARROW
            elif ch == '=':
                getChar()
                sym = LE
        elif ch == "≤":
            getChar()
            sym = LE
        elif ch == ">":
            getChar()
            sym = GT
            if ch == '=':
                getChar()
                sym = GE
        elif ch == "≥":
            getChar()
            sym = GE
        elif ch == ";":
            getChar()
            sym = SEMICOLON
        elif ch == ",":
            getChar()
            sym = COMMA
        elif ch == ":":
            getChar()
            if ch == "=":
                getChar()
                sym = BECOMES
            else:
                sym = COLON
        elif ch == ".":
            getChar()
            if ch == ".":
                getChar()
                sym = DOTDOT
            else:
                sym = PERIOD
        elif ch == "¬":
            getChar()
            sym = NOT
        elif ch == "(":
            getChar()
            sym = LPAREN
        elif ch == ")":
            getChar()
            sym = RPAREN
        elif ch == "[":
            getChar()
            sym = LBRAK
        elif ch == "]":
            getChar()
            sym = RBRAK
        elif ch == "←":
            getChar()
            sym = LARROW
        elif ch == "→":
            getChar()
            sym = RARROW
        elif ch == "{":
            getChar()
            sym = LBRACE
        elif ch == "}":
            getChar()
            sym = RBRACE
        elif ch == "#":
            getChar()
            sym = CARD
        elif ch == "∁":
            getChar()
            sym = COMPLEMENT
        elif ch == "∪":
            getChar()
            sym = UNION
        elif ch == "∩":
            getChar()
            sym = INTERSECTION
        elif ch == "∈":
            getChar()
            sym = ELEMENT
        elif ch == "⊆":
            getChar()
            sym = SUBSET
        elif ch == "⊇":
            getChar()
            sym = SUPERSET
        elif ch == "|":
            getChar()
            sym = ADT_SEP
        elif ch == chr(0):
            sym = EOF
        else:
            mark(f"illegal character; '{ch}'")
