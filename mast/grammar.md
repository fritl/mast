# The Grammar for mast

Equation -> Expression = Expression | Expression
Expression -> Term (+|- Term)*
Term -> Base (*|/ Base)*
Base -> -Base | +Base | (Expression) | Number | Variable
