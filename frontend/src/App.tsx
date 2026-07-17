import { type Component } from 'solid-js';
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
