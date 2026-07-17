/* @refresh reload */
import { render } from 'solid-js/web';
import 'solid-devtools';

import './index.css';
import "katex/dist/katex.min.css"
import { Router, Route } from '@solidjs/router';
import Home from './pages/Home/Home';
import Info from './pages/Info/Info';
import App from './App';

const root = document.getElementById('root');

if (import.meta.env.DEV && !(root instanceof HTMLElement)) {
    throw new Error(
        'Root element not found. Did you forget to add it to your index.html? Or maybe the id attribute got misspelled?',
    );
}

render(() => {
    return (
        <Router root={App}>
            <Route path={"/"} component={Home} />
            <Route path={"/info"} component={Info} />
        </Router>
    )
}
    , root!);
