import { ComponentProps, createResource, Match, Switch } from "solid-js";
import { useMastContext } from "../../context/MastContext";
import styles from "./Ast.module.css"
import Button from "../Button/Button";

async function fetchAst(mathInput: string): Promise<string> {
    const res = await fetch("/api/ast", {
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({ "expr": mathInput })
    })
    if (!res.ok) {
        throw new Error((await res.json())["detail"])
    }
    return res.text()
}

export default function Ast(props: ComponentProps<"div">) {
    const { mathInput } = useMastContext()
    const [ast, { refetch }] = createResource(mathInput, fetchAst)
    return <div class={styles.astContainer}>
        <Switch>
            <Match when={ast.loading}>
                <p>Loading AST ...</p>
            </Match>
            <Match when={ast.error}>
                <p style={"color: red"}>{ast.error.message}</p>
            </Match>
            <Match when={ast()}>
                <div innerHTML={ast()} {...props} />
            </Match>
        </Switch >
    </div>
}
