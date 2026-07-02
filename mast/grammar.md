# The Grammar for mast

```ebnf
Equation       = Expression, "=", Expression | Expression ;
Expression     = Term, { ("+" | "-"), Term } ;
Term           = Factor, { ("*" | "/"), Factor } ;
Factor         = Base, [ "^", Factor ] ;
Base           = "-", Base
               | "+", Base
               | "(", Expression, ")"
               | FunctionCall
               | Number
               | Variable ;
FunctionCall   = Identifier, "(", Expression, ")" (*Identifier mus be a known function name*)
```
