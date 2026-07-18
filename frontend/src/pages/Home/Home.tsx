import { type Component } from 'solid-js';
import { Card } from '../../components/Card/Card';
import TextInput from '../../components/TextInput/TextInput';
import { MastContextProvider } from '../../context/MastContext';
import Ast from '../../components/Ast/Ast';
import Latex from '../../components/Latex/Latex';
import styles from "./Home.module.css"
import MathActions from '../../components/MathActions/MathActions';
import { Tutorial } from './Tutorial';

const App: Component = () => {
    return <MastContextProvider>
        <div class={styles.gridContainer}>
            <Card style="grid-area: input;" title='Input'>
                <TextInput title='Math Expression' name="expr" autocomplete='off' placeholder='Math Input' />
                <MathActions />
            </Card>
            <Card style="grid-area: ast;" title="AST">
                < Ast />
            </Card>
            <Card style="grid-area: latex;" title='LaTeX'>
                <Latex />
            </Card>
        </div>
        <div class={styles.tutorialContainer}>
            <Tutorial />
        </div>
    </MastContextProvider >
};

export default App;
