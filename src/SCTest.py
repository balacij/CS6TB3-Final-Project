# coding: utf-8

# ### P0 Scanner Tests
#
# #### Original Author: Emil Sekerinski, McMaster University, revised March 2021
#
# Tests scanner output and produces all scanner error messages.


from P0 import compileString
import SC


# Procedure `scanString` collects the symbols recognized by the scanner into a list. The list consists of pair with `SC.sym` and `SC.newline`; other variables of `SC` like `SC.val`, `SC.pos`, etc. are not included, but the code can easily be modified.


from SC import (
    TIMES,
    DIV,
    MOD,
    AND,
    PLUS,
    MINUS,
    OR,
    EQ,
    NE,
    LT,
    GT,
    LE,
    GE,
    PERIOD,
    COMMA,
    COLON,
    NOT,
    LPAREN,
    RPAREN,
    LBRAK,
    RBRAK,
    LARROW,
    RARROW,
    LBRACE,
    RBRACE,
    CARD,
    COMPLEMENT,
    UNION,
    INTERSECTION,
    ELEMENT,
    SUBSET,
    SUPERSET,
    DOTDOT,
    THEN,
    DO,
    BECOMES,
    NUMBER,
    IDENT,
    SEMICOLON,
    ELSE,
    IF,
    WHILE,
    CONST,
    TYPE,
    VAR,
    SET,
    PROCEDURE,
    PROGRAM,
    INDENT,
    DEDENT,
    EOF,
    ADT_SEP,
    CASE,
    OF,
    DEFAULT,
    NIL,
    NOTHING,
    CHAR,
)

symbol = {
    TIMES: 'TIMES',
    DIV: 'DIV',
    MOD: 'MOD',
    AND: 'AND',
    PLUS: 'PLUS',
    MINUS: 'MINUS',
    OR: 'OR',
    EQ: 'EQ',
    NE: 'NE',
    LT: 'LT',
    GT: 'GT',
    LE: 'LE',
    GE: 'GE',
    PERIOD: 'PERIOD',
    COMMA: 'COMMA',
    COLON: 'COLON',
    NOT: 'NOT',
    LPAREN: 'LPAREN',
    RPAREN: 'RPAREN',
    LBRAK: 'LBRAK',
    RBRAK: 'RBRAK',
    LARROW: 'LARROW',
    RARROW: 'RARROW',
    LBRACE: 'LBRACE',
    RBRACE: 'RBRACE',
    CARD: 'CARD',
    COMPLEMENT: 'COMPLEMENT',
    UNION: 'UNION',
    INTERSECTION: 'INTERSECTION',
    ELEMENT: 'ELEMENT',
    SUBSET: 'SUBSET',
    SUPERSET: 'SUPERSET',
    DOTDOT: 'DOTDOT',
    THEN: 'THEN',
    DO: 'DO',
    BECOMES: 'BECOMES',
    NUMBER: 'NUMBER',
    IDENT: 'INDENT',
    SEMICOLON: 'SEMICOLON',
    ELSE: 'ELSE',
    IF: 'IF',
    WHILE: 'WHILE',
    CONST: 'CONST',
    TYPE: 'TYPE',
    VAR: 'VAR',
    SET: 'SET',
    PROCEDURE: 'PROCEDURE',
    PROGRAM: 'PROGRAM',
    INDENT: 'INDENT',
    DEDENT: 'DEDENT',
    CASE: 'CASE',
    NOTHING: 'NOTHING',
    ADT_SEP: 'ADT_SEP',
    OF: 'OF',
    DEFAULT: 'DEFAULT',
    NOTHING: 'NOTHING',
    NIL: 'NIL',
    CHAR: 'CHAR',
}

global i, doPrint
i = 0
doPrint = True


def scanString(src):  # for a more readable scanner output
    global i
    SC.init(src)
    syms = []
    while SC.sym != SC.EOF:
        syms.append((symbol[SC.sym], SC.newline))
        SC.getSym()
    if doPrint:
        print('SCANNING TEST:', i)
        print(syms)
    i = i + 1
    return syms


# test; i = 0
scanString(
    """

program p

  if a then
    writeln()
  else
    writeln()
  if a then writeln() else writeln()
"""
)


# test; i = 1
scanString(
    """
type T = [1..10] → integer
var a: T
procedure r()
    a[3] := 9
program p
  a[3] := 9
"""
)


# test; i = 2
scanString(
    """
type Maybe = Just(v: integer) | Nothing

program p
  var m: Maybe
  m <- Just(1)
"""
)


# test; i = 3
scanString(
    """
program
y := 5
if a then
  if b then
    a := b
x := 3
"""
)


# test; i = 4
scanString(
    """
program p
  while 2 > 3 do
    write(1)
"""
)


# test; i = 5
scanString(
    """// comment 1
program p     // comment 2
  writeNewLine()   // comment 3
              // comment 4
"""
)


# #### Error "number too large"
print('EXPECTING: number too large error')


compileString(
    """
const c = 12345678901234567890
"""
)


# #### Error "illegal character"
print('EXPECTING: illegal character error')


compileString(
    """
program p_
  writeNewLine()
"""
)
