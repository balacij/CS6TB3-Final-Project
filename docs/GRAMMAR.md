# Grammar

Key grammar changes:
* ADTs -- TODO: describe
* Cases 
* You may define ADTs using multiple lines to separate the ADT Kinds.

Supplementary grammar changes:
* Single quoted characters are native conversions to integers. This, in addition to our changes to the standard procedures write, writeln, etc are purely done for improving the presentation and usability of our `strings.p` example.

Other grammar changes:
* We allow single-value returning procedures to be executed 'in-place' in expressions (without first setting them to variables)
* `<-` and `->` as alternatives for `←` and `→`, respectively
* `>=` and `<=` as alternatives for `≥` and `≤`, respectively
* `*` is added as an alternative to the multiplication symbol


```
    selector ::= { "[" expression "]" | "." ident}
    factor ::= ident selector | integer | "(" expression ")" | "{" [expression {"," expression}] "}" | ("¬" | "#" | "∁") factor
    term ::= factor {("×" | "div" | "mod" | "∩" | "and") factor}
    simpleExpression ::= ["+" | "-"] term {("+" | "-" | "∪" | "or") term}
    expression ::= simpleExpression
        {("=" | "≠" | "<" | "≤" | ">" | "≥" | "∈" | "⊆" | "⊇") simpleExpression}
    statementList ::= statement {";" statement}
    statementBlock ::= statementList {statementList}
    statementSuite ::= statementList | INDENT statementBlock DEDENT
    statement ::=
        ident selector ":=" expression |
        ident {"," ident} (":=" expression {"," expression} |
            "←" ident "(" [expression {"," expression}] ")") |
        "if" expression "then" statementSuite ["else" statementSuite] |
        "while" expression "do" statementSuite
    type ::=
        ident |
        "[" expression ".." expression "]" "→" type |
        "(" typedIds ")" |
        "set" "[" expression ".." expression "]"
    typedIds ::= ident {"," ident} ":" type {"," ident {"," ident} ":" type}.
    declarations ::= 
        {"const" ident "=" expression}
        {"type" ident "=" type}
        {"var" typedIds}
        {"procedure" ident "(" [typedIds] ")" [ "→" "(" typedIds ")" ] body}
    body ::= INDENT declarations (statementBlock | INDENT statementBlock DEDENT) DEDENT
    program ::= declarations "program" ident body
```
