import { createSignal } from "solid-js";
import Button from "./components/Button/Button";
import TextInput from "./components/TextInput/TextInput";
import { useMastContext } from "./context/MastContext";
import style from "./MathActions.module.css"

async function simplifyApi(mathInput: string) {
    const res = await fetch("/api/simplify", {
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({ "expr": mathInput })
    })
    if (!res.ok) {
        throw new Error(await res.json())
    }
    return res.json()
}

async function differentiateApi(mathInput: string, wrt: string) {
    const res = await fetch("/api/differentiate", {
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({ "expr": mathInput, "wrt": wrt })
    })
    if (!res.ok) {
        throw new Error(await res.json())
    }
    return res.json()
}

export default function MathActions() {
    const { mathInput, setMathInput } = useMastContext()
    const [wrt, setWrt] = createSignal<string>("x")
    return (
        <div class={style.container}>
            <Button onclick={() =>
                simplifyApi(mathInput()).then(setMathInput).catch(() => { })
            }
            >
                Simplify
            </Button>
            <div class={style.diffcontainer}>
                <Button onclick={() =>
                    differentiateApi(mathInput(), wrt()).then(setMathInput).catch(() => { })
                }
                >
                    Differentiate
                </Button>
                <TextInput
                    title="Wrt"
                    name="wrt"
                    value={wrt()}
                    oninput={(e) => setWrt(e.currentTarget.value)}
                    style={"field-sizing: content; min-width: 4ch; text-align: center;"}
                />
            </div>
        </div >
    )
}
