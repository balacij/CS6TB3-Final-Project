# Grammar

## Key grammar changes:
* Disjoint union type definitions
  * _Note:_ You may define ADTs using multiple lines to separate the ADT Kinds.
* `case` statements

## Supplementary grammar changes:
* Single quoted characters (e.g., `'a'`, `'b'`, ...) are native conversions from UTF-8 characters to integers. This, in addition to our changes to the standard procedures `write`, `writeln`, etc are purely done for improving the presentation and usability of our `strings.p` example. More information on the changes to the standard procedures <a href="STANDARD_PROCEDURES.md">here</a>.

## Other grammar changes:
* We allow single-value returning procedures to be executed 'in-place' in expressions (without first setting them to variables)
* `<-` and `->` as alternatives for `←` and `→`, respectively
* `>=` and `<=` as alternatives for `≥` and `≤`, respectively
* `*` is added as an alternative to the multiplication symbol

## Full Grammar
```
    selector ::= { "[" expression "]" | "." ident}
    factor ::= ident selector | char | integer | "(" expression ")" | "{" [expression {"," expression}] "}" | ("¬" | "#" | "∁") factor
    term ::= factor {("×" | "*" | "div" | "mod" | "∩" | "and") factor}
    simpleExpression ::= ["+" | "-"] term {("+" | "-" | "∪" | "or") term}
    expression ::= simpleExpression
        {("=" | "≠" | "<" | "≤" | "<=" | ">" | "≥" | ">=" | "∈" | "⊆" | "⊇") simpleExpression}
    statementList ::= statement {";" statement}
    statementBlock ::= statementList {statementList}
    statementSuite ::= statementList | INDENT statementBlock DEDENT
    statement ::=
        ident selector ":=" expression |
        ident {"," ident} (":=" expression {"," expression} |
            ("←" | "<-") ident "(" [expression {"," expression}] ")") |
        "if" expression "then" statementSuite ["else" statementSuite] |
        "while" expression "do" statementSuite |
        "case" expression "of" "{" INDENT ["nil" ":" statementSuite] {ident ":" statementSuite} ["default" (":" statementSuite | "nothing")] DEDENT "}"
    type ::=
        ident ["(" typedIds ")"] {"|" ident ["(" typedIds ")"]} |
        "[" expression ".." expression "]" ("→" | "->") type |
        "(" typedIds ")" |
        "set" "[" expression ".." expression "]"
    typedIds ::= ident {"," ident} ":" type {"," ident {"," ident} ":" type}.
    declarations ::= 
        {"const" ident "=" expression}
        {"type" ident "=" type}
        {"var" typedIds}
        {"procedure" ident "(" [typedIds] ")" [ ("→" | "->") "(" typedIds ")" ] body}
    body ::= INDENT declarations (statementBlock | INDENT statementBlock DEDENT) DEDENT
    program ::= declarations "program" ident body
    char ::= "'" utf8Char "'"
```

where `utf8Char` is any valid `utf-8` character that Python can read.
