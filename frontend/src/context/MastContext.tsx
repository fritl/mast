import { Accessor, createContext, createSignal, ParentProps, Setter, useContext } from "solid-js";

interface MastContextType {
    mathInput: Accessor<string>
    setMathInput: Setter<string>
}

export const MastContext = createContext<MastContextType>()

export function useMastContext() {
    const context = useContext(MastContext)
    if (!context) {
        throw new Error("useMastContext must be used within MastContextProvider")
    }
    return context
}

export function MastContextProvider(props: ParentProps) {
    const [mathInput, setMathInput] = createSignal<string>("3*x+12")
    return <MastContext.Provider value={{ mathInput, setMathInput }}>
        {props.children}
    </MastContext.Provider>
}
