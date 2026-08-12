import { useState } from "react";
import board from "./assets/board.svg"
import "./App.css";

function App() {
    const [count, setCount] = useState(0);

    return (
        <>
            <div>
                <img src={board} className="logo react logo-spin" alt="board" />
            </div>
        </>
    );
}

export default App;
