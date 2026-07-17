import { CommitIcon, BranchIcon, TimeIcon } from "../Octoicons/icons"
import style from "./Footer.module.css"

export default function () {
    const config = {
        commit: import.meta.env.VITE_GIT_COMMIT,
        branch: import.meta.env.VITE_GIT_BRANCH,
        build_time: import.meta.env.VITE_BUILD_TIME,
    }
    return <footer class={style.footer}>
        <div class={style.iconContainer}>
            <p><CommitIcon style="display: inline; vertical-align: middle;" class={style.icon} /> {config.commit}</p>
            <p><BranchIcon style="display: inline; vertical-align: middle;" class={style.icon} /> {config.branch}</p>
            <p><TimeIcon style="display: inline; vertical-align: middle;" class={style.icon} />{config.build_time}</p>
        </div>
    </footer>
}
