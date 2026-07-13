import { ComponentProps, splitProps } from "solid-js";
import styles from "./Card.module.css"

export function Card(props: ComponentProps<"div"> & { title: string }) {
    const [local, remaining] = splitProps(props, ["title", "children", "class"]);

    return (
        <div
            {...remaining}
            // Hier führen wir die CSS-Module-Klasse und eventuelle externe Klassen zusammen
            class={`${styles.card} ${local.class || ""}`.trim()}
        >
            <h2 class={styles.cardTitle}>{local.title}</h2>
            <div class={styles.cardContainer}>
                {local.children}
            </div>
        </div>
    );
}
