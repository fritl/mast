import { ComponentProps, Match, Switch } from "solid-js";
import { useMastContext } from "../../context/MastContext";
import styles from "./Ast.module.css"

export default function Ast(props: ComponentProps<"div">) {
    const { ast, errorMsg } = useMastContext()
    return <div class={styles.astContainer}>
        <Switch>
            <Match when={errorMsg()}>
                <p style={"color: red"}>{errorMsg()}</p>
            </Match>
            <Match when={ast()}>
                <div innerHTML={ast()!} {...props} />
            </Match>
        </Switch>
    </div >
}
