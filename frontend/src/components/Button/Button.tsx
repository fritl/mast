import { ComponentProps, mergeProps, splitProps } from "solid-js";
import style from "./Button.module.css"

type ButtonType = "primary" | "default"
type Props = ComponentProps<"button"> & { variant?: ButtonType }

export default function Button(props: Props) {
    const merged = mergeProps({ variant: "default" as ButtonType }, props)
    const [local, rest] = splitProps(merged, ["variant", "class"])

    return <button
        classList={{
            [style.button]: true,
            [style.primaryButton]: local.variant === "primary",
            [local.class ?? ""]: !!local.class
        }}
        {...rest}
    />
}
