import { ComponentProps, createResource, Match, onMount, Switch } from "solid-js"
import { useMastContext } from "../../context/MastContext"
import style from "./Latex.module.css"
import katex from "katex"
import Button from "../Button/Button"

async function fetchLatex(mathInput: string): Promise<string> {
    const res = await fetch("/api/latex", {
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({ "expr": mathInput })
    })
    if (!res.ok) {
        throw new Error((await res.json())["detail"])
    }
    return res.json()
}

function KatexRenderer(props: { tex: string }) {
    let el!: HTMLDivElement;
    onMount(() => {
        katex.render(props.tex, el)
    })
    return <div ref={el} />
}

export default function Latex(props: ComponentProps<"div">) {
    const { mathInput } = useMastContext()
    const [latex, { refetch }] = createResource(mathInput, fetchLatex)
    return <div class={style.container} {...props}>
        <Switch>
            <Match when={latex.loading}>
                <p>Loading AST ...</p>
            </Match>
            <Match when={latex.error}>
                <p style={"color: red"}>{latex.error.message}</p>
            </Match>
            <Match when={latex()}>
                <div class={style.latexContainer}>
                    <KatexRenderer tex={latex()!} />
                </div>
            </Match>
        </Switch >
    </div>
}
