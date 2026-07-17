import { createEffect, createSignal, For, Show } from "solid-js";
import Button from "../Button/Button";
import TextInput from "../TextInput/TextInput";
import { useMastContext } from "../../context/MastContext";
import style from "./MathActions.module.css"
import { createStore } from "solid-js/store";

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

async function evaluateApi(mathInput: string, environment: Record<string, number>) {
    const res = await fetch("/api/evaluate", {
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({ "expr": mathInput, "env": environment })
    })
    if (!res.ok) {
        throw new Error(await res.json())
    }
    return res.json()
}

export default function MathActions() {
    const { mathInput, setMathInput } = useMastContext()
    const [wrt, setWrt] = createSignal<string>("x")
    const [values, setValues] = createSignal<string[]>([]);
    const [valueStore, setValueStore] = createStore<Record<string, number>>({});
    const [result, setResult] = createSignal<Number | null>(null);

    createEffect(async () => {
        const res = await fetch("/api/variables", {
            headers: {
                "Content-Type": "application/json"
            },
            method: "POST",
            body: JSON.stringify({ "expr": mathInput() })
        })
        if (!res.ok) {
            throw new Error(await res.json())
        }
        const values = await res.json();
        for (const v of values) {
            setValueStore(v, 0);
        }
        setValues(values);
    })

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
                    name="wrt"
                    value={wrt()}
                    oninput={(e) => setWrt(e.currentTarget.value)}
                    style={"field-sizing: content; min-width: 4ch; text-align: center;"}
                    placeholder="wrt"
                />
            </div>
            <div class={style.evalcontainer}>
                <Button onclick={() => { evaluateApi(mathInput(), valueStore).then(setResult) }}>Evaluate</Button>
                <p>Variables:</p>
                <For each={values()}>
                    {
                        (item, _) => (<div class={style.valuecontainer}>
                            <span>{item} = </span>
                            <TextInput
                                style={"field-sizing: content; min-width: 4ch; text-align: center;"}
                                oninput={(e) => setValueStore(item, Number(e.currentTarget.value))}
                                value={0}
                                name={item}
                                type="number"
                            />
                        </div>
                        )
                    }
                </For>
                <Show when={result()}>
                    <>Result: {result()}</>
                </Show>
            </div>
        </div >
    )
}
