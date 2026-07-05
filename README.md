<div align="center">
    <h1>Mast</h1>
</div>

<div align="center">
    <p>
        <picture>
              <source media="(prefers-color-scheme: dark)" srcset="branding/logo_dark_export.svg">
              <source media="(prefers-color-scheme: light)" srcset="branding/logo_light_export.svg">
              <img alt="Logo für Mast" src="logo_light_export.svg" width=300>
        </picture>
    </p>
    <p>
        Mast supports evaluation, simplifaction and differentiation of math
        inputs. Mast renders expressions as LaTeX or shows the abstract syntax
        tree.
    </p>
    <p>
        <picture>
            <source media="(prefers-color-scheme: dark)" srcset="docs/images/banner-dark.png">
            <source media="(prefers-color-scheme: light)" srcset="docs/images/banner-light.png">
            <img alt="Logo für Mast" src="docs/images/banner-light.png" width=800>
        </picture>
    </p>
    <a href="#">
        (Link to the demo)
    </a>
</div>


## Features

- **Output the AST.** A parser converts and outputs the math input into a form which the
  computer can easily handle.
- **Differentiate symbolically.** This means taking and expression and outputing
  the derivative also as an expression. For instance $x^2$ would produce
  $2\cdot x$
- **Simple simplifaction.** This means reducing parts like $x + 0$ or $1\cdot x$ into $x$.
- **Evaluating expressions.** If you have $ax^2 + bx + c$ you can input _a, b, c_ and _x_ and it will give you the value.
- **Output LaTeX.** After inputting your math you can view the ast or, if you are a human, you can also view the Latex.

## Common pitfalls

1. You must always specify multiplication. Usually you can just write $3x$ and everyone knows it is $3\cdot x$. My program doesn't


## Running it locally

To run this project you need:
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [graphviz](https://graphviz.org)
- [git](https://git-scm.com/install/windows)

To run the web ui just run the folowing commands:

```bash
git clone https://github.com/fritl/mast.git
cd mast
uv run fastapi dev
```
Then just open [http://localhost:8000](http://localhost:8000)

There's also a small cli you can run but it won't let you do everything unless you are willing to change the code to do the specific action you want to do.
The cli can be run with:

```bash
uv run cli.py
```

## How it works

The processing follows three steps:
1. **Lexing.** In this part the computer converts the input into tokens. While this is not strictly necessary it really helps with the next step because it gets rid of whitespace.
2. **Parsing.** Specifically I used the _Recursive Descent_ parser. This converts the tokens of the previous step into an abstract syntax tree. This tree is useful because it handles precedence and you can work really well with it.

![ast of 3+2*3](./docs/images/3+2*3.svg)
![ast of (3+2)*3](./docs/images/(3+2)*3.svg)

3. **Manipulating the AST.** Once you have parsed the input you can do a lots of actions like simplifying, differentiating or evaluating on the ast

This process is also a big part of what compilers do. Of course there is much more to writing a compiler than to a mat pareser but I think I still got a good understanding on how you could write a compiler.

## What I have not done

You could go on and do much more with the ast. Just to name a few:
- Improve simplification to also simplify e.g. $3x + 2x \to 5x$
- Check two expressions for equality. This sounds simple but if you want to compare $(x+1)^2 = x^2 + 2x + 1$ you need to find some standardized form which is really difficult.
- Improve input. You currently cannot input $3(x + 2)$ because it is too hard to differentiate between 3 beeing a simple number and 3 beeing a function call like $sin(x)$
