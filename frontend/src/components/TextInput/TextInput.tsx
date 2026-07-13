import { ComponentProps, JSX } from "solid-js";
import styles from "./TextInput.module.css"
import { useMastContext } from "../../context/MastContext";

interface TextInputProps extends ComponentProps<"input"> {
    title: string
}

export default function TextInput(props: TextInputProps): JSX.Element {
    const { mathInput, setMathInput } = useMastContext()
    return (
        <label class={styles.inputWrapper}>
            <span class={styles.labelText}>{props.title}</span>
            <input
                class={styles.inputField}
                value={mathInput()}
                oninput={(e) => setMathInput(e.currentTarget.value)}
                {...props}
            />
        </label>
    )
}
