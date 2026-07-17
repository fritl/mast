import { ComponentProps, createEffect, Match, Switch } from "solid-js"
import { useMastContext } from "../../context/MastContext"
import style from "./Latex.module.css"
import katex from "katex"

function KatexRenderer(props: { tex: string }) {
    let el!: HTMLDivElement;
    createEffect(() => {
        katex.render(props.tex, el)
    })
    return <div ref={el} />
}

export default function Latex(props: ComponentProps<"div">) {
    const { latex, errorMsg } = useMastContext()
    return <div class={style.container} {...props}>
        <Switch>
            <Match when={errorMsg()}>
                <p style={"color: red"}>{errorMsg()}</p>
            </Match>
            <Match when={latex()}>
                <div class={style.latexContainer}>
                    <KatexRenderer tex={latex()!} />
                </div>
            </Match>
        </Switch>
    </div >
}
