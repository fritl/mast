import { type Component } from 'solid-js';
import { Router, Route } from '@solidjs/router';
import Info from './pages/Info/Info';
import Home from './pages/Home/Home';
import style from "./App.module.css"
import Footer from './components/Footer/Footer';
import Header from './components/Header/Header';

const App: Component = (props) => {
    return (<>
        <div class={style.appContainer}>
            <Header />
            {props.children}
        </div>
        <Footer />
    </>
    )
};

export default App;
