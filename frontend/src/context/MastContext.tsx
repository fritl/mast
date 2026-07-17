import { Accessor, createContext, createEffect, createSignal, onCleanup, ParentProps, Setter, useContext } from "solid-js";

interface MastContextType {
    mathInput: Accessor<string>
    setMathInput: Setter<string>
    latex: Accessor<string | null>
    ast: Accessor<string | null>
    errorMsg: Accessor<string | null>
}

export const MastContext = createContext<MastContextType>()

export function useMastContext() {
    const context = useContext(MastContext)
    if (!context) {
        throw new Error("useMastContext must be used within MastContextProvider")
    }
    return context
}

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

export function MastContextProvider(props: ParentProps) {
    const [mathInput, setMathInput] = createSignal<string>("3*x+12")
    const [latex, setLatex] = createSignal<string | null>(null);
    const [astSvg, setAstSvg] = createSignal<string | null>(null);
    const [errorMsg, setErrorMsg] = createSignal<string | null>(null);

    createEffect(() => {
        let math = mathInput();
        const timer_latex = setTimeout(() => {
            fetchLatex(math).then((v) => {
                setErrorMsg(null);
                setLatex(v);
            }).catch((error) => {
                setLatex(null);
                setErrorMsg(error.message);
            }
            );
        }, 500)

        const timer_ast = setTimeout(() => {
            fetchAst(math).then((v) => {
                setErrorMsg(null);
                setAstSvg(v);
            }).catch((error) => {
                setAstSvg(null);
                setErrorMsg(error.message);
            });
        }, 500)

        onCleanup(() => {
            clearTimeout(timer_latex);
            clearTimeout(timer_ast);
        })
    })

    return <MastContext.Provider value={{ mathInput, setMathInput, latex, errorMsg, ast: astSvg }}>
        {props.children}
    </MastContext.Provider>
}
