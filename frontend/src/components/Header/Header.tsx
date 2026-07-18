import { A } from "@solidjs/router";
import style from "./Header.module.css"
import logo_dark from "../../assets/logo_dark_export.svg"
import logo_light from "../../assets/logo_light_export.svg"

export default function Header() {
    return (
        <header class={style.header}>
            <A href="/" class={style.imageLink}>
                <picture class={style.headerLogo}>
                    <source srcset={logo_light} media="(prefers-color-scheme: light)" class={style.headerLogo} />
                    <source srcset={logo_dark} media="(prefers-color-scheme: dark)" class={style.headerLogo} />
                    <img src={logo_dark} class={style.headerLogo} alt="Logo" />
                </picture>
            </A>
            <nav class={style.nav}>
                <A href="/" class={style.A}>Home</A>
                <A href="/info" class={style.A}>Info</A>
            </nav>
        </header >
    )
}
