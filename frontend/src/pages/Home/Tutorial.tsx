import { A } from "@solidjs/router";
import style from "./Tutorial.module.css"
import Accordion from "@corvu/accordion";

export function Tutorial() {
    style
    return (
        <>
            <Accordion>
                <Accordion.Item>
                    <Accordion.Trigger class={style.accordion}>
                        <h1>Tutorial</h1>
                    </Accordion.Trigger>
                    <Accordion.Content class={style.accordion}>
                        This section walks you through every feature of MAST. For more background
                        on how it works under the hood, check out the <A href="/info">Info</A> page.

                        <h2>Input & Output</h2>
                        Type any math expression into the input field. The LaTeX and ast update automatically
                        <br />
                        You can use the operators <code>+</code>, <code>-</code>, <code>*</code>,
                        <code>/</code>, <code>^</code>, parentheses for grouping, and the
                        functions <code>sqrt</code>, <code>sin</code>, <code>cos</code>, <code>tan</code>, <code>ln</code>, and <code>log</code>.
                        as well as the constants <code>pi</code> and <code>e</code>
                        <br />
                        One thing to watch out for: MAST always needs an
                        explicit <code>*</code> for multiplication. Even though <code>3x</code> is common
                        shorthand in math class, you have to type <code>3*x</code>.

                        <h2>The AST</h2>
                        The Abstract Syntax Tree of any math expression is shown in the second panel.
                        By default, the AST for <code>3*x+12</code> is displayed. It should be
                        fairly clear how the tree represents the equation. If not, try experimenting
                        a bit. Type <code>3+2*4</code> and then <code>(3+2)*4</code> and watch how
                        the tree changes to account for parentheses and operator precedence.

                        <h2>Simplify</h2>
                        Click <strong>Simplify</strong> to reduce your expression to a shorter,
                        equivalent form. Try typing <code>x+x</code> and hitting Simplify to see
                        it collapse to <code>2*x</code>. Or try <code>x*(1/x)</code>. It is
                        worth noting, that simplification can only be done once on any
                        expression. Clicking Simplify more than once won't simplify any
                        more.

                        <h2>Differentiate</h2>
                        Click <strong>Differentiate</strong> to compute the derivative with respect
                        to the variable shown next to the button (click the variable to change it).
                        Try <code>x^2+3*x</code> and see what comes out (it should be <code>2*x+3</code>).
                        After each differentiation it is reccomended to simplify once.

                        <h2>Evaluate</h2>
                        Want an actual number? Set values for your variables under
                        <strong>Variables</strong>, then click <strong>Evaluate</strong>. For
                        <code>3*x+12</code> with <code>x = 2</code>, you should get <code>18</code>.

                        <h2>LaTeX</h2>
                        The bottom panel shows your expression typeset as proper math notation,
                        the way you'd see it in a textbook. It updates automatically alongside the
                        AST as you type or apply any of the operations above. Try
                        <code>sqrt(x)+2^3</code> and see how it's rendered.
                    </Accordion.Content>
                </Accordion.Item>
            </Accordion >
        </>
    )
}
