import Accordion from "@corvu/accordion"
import style from "./Info.module.css"
import faqData from "./faqdata.json"
import { For } from "solid-js"

export default function Info() {
    return <div class={style.wrapper}>
        <h1>FAQ</h1>
        <Accordion>
            <For each={Object.entries(faqData)}>
                {([question, answer], _) =>
                    <Accordion.Item>
                        <Accordion.Trigger class={style.accordion}><p innerHTML={question} /></Accordion.Trigger>
                        <Accordion.Content class={style.accordion}>
                            <div class={style.contentWrapper}>
                                <p style="white-space: pre-line;" innerHTML={answer} />
                            </div>
                        </Accordion.Content >
                    </Accordion.Item >
                }
            </For>
        </Accordion >
    </div >
}
