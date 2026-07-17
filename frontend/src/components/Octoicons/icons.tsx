import { ComponentProps } from "solid-js";

export function CommitIcon(props: ComponentProps<"svg">) {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16"
            height="16" fill="currentcolor" {...props}><path d="M11.93 8.5a4.002 4.002 0 0 1-7.86 0H.75a.75.75 0 0 1
0-1.5h3.32a4.002 4.002 0 0 1 7.86 0h3.32a.75.75 0 0 1 0 1.5Zm-1.43-.75a2.5 2.5
0 1 0-5 0 2.5 2.5 0 0 0 5 0Z"></path></svg>
    )
}

export function BranchIcon(props: ComponentProps<"svg">) {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16"
            height="16" fill="currentcolor" {...props}><path d="M9.5 3.25a2.25 2.25 0 1 1 3 2.122V6A2.5 2.5 0 0 1 10
8.5H6a1 1 0 0 0-1 1v1.128a2.251 2.251 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.5
0v1.836A2.493 2.493 0 0 1 6 7h4a1 1 0 0 0 1-1v-.628A2.25 2.25 0 0 1 9.5
3.25Zm-6 0a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Zm8.25-.75a.75.75 0 1 0 0
1.5.75.75 0 0 0 0-1.5ZM4.25 12a.75.75 0 1 0 0 1.5.75.75 0 0 0
0-1.5Z"></path></svg>
    )
}

export function TimeIcon(props: ComponentProps<"svg">) {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16"
            height="16" fill="currentcolor" {...props}><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13
0 6.5 6.5 0 0 0-13 0Zm7-3.25v2.992l2.028.812a.75.75 0 0 1-.557
1.392l-2.5-1A.751.751 0 0 1 7 8.25v-3.5a.75.75 0 0 1 1.5 0Z"></path></svg>
    )
}
